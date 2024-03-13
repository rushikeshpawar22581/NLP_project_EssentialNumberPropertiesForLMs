import openai
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = openai.Client(api_key=api_key)

#load in the lists
with open("../../data/lists.json", "r") as f:
    data = json.load(f)

rpm = 3
tpm = 40000

tokens_per_request = tpm//rpm

batch_prompts = []
outputs = []

filepath = "./list_sort_responses.txt"

for list in data:
    list_ = data[list]

    #each list contains a list of numbers. go through 100 of them at a time and create a batch of 100 prompts
    
    index = 0

    while(index < len(list_)):
        batch_prompt = [f"Sort the numbers in the list {list_[i]}" for i in range(index, min(index+100, len(list_)))]
        batch_prompts.append(batch_prompt)
        index += 100
    
print("Number of batches:", len(batch_prompts))
print("Number of prompts in each batch:", [len(batch) for batch in batch_prompts])

for _, batch_prompt in enumerate(batch_prompts):
    
    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you to sort the numbers in a list. Please answer in the correct format. For example, if I ask 'Sort the numbers in the list [3, 1, 4]', you should answer '[1, 3, 4]'. Each question is in a separate line. Please return each answer in a separate line."},
            {"role" : "user", "content" : "".join([f"{prompt}\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    time.sleep(60//rpm) #to avoid rate limit errors