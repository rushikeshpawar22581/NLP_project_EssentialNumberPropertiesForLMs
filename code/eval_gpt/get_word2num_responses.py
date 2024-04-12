import openai
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
rpm = 3

client = openai.Client(api_key=api_key)

#load in the lists
with open("../../data/numeration_word2num.json", "r") as f:
    data = json.load(f)


batch_prompts = []

for type in data:
    for i, num_digit_code in enumerate(data[type]):

        numbers_word_form = data[type][num_digit_code]
        num_prompts = 2000 // (i+1) # 2000 divided by number of digits in the number
        index = 0

        #this is unncessary for the current size of the dataset (we can make 1 batch with all the data for a particular combination of type and num_digit_code) but is useful if the dataset is expanded.

        while(index < len(numbers_word_form)):
            batch_prompt = [f"What is {numbers_word_form[i]}?" for i in range(index, min(index+num_prompts, len(numbers_word_form)))]
            batch_prompts.append(batch_prompt)
            index += num_prompts

print("Number of batches:", len(batch_prompts))
print("Number of prompts in each batch:", [len(batch) for batch in batch_prompts])

filepath = "./numeration_word2num_responses.txt"

for _, batch_prompt in enumerate(batch_prompts):

    print("Sending batch {} of {}".format(_+1, len(batch_prompts)))

    num_prompts = len(batch_prompt)

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=
            [{"role": "user", "content": "You are a math assistant. I will ask you to find number from its word representation. Please answer in the correct format. For example, if I ask 'What is thirty-three?' , you should answer 'thirty-three = 33'. Each question is in a separate line. Please return each answer in a separate line."},
            {"role" : "user", "content" : "".join([f"{prompt}\n" for prompt in batch_prompt])}])

    responses = response.choices[0].message.content.split("\n")
    #write to file
    with open(filepath, "a") as f:
        for response in responses:
            f.write(response + "\n")
    
    time.sleep(60//rpm) #to avoid rate limit errors


print("Responses written to file:", filepath)

