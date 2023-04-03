import os
import openai
from datetime import datetime
import re
from unidecode import unidecode


def GPT_Completion(texts):
## Call the API key under your account (in a secure way)
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Completion.create(
    engine="gpt-4-32k",
    prompt =  texts,
    temperature = 0.6,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0
    )
    print(response.choices[0].text)
    timestamp = datetime.timestamp(datetime.now())
    with open(slugify(texts)+"_"+str(timestamp) + ".txt", 'w') as file:
        print(response.choices)
        file.write(response.choices[0].text)
    return

def slugify(title):
    # Convert accented characters to ASCII characters
    title = unidecode(title)
    # Convert the title to lowercase and replace spaces with hyphens
    slug = title.lower().replace(" ", "-")
    # Remove any characters that are not alphanumeric or hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)

    return slug

def askfromgpt():
    question = input("Question: ")
    GPT_Completion(question)


if __name__ == "__main__":
    askfromgpt()