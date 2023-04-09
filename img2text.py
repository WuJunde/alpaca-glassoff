
from transformers import pipeline

# img_pth = "https://ankur3107.github.io/assets/images/image-captioning-example.png"

def imgcap(img_pth):

    image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

    return image_to_text(img_pth)
