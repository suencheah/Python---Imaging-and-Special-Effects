# THE STREETS AFTER BOMBING

from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np

crossing = Image.open('photos/shibuya_crossing1.jpg')
crossing.thumbnail((800,800))
display(crossing)

# Mask the lit up screens to reduce the brightness so that it looks broken already.
pixels = crossing.load()

for i in range(crossing.width):
    for j in range(crossing.height):
        r, g, b = pixels[i, j]

        brightness = 0.299 * r + 0.587 * g + 0.114 * b

        if brightness > 180:
            # Reduce brightness
            r = int(r * 0.5)
            g = int(g * 0.5)
            b = int(b * 0.5)

        if g > r * 1.2 and g > b * 1.2:
            # Reduce the saturation by blending with grayscale
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            desaturation_factor = 0  # Adjust this value for more or less desaturation

            r = int(r * desaturation_factor + gray * (1 - desaturation_factor))
            g = int(g * desaturation_factor + gray * (1 - desaturation_factor))
            b = int(b * desaturation_factor + gray * (1 - desaturation_factor))

        pixels[i, j] = (r, g, b)

display(crossing)

# Add land crack
landCrack = Image.open('photos/land_crack_long.png').convert("RGBA")
landCrack.thumbnail((160,160))
landCrack = landCrack.transpose(Image.FLIP_LEFT_RIGHT)
  # Reduce brightnes of crack (make it grey)
r, g, b, alpha = landCrack.split()
rgb_image = Image.merge("RGB", (r, g, b))
enhancer = ImageEnhance.Brightness(rgb_image)
darker_rgb_image = enhancer.enhance(0.3)
darker_landCrack = Image.merge("RGBA", (*darker_rgb_image.split(), alpha))
  # Reduce transparency of crack
alpha_channel = darker_landCrack.split()[3]
alpha_channel = alpha_channel.point(lambda p: p * 0.9)
darker_landCrack.putalpha(alpha_channel)
  # Rotate the crack
darker_landCrack = darker_landCrack.rotate(-10, expand=False)
# display(darker_landCrack)
  # Paste the land crack onto the pucture
crossing.paste(darker_landCrack, (440, (crossing.height-landCrack.height)), darker_landCrack)
# display(crossing)

# Decrease saturation
filter = ImageEnhance.Color(crossing)
crossing = filter.enhance(0.4)

# Add noise for dust/debris
noise = np.random.randint(0, 30, (crossing.size[1], crossing.size[0], 3), dtype='uint8')
crossing = Image.fromarray(np.clip(np.array(crossing) + noise, 0, 255).astype('uint8'))

# display(noisy_image)

# Add smoke overlay
red_smoke_overlay = Image.open('photos/red_smoke.png')
red_smoke_overlay = red_smoke_overlay.resize((crossing.width,crossing.height))
  # Flip vertical
red_smoke_overlay = red_smoke_overlay.transpose(Image.FLIP_TOP_BOTTOM)
red_smoke_overlay = red_smoke_overlay.transpose(Image.FLIP_LEFT_RIGHT)
  # Decrease saturation
smoke_filter = ImageEnhance.Color(red_smoke_overlay)
red_smoke_overlay = smoke_filter.enhance(0)
  # Increase brightness to make the smoke more emphasized
smoke_enhancer = ImageEnhance.Brightness(red_smoke_overlay)
red_smoke_overlay = smoke_enhancer.enhance(1.5)
  # Blend the orange-filtered image with the modified smoke overlay
crossing = Image.blend(crossing, red_smoke_overlay, alpha=0.5)
display(crossing)


# Add colour filter
orange_overlay = Image.new("RGB", crossing.size, (210, 116, 52))
crossing = Image.blend(crossing, orange_overlay, alpha=0.1)
display(crossing);
crossing.save('output/shibuya_crossing.png')