import os
import openai
from datetime import datetime

def GPT_Completion(texts):
## Call the API key under your account (in a secure way)
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt =  texts,
    temperature = 0.6,
    top_p = 1,
    max_tokens = 3800,
    frequency_penalty = 0,
    presence_penalty = 0
    )
    print(response.choices[0].text)
    timestamp = datetime.timestamp(datetime.now())
    with open(str(timestamp) + ".txt", 'w') as file:
        print(response.choices)
        file.write(response.choices[0].text)
    return
def askfromgpt():
    question = input("Question: ")
    GPT_Completion(question)


if __name__ == "__main__":
    askfromgpt()