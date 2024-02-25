from rembg import remove
from PIL import Image, ImageDraw


def remove_background(input_path, output_path):
    with open(input_path, 'rb') as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)

    with open(output_path, 'wb') as output_file:
        output_file.write(output_data)



def combine_images(image1_path, image2_path, output_image_path, position=(None, None)):
    # Open the first image
    image1 = Image.open(image1_path).convert('RGBA')

    # Open the second image
    image2 = Image.open(image2_path).convert('RGBA')

    # Resize the second image to match the dimensions of the first image
    image2 = image2.resize(image1.size, Image.LANCZOS)

    new_height = int(image2.size[1] * 0.7)  # 25% from the top and 25% from the bottom

    image1 = image1.resize((int(new_height * image1.size[0] / image1.size[1]), new_height), Image.LANCZOS)

    # Create a mask based on the non-white pixels of image1
    mask = Image.new('L', image1.size, 0)
    mask.paste(255, image1.split()[3])  # Use the alpha channel of image1 as the mask

    if position[0] is None:
        position_x = (image2.width - image1.width) // 2
    else:
        position_x = position[0]

    if position[1] is None:
        position_y = (image2.height - image1.height) // 2 
    else:
        position_y = position[1]


    combined_image = Image.new('RGBA', image2.size)  # Create a new image with image2's size
    combined_image.paste(image2, (0, 0))  # Paste image2 onto the new image
    combined_image.paste(image1, (position_x, position_y), mask)  # Paste image1 with the specified offset


    # Save the result
    combined_image.save(output_image_path)

def combine_images_without_resize(image1_path, image2_path, output_image_path, position=(None, None)):
   
    # Open the images
    image1 = Image.open(image1_path).convert('RGBA')
    image2 = Image.open(image2_path).convert('RGBA')

   

    # Check if position is valid
    if position[0] is not None and (position[0] < 0 or position[0] + image1.width > image2.width):
        raise ValueError("Invalid x position: Out of image bounds")
    if position[1] is not None and (position[1] < 0 or position[1] + image1.height > image2.height):
        raise ValueError("Invalid y position: Out of image bounds")

    # Calculate default center position if not provided
    if position[0] is None:
        position_x = (image2.width - image1.width) // 2
    else:
        position_x = position[0]

    if position[1] is None:
        position_y = (image2.height - image1.height) // 2
    else:
        position_y = position[1]

    # Create a new image, paste image2, then image1 with calculated position and mask
    combined_image = Image.new('RGBA', image2.size)
    combined_image.paste(image2, (0, 0))
    combined_image.paste(image1, (position_x, position_y), image1.convert('L'))  # Use image1's alpha channel as mask

    # Save the result
    combined_image.save(output_image_path)

def combine_images2(image1_path, image2_path, output_image_path, position=(None, None)):
    # Open the first image
    image1 = Image.open(image1_path).convert('RGBA')

    # Open the second image
    image2 = Image.open(image2_path).convert('RGBA')

    # Resize the second image to match the dimensions of the first image
    image2 = image2.resize(image1.size, Image.LANCZOS)


    # Create a mask based on the non-white pixels of image1
    mask = Image.new('L', image1.size, 0)
    mask.paste(255, image1.split()[3])  # Use the alpha channel of image1 as the mask

    if position[0] is None:
        position_x = (image2.width - image1.width) // 2
    else:
        position_x = position[0]

    if position[1] is None:
        position_y = (image2.height - image1.height) // 2 + 50
    else:
        position_y = position[1]


    combined_image = Image.new('RGBA', image2.size)  # Create a new image with image2's size
    combined_image.paste(image2, (0, 0))  # Paste image2 onto the new image
    combined_image.paste(image1, (position_x, position_y), mask)  # Paste image1 with the specified offset


    # Save the result
    combined_image.save(output_image_path)







# Replace 'input.jpg' and 'output.png' with your input and output image paths
person = 'person.jpg'
person_output = 'person_output.png'

background = 'bg2.png'
text = 'text.png'
new_bg_output= 'output_combined.png'


remove_background(person, person_output)

combine_images(person_output, background, "output_combined.png")

combine_images2(text, new_bg_output, "output_combined.png")


