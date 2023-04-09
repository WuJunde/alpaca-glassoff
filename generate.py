import sys

import fire
import torch
from peft import PeftModel
import transformers
import gradio as gr
from img2text import imgcap

assert (
    "LlamaTokenizer" in transformers._import_structure["models.llama"]
), "LLaMA is now in HuggingFace's main branch.\nPlease reinstall it: pip uninstall transformers && pip install git+https://github.com/huggingface/transformers.git"
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

try:
    if torch.backends.mps.is_available():
        device = "mps"
except:
    pass


def main(
    load_8bit: bool = False,
    base_model: str = "",
    lora_weights: str = "tloen/alpaca-lora-7b",
):
    assert base_model, (
        "Please specify a --base_model, e.g. --base_model='decapoda-research/llama-7b-hf'"
    )

    tokenizer = LlamaTokenizer.from_pretrained(base_model)
    if device == "cuda":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            torch_dtype=torch.float16,
        )
    elif device == "mps":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
    else:
        model = LlamaForCausalLM.from_pretrained(
            base_model, device_map={"": device}, low_cpu_mem_usage=True
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
        )


    # unwind broken decapoda-research config
    model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
    model.config.bos_token_id = 1
    model.config.eos_token_id = 2

    if not load_8bit:
        model.half()  # seems to fix bugs for some users.

    model.eval()
    if torch.__version__ >= "2" and sys.platform != "win32":
        model = torch.compile(model)

    def evaluate(
        img,
        instruction,
        input=None,
        temperature=0.1,
        top_p=0.75,
        top_k=40,
        num_beams=4,
        max_new_tokens=128,
        **kwargs,
    ):
        imgtext = imgcap(img)
        # print(imgtext)
        instruction = "Given the following image. " + instruction 
        input = 'The image is ' + imgtext[0]['generated_text'] + '. '
        prompt = generate_prompt(instruction, input)
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            **kwargs,
        )
        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )
        s = generation_output.sequences[0]
        output = tokenizer.decode(s)
        return output.split("### Response:")[1].strip()

    gr.Interface(
        fn=evaluate,
        inputs=[
            gr.components.Image(
                type="pil", label="Image"
            ),
            gr.components.Textbox(
                lines=2, label="Chat", placeholder="Ask me anything"
            ),
            # gr.components.Textbox(lines=2, label="Input", placeholder="none"),
            # gr.components.Slider(minimum=0, maximum=1, value=0.1, label="Temperature"),
            # gr.components.Slider(minimum=0, maximum=1, value=0.75, label="Top p"),
            # gr.components.Slider(
            #     minimum=0, maximum=100, step=1, value=40, label="Top k"
            # ),
            # gr.components.Slider(minimum=1, maximum=4, step=1, value=4, label="Beams"),
            # gr.components.Slider(
            #     minimum=1, maximum=2000, step=1, value=128, label="Max tokens"
            # ),
        ],
        outputs=[
            gr.inputs.Textbox(
                lines=5,
                label="Output",
            )
        ],
        title="Alpaca-GlassOff",
        description="Mini Image-acceptable Chat AI can run on your own laptop. The chat model is based on Alpaca. The server may break down sometimes, give it another try.",
    ).launch(share=True)
    # Old testing code follows.


    # # testing code for readme
    # img = 'https://ankur3107.github.io/assets/images/image-captioning-example.png'
    # for instruction in [
    #     "What is in the iamge.",
    #     "Write me a novel plot based on the image.",
    #     "Where I can find an image like this.",
    #     "Is there any human in the image?",
    #     "How many people in the image?",
    #     "Tell me the most salient object in the image.",
    #     "Describe the image using five words.",
    # ]:
    #     print("Instruction:", instruction)
    #     print("Response:", evaluate(img, instruction))
    #     print()



def generate_prompt(instruction, input=None):
    if input:
        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

        

### Instruction:
{instruction}

### Input:
{input}

### Response:
"""
    else:
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Response:
"""


if __name__ == "__main__":
    fire.Fire(main)
