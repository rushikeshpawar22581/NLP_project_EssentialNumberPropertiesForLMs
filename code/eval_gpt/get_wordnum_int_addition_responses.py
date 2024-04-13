import openai
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
rpm = 3

client = openai.Client(api_key=api_key)

with open("../../data/numeration_int_addn.json", "r") as f:
    data = json.load(f)

print(data)

batch_prompts = []

for sign_type in data:
    for num_type in data[sign_type]:
        for i, num_digit_code in enumerate(data[sign_type][num_type]):

            data_list = data[sign_type][num_type][num_digit_code]
            
            num_prompts = 2000 // (i+1)*5

            index = 0

            while(index < len(data_list)):
                batch_prompt = [f"What is {data_list[i][0]} + {data_list[i][1]}?" for i in range(index, min(index+num_prompts, len(data_list)))]
                batch_prompts.append(batch_prompt)
                index += num_prompts
            
print("Number of batches:", len(batch_prompts))
print("Number of prompts in each batch:", [len(batch) for batch in batch_prompts])

filepath = "./numeration_int_addn_responses_wf.txt"

for _, batch_prompt in enumerate(batch_prompts):
    
        print("Sending batch {} of {}".format(_+1, len(batch_prompts)))
    
        num_prompts = len(batch_prompt)
    
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
                [{"role": "user", "content": "You are a math assistant. I will ask you some addition questions. The two numbers I ask you to add can be in either digit form or word form, irrespective of the input form I want you to answer in word form. For example, if I ask 'What is 2 + three?', you should answer '2 + three = five'. Note that input format should be preserved in answer. Each question is in a separate line. Please return each answer in a separate line."},
                {"role" : "user", "content" : "".join([f"{prompt}\n" for prompt in batch_prompt])}])
    
        responses = response.choices[0].message.content.split("\n")
        #write to file
        with open(filepath, "a") as f:
            for response in responses:
                f.write(response + "\n")
        
        time.sleep(60//rpm) #to avoid rate limit errors

print("Responses written to file:", filepath)

print("Now sending prompts for digit form responses\n")
filepath_df = "./numeration_int_addn_responses_df.txt"

for _, batch_prompt in enumerate(batch_prompts):
        
    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you some addition questions. The two numbers I ask you to add can be in either digit form or word form, irrespective of the input form I want you to answer in digit form. For example, if I ask 'What is 2 + three?', you should answer '2 + three = 5'. Note that input format should be preserved in answer. Each question is in a separate line. Please return each answer in a separate line."},
            {"role" : "user", "content" : "".join([f"{prompt}\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath_df, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    time.sleep(60//rpm) #to avoid rate limit errors