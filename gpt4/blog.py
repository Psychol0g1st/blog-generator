# -*- coding: utf-8 -*-
import os
import openai
import re
import json
from unidecode import unidecode
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
import time

ENGINE = "text-davinci-003"

def saveAnswer(text, title=""):
    timestamp = datetime.timestamp(datetime.now())
    with open("data/"+title+"_"+str(timestamp) + ".txt", 'w', encoding="utf-8") as file:
        file.write(text)

def approve(text):
    print("Generált válasz:\n")
    answer = input("Elfogadod a választ? I(gen)/N(em)\n:")
    return True if (answer.lower() in "igen" and answer.lower() != "n") else False
def generate_chapters(title):
    print("Alcímek generálása...")
    accepted_flag = False
    prompt = f"5 darab alcím {title} című bloghoz"
    response = openai.Completion.create(
        engine=ENGINE,
        prompt = prompt,
        temperature = 0.6,
        max_tokens = 1500,
        frequency_penalty = 0,
        presence_penalty = 0
    )

    text = ("".join([choice.text for choice in response.choices]))
    print(text)
    lines = text.splitlines()
    chapters = [line for line in lines if line.strip()]
    return [chapter[3:] for chapter in chapters]

def generate_blog_from_chapters(chapters):
    prompts = [f"Generálj HTML blogot az alábbi témára: {chapter}." for chapter in chapters]
    response = openai.Completion.create(
        engine=ENGINE,
        prompt = prompts,
        temperature = 0.65,
        max_tokens = 1500,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    html_string =  "".join([choice.text.strip() for choice in response.choices])
    html_string = html_string.replace("h2>", "h3>")
    html_string = html_string.replace("h1>", "h2>")
    body_pattern = re.compile(r'<body>(.*?)</body>', re.DOTALL)
    return ("".join(re.findall(body_pattern, html_string))).strip()
def generate_blog_lead(title):
    prompt = f"Rövid leírás \"{title}\" című bloghoz"
    response = openai.Completion.create(
        engine=ENGINE,
        prompt = prompt,
        temperature = 0.6,
        max_tokens = 700,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    return response.choices[0].text.strip().replace('"', "'")

def getBlogData(file):
    with open(file) as f:
        data = json.load(f)
    return data
def slugify(title):
    # Convert accented characters to ASCII characters
    title = unidecode(title)

    # Convert the title to lowercase and replace spaces with hyphens
    slug = title.lower().replace(" ", "-")

    # Remove any characters that are not alphanumeric or hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)

    return slug

def makeDirectory(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(path + " directory already exists!")

def download_crop_convert_webp_image(image_url, filepath, filename):
    # Download the image from the URL
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(image_url, headers=headers)
    img = Image.open(BytesIO(response.content))

    # Resize the image to 800x450 resolution
    img = img.resize((800, 450))

    # Convert the image to the WebP format
    webp_img = BytesIO()
    img.save(webp_img, format="webp")

    # Save the WebP image to a file
    filename = filename+".webp"
    with open(os.path.join(filepath, filename), "wb") as f:
        f.write(webp_img.getvalue())

    return filename

def saveBlogData(title, keywords, content, lead, imageUrl):
    slug = slugify(title)
    rootPath = "./"
    blogPath = os.path.join(rootPath, slug)
    imagesPath = os.path.join(blogPath, "images")
    makeDirectory(blogPath)
    makeDirectory(imagesPath)

    imageFilePath = download_crop_convert_webp_image(imageUrl, imagesPath, slug)
    blogSummary = {
        "title": title,
        "lead": lead,
        "slug": slug,
        "image": imageFilePath
    }
    pageContent = f'''
<?php
    $articleTitle = "{title}";
    $articleLead = "{lead}";
    $articleImage = "{imageFilePath}";
    $articleImageAlt = "{title}";
    $articleKeywords = "{keywords}";
    $slug = "{slug}";
    $articleImageType = "image/webp";
    $articleContent = '<img src="images/webp/{imageFilePath}" alt="{title}">\n{content}';

include 'blog-template.php';
?>
    '''

    with open(os.path.join(blogPath, slug+".php"), "w", encoding="utf-8") as f:
        f.write(pageContent)
    with open(os.path.join(blogPath, slug+".json"), "w", encoding="utf-8") as f:
        f.write(json.dumps(blogSummary, ensure_ascii=False).encode('utf8').decode())

if __name__ == "__main__":
    openai.api_key = os.environ["OPENAI_API_KEY"]
    print("Adatok beolvasása...")
    blogData = getBlogData("blog-data.json")
    for data in blogData:
        title, keywords, imageUrl = data['title'], data['keywords'], data['image']
        titles = generate_chapters(title)
        print("Blog tartalmának generálása...")
        blog = generate_blog_from_chapters(titles)
        print("Blog leírás generálása...")
        lead = generate_blog_lead(title)
        print("Blog mentése...")

        saveBlogData(title, keywords, blog, lead, imageUrl)

        saveAnswer(blog + "\n" + lead, slugify(title))
        print(f"\n{title} blog generálás sikeresen befejeződött!\n\n")