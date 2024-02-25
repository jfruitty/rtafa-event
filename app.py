from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from io import BytesIO
from rembg import remove

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        # If the user does not select a file, browser submits an empty file
        if file.filename == '':
            return render_template('index.html', error='No selected file')

        # If the file is allowed and valid
        if file and allowed_file(file.filename):
       
            person = 'person.jpg'
            person_output = 'person_output.png'
            background = 'bg2.png'
            text = 'text.png'
            new_bg_output= 'output_combined.png'

            file.save(person)


            remove_background(person, person_output)

            combine_images(person_output, background, "output_combined.png")

            combine_images2(text, new_bg_output, new_bg_output)
        

            # Return the processed image
            return send_file(new_bg_output, as_attachment=True)

    return render_template('index.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)
