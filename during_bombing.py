# CITY BIRD'S EYE VIEW WHEN GETTING NUKED

from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import imageio
import random
import math
import cv2

# GET BUILDINGS MASK OF THE TOKYO IMAGE
tokyo = cv2.imread('photos/cityscape of tokyo.jpg')
gray = cv2.cvtColor(tokyo, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, threshold1=50, threshold2=150) # Apply edge detection (e.g., Canny edge detection)
kernel = np.ones((5, 5), np.uint8) # Use dilation to make the mask solid (fills gaps)
mask = cv2.dilate(edges, kernel, iterations=1)
mask = cv2.bitwise_not(mask) # Invert the mask so that buildings are white and sky is black
mask_pil = Image.fromarray(mask) # Convert the mask to a format usable by PIL
mask_pil.save('output/buildings_mask.png') # Save the mask if needed

# CREATE DURING BOMBING IMAGE
tokyo = Image.open('photos/cityscape of tokyo.jpg')
during_bomb = tokyo
during_bomb.thumbnail((800,800))

bomber = Image.open('photos/bomber 2.png').convert("RGBA")
bomber.thumbnail((80, 80))
during_bomb.paste(bomber, (200, 180), bomber)

droppedBomb = Image.open('photos/drop bomb.png').convert("RGBA")
droppedBomb.thumbnail((80,80))
droppedBomb = droppedBomb.rotate(-68, expand=True)
bomb_drop_start_y = (570, 130)
bomb_drop_end = (570, 300)

jetFighter = Image.open('photos/jet fighter.png').convert("RGBA")
jetFighter.thumbnail((280,280))
during_bomb.paste(jetFighter, (470, 10), jetFighter)

display(during_bomb)
during_bomb.save('output/during_bomb.jpg')

# ADD BOMB DROP AND EXPLOSION ANIMATION TO DURING BOMBING IMAGE
num_frames = 30
fall_speed = 10
bomb_start_x = 570
bomb_start_y = 130
bomb_stop_y = 300

frames = []

for i in range(num_frames):
    # Create a new frame by copying the base image
    frame = during_bomb.copy()

    # Calculate the current y position of the bomb (falling downwards)
    current_y_position = bomb_start_y + (i * fall_speed)

    # If the bomb has reached the stopping point, stop moving it further
    if current_y_position >= bomb_stop_y:
        current_y_position = bomb_stop_y

    # Paste the bomb image onto the frame at the specified starting x position and calculated y position
    frame.paste(droppedBomb, (bomb_start_x, current_y_position), droppedBomb)

    # Append the frame to the list
    frames.append(frame)


# Add Explosion animation
explosion = Image.open('photos/bomb (2).png').convert("RGBA")
explosion = explosion.resize((200, 200))

explosion1_start_x = 520
explosion1_stop_y = 300
num_frames = 20  # Number of frames for the animation
scale_factor = 1.02  # Scale factor for enlargement in each step

