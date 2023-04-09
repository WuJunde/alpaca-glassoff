## Alpaca-GlassOff: Image-acceptable Alpaca

Alpaca-GlassOff is a mini image-acceptable Chat AI can run on your own laptop. The chat model is based on [stanford-alpaca](https://github.com/tatsu-lab/stanford_alpaca) and [alpaca-lora](https://github.com/tloen/alpaca-lora).

### Demo

https://32b9d44b2fe3fe91b8.gradio.live

### Example outputs

### Recognization 

**Image**: women bath

**Chat**: what is in the image

**Alpaca-GlassOff**: Three people in bathing suits are in a pool.

---

**Image**: food

**Chat**: what I can make for dinner if have food ingredients like these, and tell me how to do it

**Alpaca-GlassOff**: If you have food ingredients like these, you can make a vegetable stir-fry. Start by heating a tablespoon of oil in a large skillet over medium-high heat. Add the vegetables and stir-fry for 2-3 minutes, until the vegetables begin to soften. Add the garlic and ginger and stir-fry for an additional 1-2 minutes. Add the soy sauce and stir-fry for an additional 1-2 minutes, until the vegetables are cooked through. Serve the stir-fry over a bed of...


---

### Generation

**Image**: flower woman

**Chat**: write a poem for the image

**Alpaca-GlassOff**: 

A woman with a flower in her hair, 
A beauty that can't be denied. 
The petals of the flower, so bright and fair, 
A symbol of life, a symbol of care. 

The flower in her hair, a symbol of joy, 
A reminder of life's beauty, a reminder of love. 
A reminder of life's beauty, a reminder of love. 

---

**Image**: pulp fiction

**Chat**: Tell me a story based on the given image

**Alpaca-GlassOff**: She was a young woman who had just moved into a new apartment. She was excited to explore her new surroundings, but she was also a bit overwhelmed. She decided to take it slow and started by reading the newspaper that had been delivered to her doorstep. As she read, she began to feel more at home in her new home.

---

**Image**: antman

**chat**: who you think would be the best actor of this character

**Alpaca-LoRA**: Tom Hardy 

The actor of venom


#### Fail examples 
---

**Image**: iphone1

**Chat**: What is the generation of this iphone?

**Alpaca-GlassOff**: It is an iPhone 11 

wrong, it is iPhone1

---


**Image**: Exeggutor(pokemon)

**Chat**: What it is?

**Alpaca-GlassOff**: It is a stuffed animal toy with a plant in its mouth 

not good enough, it is pokemon named Exeggutor.

---

### Usage (`Inference on pre-trained model`)

1. Install dependencies

```
pip install -r requirements.txt
```

2. If bitsandbytes doesn't work, [install it from source.](https://github.com/TimDettmers/bitsandbytes/blob/main/compile_from_source.md) Windows users can follow [these instructions](https://github.com/tloen/alpaca-lora/issues/17).


3. run 
```bash
python generate.py \
    --load_8bit \
    --base_model 'decapoda-research/llama-7b-hf' \
    --lora_weights 'tloen/alpaca-lora-7b'
```

### Implementation
At present, an image-caption model is employed to describe an image. Next, the description along with the user's query is combined and sent to a chat model (Alpaca-Lora) for generating the result. This approach is not optimal for building an image-text chat model, but it is cost-effective. The project is undergoing frequent updates and may change its implementation strategy at any time.

### Contribution
Welcome to contribute 






