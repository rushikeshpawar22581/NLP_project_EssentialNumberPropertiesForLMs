import matplotlib.pyplot as plt
import numpy as np
import json
import re
import seaborn as sns

MAX_DIGITS = 60

def plot_for_int_addition(responses_path):

    with open(responses_path, "r") as f:
        responses = f.readlines()
    
    #have to go through the responses manually and extract the numbers
    
    correct = np.zeros((3, MAX_DIGITS)) # 3 -> one for case when both numbers are positive, one for case when one number is negative, one for case when both numbers are negative
    total = np.zeros((3, MAX_DIGITS))

    triplets = []

    def is_correct(a, b, answer):
        return a+b == answer

    def get_num_digits(num):
        return len(str(num).replace("-", ""))
    
    #There are 6 formats in which the responses were received, even though the model was asked to follow a certain pattern. 
    #since these formats are non-overlapping, we can use 6 different regex patterns to extract the numbers from the responses, looping over all the responses.
    
    #format 1. Format is '[2, 2, 4] = 4'.
    for response in responses:
        match = re.search(r'\[([-+]?\d+), ([-+]?\d+), ([-+]?\d+)\] = ([-+]?\d+)', response)

        if match:
            a, b, c, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
    
    #format 2. Format is '[-17 + -81 = -98]'.
    for response in responses:
        match = re.search(r'(\[)?([-+]?\d+) \+ ([-+]?\d+) = ([-+]?\d+)(\])?', response)

        if match:
            a, b, answer = match.groups()[1: -1]
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
    
    #format 3. Format is '[2, 2, 4]'.
    for response in responses:
        match = re.search(r'\[([-+]?\d+), ([-+]?\d+), ([-+]?\d+)\]', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
    
    #1540 to 1563. 
    #format 4. Format is '2 - 4 = -2'.
    for response in responses:

        match = re.search(r'([-+]?\d+) \- ([-+]?\d+) = ([-+]?\d+)', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), -int(b), int(answer)
            triplets.append((a, b, answer))

    #format 5. format is '2106518290868 + (-5009410029817) = -2902891738949'.
    
    for response in responses:

        match = re.search(r'([-+]?\d+) \+ \(([-+]?\d+)\) = ([-+]?\d+)', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
    
    #format 6. format is '\[ -382080619849359354451962436565147864320463465990184530075 + 371914144627003178302099873114871577476724839546326059237 = -10166475222356176149862563450276286843738626443858470838 \]'.
    for response in responses:
        match = re.search(r'[\\]\[ ([-+]?\d+) \+ ([-+]?\d+) = ([-+]?\d+) [\\]\]', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
   

    for a, b, answer in triplets:

        num_digits = get_num_digits(a)

        if a >= 0 and b >= 0:
            correct[0, num_digits-1] += is_correct(a, b, answer)
            total[0, num_digits-1] += 1

        elif a < 0 and b < 0:
            correct[2, num_digits-1] += is_correct(a, b, answer)
            total[2, num_digits-1] += 1

        else:
            correct[1, num_digits-1] += is_correct(a, b, answer)
            total[1, num_digits-1] += 1

    
    #strike off the cases where total < 40
    strike_off = total < 40

    correct[strike_off] = 0
    total[strike_off] = 1

    accuracy = correct/total

    for i in range(3):

        plt.figure(figsize=(60, 5))
        accuracy_i = np.expand_dims(accuracy[i], axis=0)
        mask = np.expand_dims(strike_off[i], axis=0)
        sns.heatmap(accuracy_i, cmap = "Blues", annot=False, cbar=True, mask=mask, square=True, xticklabels=5, cbar_kws={"orientation": "horizontal"}, linewidths=1, linecolor='black', yticklabels=False)
        plt.title("Accuracy for integer addition when " + ["both numbers are positive", "one number is negative", "both numbers are negative"][i], fontsize=20)
        plt.xlabel("Number of digits in the numbers", fontsize=16)
        plt.xticks(np.arange(1, 61, 5), np.arange(1, 61, 5), fontsize=14)
        
        #cancel out the strike off cells
        for j in range(len(accuracy_i[0])):
            if mask[0][j]:
                plt.text(j + 0.5, 0.6, 'X', ha='center', va='center', color='black', fontsize=58)
                
        plt.savefig("./int_addition_plots/" + ["both_positive", "one_negative", "both_negative"][i] + ".png")


        







if __name__ == "__main__":
    plot_for_int_addition("./int_addition_responses.txt")
