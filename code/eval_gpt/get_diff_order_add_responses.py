import openai
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = openai.Client(api_key=api_key)

#load in the integer addition data
with open("../../data/diff_order_int_addition.json", "r") as f:
    data = json.load(f)

rpm = 3

batch_size = 100

batch_prompts = []

for sign_of_both in data:
    # sign of both : both pos, bignum pos smallnum neg, bignum neg smallnum pos, both neg
    for digit_of_both in data[sign_of_both]:
        # type of both : d41, d42, d43, d51,..d101, d102, d103
        key_to_get_batch_size = digit_of_both[:2]
        list_data = data[sign_of_both][digit_of_both]
        
        index = 0

        while index< len(list_data):
            batch_prompt = list_data[index:min(index+batch_size,len(list_data))]
            batch_prompts.append(batch_prompt)
            index += batch_size
    
print("Number of batches:", len(batch_prompts))
print("Number of prompts in each batch:", [len(batch) for batch in batch_prompts])

filepath = "./diff_order_int_addition_responses.txt"

for _, batch_prompt in enumerate(batch_prompts):
    
    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you some addition questions. Please answer in the correct format. For example, if I ask 'What is 2 + 3?', you should answer '2 + 3 = 5'. Each question is in a separate line. Please return each answer in a separate line."},
            {"role" : "user", "content" : "".join([f"What is {a} + {b}\n" for (a, b, sum) in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    time.sleep(60//rpm) #to avoid rate limit errors
