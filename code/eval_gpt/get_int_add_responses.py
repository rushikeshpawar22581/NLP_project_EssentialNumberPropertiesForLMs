import openai
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = openai.Client(api_key=api_key)

#load in the integer addition data
with open("../../data/int_addition.json", "r") as f:
    data = json.load(f)

rpm = 3
tpm = 40000

tokens_per_request = tpm//rpm

batch_prompts = []
outputs = []

index = 0

while index < len(data):
    expected_num_tokens = max(30, len(data[index])//3) #a heuristic. Can be made more accurate by counting number of tokens.
    if len(batch_prompts) < 27:
        num_prompts = tokens_per_request// expected_num_tokens
    elif len(batch_prompts) < 88:
        num_prompts = 15
    else:
        num_prompts = 150
    batch_prompt = data[index:min(index+num_prompts, len(data))]
    batch_prompts.append(batch_prompt)
    index += num_prompts

print("Number of batches:", len(batch_prompts))
print("Number of prompts in each batch:", [len(batch) for batch in batch_prompts])

filepath = "./int_addition_responses.txt"

for _, batch_prompt in enumerate(batch_prompts):

    if _ < 88:
        continue
    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you some addition questions. Please answer in the correct format. For example, if I ask 'What is 2 + 3?', you should answer '2 + 3 = 5'. Each question is in a separate line. Please return each answer in a separate line."},
            {"role" : "user", "content" : "".join([f"{prompt}\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    #print the prompt and response separated by space
    print(len(batch_prompt), len(responses))

    for prompt, response in zip(batch_prompt, responses):
        print(prompt, response, sep=" ->")
    
    
    print("Received responses for batch", _+1, "of", len(batch_prompts))

    time.sleep(60//rpm) #to avoid rate limit errors

print("Responses saved to", filepath)