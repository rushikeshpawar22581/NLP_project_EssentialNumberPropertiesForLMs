import openai
import json
import os
import time
from dotenv import load_dotenv
import random

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
rpm = 3

client = openai.Client(api_key=api_key)

#read in the data
with open("../../data/primality_test.json", "r") as f:
    data = json.load(f)

primes = data["primes"]
composites= data["composites"]

#we will mix the primes and composites. We are batching the prompts, so we don't want to send all primes first and then all composites. This will make the model biased towards one class. So we will mix the primes and composites in each batch.

combined = primes + composites

#shuffle the combined list
random.seed(42)
random.shuffle(combined)

batch_prompts = []
batch_size = 200

index = 0

while index < len(combined):
    batch_prompt = []
    for i in range(index, min(index+batch_size, len(combined))):
        num = combined[i]
        batch_prompt.append(num)
    batch_prompts.append(batch_prompt)
    index += batch_size

print("Number of batches:", len(batch_prompts))
print("Number of prompts in each batch:", [len(batch) for batch in batch_prompts])

filepath = "./primality_responses_ask_if_prime.txt"

for _, batch_prompt in enumerate(batch_prompts):
    
    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you some questions. Please answer in the correct format. For example, if I ask 'Is 5 a prime number?', you should answer '5:Yes' if 5 is a prime number or '5:No' if 5 is not a prime number. Each question is in a separate line. Please return each answer in a separate line."},
            {"role" : "user", "content" : "".join([f"Is {prompt} a prime number?\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    print("Responses:", responses)
    time.sleep(60//rpm) #to avoid rate limit errors

print("Responses written to file primality_responses_ask_if_prime.txt")

