from PIL import Image

# 이미지 로드
bgImage = Image.open("Fund.png").resize((240, 240)).convert("RGB")
bubbleImage = Image.open("Say.png").convert("RGBA")
colaImage = Image.open("Cola.png").convert("RGBA")

breadImage = Image.open("Bread.png").convert("RGBA")
vegetableImage = Image.open("Vegetable.png").convert("RGBA")
meatImage = Image.open("Meat.png").convert("RGBA")

mustardImage = Image.open("Mustard.png").convert("RGBA")
ketchupImage = Image.open("Ketchup.png").convert("RGBA")

handImage = Image.open("Hand.png").convert("RGBA").resize((30, 30))
hotdogImage = [
    Image.open("Mustard_Dog.png").convert("RGBA").resize((160, 160)),
    Image.open("ketchup_Dog.png").convert("RGBA").resize((160, 160)),
]

hotdogImages = [
    breadImage,
    vegetableImage,
    meatImage,
    mustardImage,
    ketchupImage
]
