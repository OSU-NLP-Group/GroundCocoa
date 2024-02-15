# Author: Harsh Kohli
# Date Created: 11-02-2024

from PIL import Image

# Open the .webp image
with Image.open('groundcocoa.webp') as img:
    # Convert the image to PNG and save it
    img.save('static/images/groundcocoa.png', 'PNG')