for i in range(num_frames):
    # Resize the object incrementally
    new_size = (int(explosion.width * (scale_factor ** i)), int(explosion.height * (scale_factor ** i)))
    resized_object = explosion.resize(new_size, Image.Resampling.LANCZOS)

    # Create a copy of the base image for each frame
    frame = during_bomb.copy()

    # Calculate position to keep the object centered while enlarging
    position = (explosion1_start_x - (new_size[0] - explosion.width) // 2,
                explosion1_stop_y - (new_size[1] - explosion.height) // 2)

    # Paste the resized object onto the frame
    frame.paste(resized_object, position, resized_object)

    # Append the frame to the list
    frames.append(frame)




# CREATE THE HELL TOKYO IMAGE
tokyo = Image.open('photos/cityscape of tokyo.jpg').convert("RGBA")
hell_tokyo = tokyo
hell_tokyo.thumbnail((800, 800))
display(hell_tokyo)

# Decrease brightness
enhancer = ImageEnhance.Brightness(hell_tokyo)
hell_tokyo = enhancer.enhance(0.5)

# Add reddish colour filter
orange_overlay = Image.new("RGBA", hell_tokyo.size, (210, 116, 52))
hell_tokyo = Image.blend(hell_tokyo, orange_overlay, alpha=0.2)

# Create the apocalyptic background
hell_background = Image.open('photos/hell_bg2.webp').convert("RGBA")
hell_background = hell_background.resize(hell_tokyo.size)
  # blur the background
hell_background = hell_background.filter(ImageFilter.GaussianBlur(radius=2))
  # Reduce brightness of bg
enhancer = ImageEnhance.Brightness(hell_background)
hell_background = enhancer.enhance(0.5)
  # Add the mushroom to background
mushroom = Image.open('photos/bomb (3).png').convert("RGBA")
mushroom = mushroom.resize((300, 300))
  # Reduce brightness
enhancer = ImageEnhance.Brightness(mushroom)
mushroom = enhancer.enhance(0.5)
mushroom = mushroom.filter(ImageFilter.GaussianBlur(radius=1))
hell_background.paste(mushroom, (100, 15), mushroom)
  # Apply apocalyptic backgroun without masked buildings
buildings_mask = Image.open('output/buildings_mask.png').convert("L")
buildings_mask = buildings_mask.resize(hell_tokyo.size)
hell_tokyo = Image.composite(hell_background, hell_tokyo, buildings_mask)

# Add smoke to image
smoke = Image.open('photos/smoke4.png').convert("RGBA")
  # Crop
width, height = smoke.size
crop_amount = 300
crop_amount = min(crop_amount, width // 2)
smoke = smoke.crop((crop_amount, 0, width - crop_amount, height))
smoke = smoke.resize((hell_tokyo.width, 250))
  # Reduce brightness
enhancer = ImageEnhance.Brightness(smoke)
smoke = enhancer.enhance(-1)
  # Reduce transparency
r, g, b, alpha = smoke.split()
alpha = alpha.point(lambda p: p * 0.5)
smoke = Image.merge("RGBA", (r, g, b, alpha))
hell_tokyo.paste(smoke, (0, 50), smoke)

# Add another mushroom
mushroom2 = Image.open('photos/mushroom (2).png').convert("RGBA")
mushroom2 = mushroom2.resize((350, 350))
  # reduce halo
r, g, b, alpha = mushroom2.split()
enhanced_alpha = alpha.point(lambda p: min(p * 2, 255))
mushroom2 = Image.merge("RGBA", (r, g, b, enhanced_alpha))
  # Reduce brightness
enhancer = ImageEnhance.Brightness(mushroom2)
mushroom2 = enhancer.enhance(0.5)
hell_tokyo.paste(mushroom2, (450, 20), mushroom2)

display(hell_tokyo)

# Fire sparks image
fireSpark = Image.open('photos/fire spark 3.png').convert("RGBA")
fireSpark = fireSpark.resize((hell_tokyo.width, (hell_tokyo.height*2)))
  # Reduce transparency
r, g, b, alpha = fireSpark.split()
alpha = alpha.point(lambda p: p * 0.5)
fireSpark = Image.merge("RGBA", (r, g, b, alpha))
  # blur the background
fireSpark = fireSpark.filter(ImageFilter.GaussianBlur(radius=1))


# ADD THE SPARKS ANIMATION AND FRAME CHANGING ANIMATION
ori_tokyo = Image.open('photos/cityscape of tokyo.jpg').convert("RGBA")
ori_tokyo.thumbnail((800,800))

num_frames = 60  # Number of frames in the animation
vertical_shift_per_frame = -5  # Pixels to move up each frame
amplitude = 10  # Amplitude for horizontal wiggle
frequency = 0.2  # Frequency for horizontal wiggle

i = 0
while i < num_frames:
    frame = hell_tokyo.copy()
    special_frame_interval = random.randint(8, 13)

    # Check if it's time to show the special image
    if i % special_frame_interval == 0:
        # Generate a random number of frames (between 1 and 2)
        special_duration = random.randint(1, 2)

        # For the number of frames determined by random, paste the special image
        for _ in range(special_duration):
            # Create a copy of the base image to hold the special image
            frame.paste(ori_tokyo, (0, 0), ori_tokyo)  # Paste it in the same position

            # Append the frame with the special image to the list
            frames.append(frame)

        # Increment `i` by the random duration to skip to the next segment
        i += special_duration
    else:
        # Regular animation: Calculate the vertical and horizontal shift
        vertical_shift = i * vertical_shift_per_frame
        if vertical_shift >= fireSpark.height - hell_tokyo.height:
            vertical_shift = vertical_shift % (fireSpark.height - hell_tokyo.height)

        horizontal_shift = int(amplitude * math.sin(frequency * i))

        # Apply transformation to create the offset effect
        transformed_sparks = fireSpark.transform(
            fireSpark.size,
            Image.AFFINE,
            (1, 0, horizontal_shift, 0, 1, -vertical_shift),
            resample=Image.NEAREST
        )

        # Crop the transformed sparks to the base image size
        cropped_sparks = transformed_sparks.crop((0, 0, hell_tokyo.width, hell_tokyo.height))

        # Paste the cropped, shifted sparks onto the frame
        frame.paste(cropped_sparks, (0, 0), cropped_sparks)

        # Append the regular animation frame to the list
        frames.append(frame)

        # Increment frame counter
        i += 1


# Save the animation as a GIF
frames[0].save('output/bombing_animation.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)

# Alternatively, save as a video using imageio
imageio.mimsave('output/bombing_animation.mp4', [frame.convert("RGB") for frame in frames], fps=10)