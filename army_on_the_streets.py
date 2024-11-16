from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np

street = Image.open('photos/tokyo street 1.jpg').convert("RGBA")
street.thumbnail((800,800))

# image enhancement
enhancer = ImageEnhance.Contrast(street)
street = enhancer.enhance(1.5)  # Adjust the factor for desired contrast


# Add the objects
crack1 = Image.open('photos/crack1.png').convert("RGBA")
crack1 = crack1.resize((70,130))
enhancer = ImageEnhance.Brightness(crack1)
crack1 = enhancer.enhance(0.2)
crack1 = crack1.rotate(-90, expand=True)

crack1a = Image.open('photos/crack1.png').convert("RGBA")
crack1a = crack1a.resize((50,100))
enhancer = ImageEnhance.Brightness(crack1a)
crack1a = enhancer.enhance(0.2)
crack1a = crack1a.rotate(90, expand=True)

crack2 = Image.open('photos/crack2.png').convert("RGBA")
crack2.thumbnail((130,400))
enhancer = ImageEnhance.Brightness(crack2)
crack2 = enhancer.enhance(0.2)
crack2 = crack2.rotate(30, expand=True)

crack3 = Image.open('photos/crack3.png').convert("RGBA")
crack3.thumbnail((150,400))
enhancer = ImageEnhance.Brightness(crack3)
crack3 = enhancer.enhance(0.5)
crack3 = crack3.rotate(-20, expand=True)

tape = Image.open('photos/police tape2.png').convert("RGBA")
tape = tape.resize((280,50))
enhancer = ImageEnhance.Brightness(tape)
tape = enhancer.enhance(0.9)

troops = Image.open('photos/troops.png').convert("RGBA")
troops.thumbnail((300,300))
troops = troops.transpose(Image.FLIP_LEFT_RIGHT)
enhancer = ImageEnhance.Brightness(troops)
troops = enhancer.enhance(0.8)

street.paste(crack1, (400, 100), crack1)
street.paste(crack1a, (130, 270), crack1a)
street.paste(crack2, (200, 150), crack2)
street.paste(crack3, (240, 100), crack3)
street.paste(tape, (550, 460), tape)
street.paste(troops, (0, 340), troops)

# Make the sky burning red
image_array = np.array(street)
sky_mask = (image_array[:, :, 2] > 180) & (image_array[:, :, 0] > 150) & (image_array[:, :, 1] > 150)
mask = Image.fromarray((sky_mask * 255).astype('uint8')).convert('L')
overlay = Image.new("RGBA", street.size, (255, 47, 0))
street = Image.composite(Image.blend(street, overlay, 0.6), street, mask)

# Applying red filter to remaining image
street = Image.composite(Image.blend(street, overlay, 0.2), street, street)

# Enhance contrast and saturation to add to the dramatic effect
contrast_enhancer = ImageEnhance.Contrast(street)
street = contrast_enhancer.enhance(0.8)
saturation_enhancer = ImageEnhance.Color(street)
street = saturation_enhancer.enhance(2)

enhancer = ImageEnhance.Brightness(street)
street = enhancer.enhance(1.2)

# Apply sepia filter
gray_image = ImageOps.grayscale(street)
sepia_image = ImageOps.colorize(gray_image, black="#000000", white="#14120f")
enhancer = ImageEnhance.Contrast(sepia_image)
enhanced_sepia_image = enhancer.enhance(1.3)
street = Image.blend(street.convert("RGB"), sepia_image, 0.4)

display(street)
street.save('output/army_on_the_street.jpg')

# Create the illusion of a girl looking outside from her house by putting a  girl's reflection in the window
window = Image.open("photos/window.png").convert("RGBA")
window = window.resize(street.size)

window = window.crop((200,150,window.width-150,window.height-70))
window = window.resize(street.size)

girl = Image.open("photos/girl.png").convert("RGBA")
girl.thumbnail((370,370))
enhancer = ImageEnhance.Brightness(girl)
girl = enhancer.enhance(0.4)
girl_silhoutte = girl

reflection_alpha = girl.split()[3]  # Get the alpha channel (transparency)
reflection_alpha = reflection_alpha.point(lambda p: p * 0.7)  # Decrease the opacity
girl.putalpha(reflection_alpha)

hangingLight = Image.open("photos/hanging light.png").convert("RGBA")
hangingLight.thumbnail((100,100))
hangingLight = hangingLight

reflection_alpha = hangingLight.split()[3]  # Get the alpha channel (transparency)
reflection_alpha = reflection_alpha.point(lambda p: p * 0.8)  # Decrease the opacity
hangingLight.putalpha(reflection_alpha)

cupboard = Image.open("photos/cupboard.png").convert("RGBA")
cupboard.thumbnail((400,400))
enhancer = ImageEnhance.Brightness(cupboard)
cupboard = enhancer.enhance(0.6)

reflection_alpha = cupboard.split()[3]  # Get the alpha channel (transparency)
reflection_alpha = reflection_alpha.point(lambda p: p * 0.7)  # Decrease the opacity
cupboard.putalpha(reflection_alpha)


reflection_in_window = Image.new("RGBA", window.size, (0, 0, 0, 100))
reflection_in_window.paste(girl, (270, (reflection_in_window.height-girl.height)), girl.split()[3])
reflection_in_window.paste(hangingLight, (400, 0), hangingLight.split()[3])
reflection_in_window.paste(cupboard, (0, (reflection_in_window.height-cupboard.height+50)), cupboard.split()[3])
reflection_in_window.paste(window, (0, 0), window.split()[3])

street.paste(reflection_in_window, (0, 0), reflection_in_window)

display(street)


street.save('output/girl_looking_out.jpg')
