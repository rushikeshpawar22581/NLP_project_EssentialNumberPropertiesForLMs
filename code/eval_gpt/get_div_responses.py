import openai
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
rpm = 3

client = openai.Client(api_key=api_key)

#read in the data
with open("../../data/division_dataset.json", "r") as f:
    data = json.load(f)

batch_prompts = []
batch_size = 100 # set arbitrarily

#each element in data is a list of 5 numbers. We are concerned with the first two numbers for forming the prompts. Go through the data and generate prompts in batches of 100. Each prompt should be 'What is <num0> / <num1> correct to 4 decimal digits?'

index = 0

while index < len(data):
    batch_prompt = []
    for i in range(index, min(index+batch_size, len(data))):
        num0 = data[i][0]
        num1 = data[i][1]
        batch_prompt.append([num0, num1])
    batch_prompts.append(batch_prompt)
    index += batch_size

print("Number of batches:", len(batch_prompts))
print("Number of prompts in each batch:", [len(batch) for batch in batch_prompts])

filepath = "./division_responses4.txt"

for _, batch_prompt in enumerate(batch_prompts):

    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you some division questions. Please answer in the correct format. For example, if I ask 'What is 1 / 2 correct to 4 digits after decimal point?',you should answer '1 / 2 = 0.5000'. Each question is in a separate line. Please return each answer in a separate line with required accuracy."},
            {"role" : "user", "content" : "".join([f"What is {prompt[0]} / {prompt[1]} correct to 4 digits after decimal point?\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    time.sleep(60//rpm) #to avoid rate limit errors

#do the same. this time, ask for 8 digits after decimal point

filepath = "./division_responses8.txt"

for _, batch_prompt in enumerate(batch_prompts):

    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you some division questions. Please answer in the correct format. For example, if I ask 'What is 1 / 2 correct to 8 digits after decimal point?',you should answer '1 / 2 = 0.50000000'. Each question is in a separate line. Please return each answer in a separate line with required accuracy."},
            {"role" : "user", "content" : "".join([f"What is {prompt[0]} / {prompt[1]} correct to 8 digits after decimal point?\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    time.sleep(60//rpm) #to avoid rate limit errors

print("Responses written to file:", filepath)

#do the same. this time, ask for 12 digits after decimal point

filepath = "./division_responses12.txt"

for _, batch_prompt in enumerate(batch_prompts):
    
    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you some division questions. Please answer in the correct format. For example, if I ask 'What is 1 / 2 correct to 12 digits after decimal point?',you should answer '1 / 2 = 0.500000000000'. Each question is in a separate line. Please return each answer in a separate line with required accuracy."},
            {"role" : "user", "content" : "".join([f"What is {prompt[0]} / {prompt[1]} correct to 12 digits after decimal point?\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    time.sleep(60//rpm) #to avoid rate limit errors



