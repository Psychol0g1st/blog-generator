import requests
from PIL import Image
import base64
from io import BytesIO

def download_crop_convert_webp_image(image_url, filename):
    # Download the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Resize the image to 800x450 resolution
    img = img.resize((800, 450))
    
    # Convert the image to the WebP format
    webp_img = BytesIO()
    img.save(webp_img, format="webp")
    
    # Save the WebP image to a file
    with open(filename, "wb") as f:
        f.write(webp_img.getvalue())
    
    # Generate the HTML img tag with the WebP image
    html_tag = f'<img src="{filename}" alt="WebP image">'
    
    return html_tag

imgurl = input("image url: ")
print(download_crop_convert_webp_image(imgurl, "image.webp"))