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

        plt.figure(figsize=(60, 14 if i==2 else 5))
        accuracy_i = np.expand_dims(accuracy[i], axis=0)
        mask = np.expand_dims(strike_off[i], axis=0)
        sns.heatmap(accuracy_i, cmap = "Blues", annot=False, cbar=True if i==2 else False, mask=mask, square=True, xticklabels=5, cbar_kws={"orientation": "horizontal"}, linewidths=1, linecolor='black', yticklabels=False)
        #plt.title("Accuracy for integer addition when " + ["both numbers are positive", "one number is negative", "both numbers are negative"][i], fontsize=20)
        plt.xlabel("Number of digits in the numbers", fontsize=46)
        plt.xticks(np.arange(1, 61, 5), np.arange(1, 61, 5), fontsize=44)
        
        #cancel out the strike off cells
        for j in range(len(accuracy_i[0])):
            if mask[0][j]:
                plt.text(j + 0.5, 0.6, 'X', ha='center', va='center', color='black', fontsize=58)
                
        plt.savefig("./int_addition_plots/" + ["both_positive", "one_negative", "both_negative"][i] + ".png")


def plot_for_list_min(responses_path):

    with open(responses_path, "r") as f:
        responses = f.readlines()
    
    #all the responses are of the format 'Min([1, 2, 3]) = 1'
    
    #extract the lists and the minimum numbers
    lists = []
    min_numbers = []

    for response in responses:
        match = re.search(r'Min\((\[[^\]]+\])\) = ([+-]?\d+)', response)

        if match:
            list_, min_number = match.groups()
            list_ = json.loads(list_)
            min_number = int(min_number)
            lists.append(list_)
            min_numbers.append(min_number)

    
    max_num_digits = 5

    correct_size3 = np.zeros((2, max_num_digits))
    correct_size5 = np.zeros((2, max_num_digits))
    correct_size10 = np.zeros((2, max_num_digits))

    total_size3 = np.zeros((2, max_num_digits))
    total_size5 = np.zeros((2, max_num_digits))
    total_size10 = np.zeros((2, max_num_digits))

    def num_digits(list_):

        def get_num_digits(num):
            return len(str(num).replace("-", ""))
        
        return max(get_num_digits(num) for num in list_)

    for list_, min_number in zip(lists, min_numbers):

        list_size = len(list_)
        
        n_digits = num_digits(list_)

        is_neg = 1 if any(num < 0 for num in list_) else 0

        if list_size == 3:

            if min(list_) == min_number:
                correct_size3[is_neg, n_digits-1] += 1
            total_size3[is_neg, n_digits-1] += 1
        
        elif list_size == 5:

            if min(list_) == min_number:
                correct_size5[is_neg, n_digits-1] += 1
            total_size5[is_neg, n_digits-1] += 1
        
        else:

            if min(list_) == min_number:
                correct_size10[is_neg, n_digits-1] += 1
            total_size10[is_neg, n_digits-1] += 1
        

    accuracies_size3 = correct_size3/total_size3
    accuracies_size5 = correct_size5/total_size5
    accuracies_size10 = correct_size10/total_size10

    #plot how the accuracy varies with the number of digits in the numbers. draw two curves, one for when all the numbers are positive, and one for when at least one number is negative. Show the points through scatter plot.
    #separate plots for each list size.

    for size, accuracies in zip([3, 5, 10], [accuracies_size3, accuracies_size5, accuracies_size10]):

        plt.figure()
        x_range = np.arange(1, max_num_digits+1)
        plt.plot(x_range, accuracies[0], label="All numbers are positive")
        plt.scatter(x_range, accuracies[0])
        plt.plot(x_range, accuracies[1], label="At least one number is negative")
        plt.scatter(x_range, accuracies[1])

        plt.xlabel("Number of digits in the numbers")
        plt.ylabel("Accuracy")

        plt.ylim(0.9, 1.01)
        plt.xticks(x_range)
        plt.yticks(np.arange(0.9, 1.01, 0.02))
        plt.title("Accuracy for finding the minimum number in a list of size " + str(size))
        plt.legend()
        plt.grid()
        plt.savefig("./list_min_plots/size" + str(size) + ".png")


def plot_for_list_max(responses_path):
    
        with open(responses_path, "r") as f:
            responses = f.readlines()
        
        #all the responses are of the format 'Max([1, 2, 3]) = 3'
        
        #extract the lists and the maximum numbers
        lists = []
        max_numbers = []
    
        for response in responses:
            match = re.search(r'Max\((\[[^\]]+\])\) = ([+-]?\d+)', response)
    
            if match:
                list_, max_number = match.groups()
                list_ = json.loads(list_)
                max_number = int(max_number)
                lists.append(list_)
                max_numbers.append(max_number)

        max_num_digits = 5
    
        correct_size3 = np.zeros((2, max_num_digits))
        correct_size5 = np.zeros((2, max_num_digits))
        correct_size10 = np.zeros((2, max_num_digits))
    
        total_size3 = np.zeros((2, max_num_digits))
        total_size5 = np.zeros((2, max_num_digits))
        total_size10 = np.zeros((2, max_num_digits))
    
        def num_digits(list_):
    
            def get_num_digits(num):
                return len(str(num).replace("-", ""))
            
            return max(get_num_digits(num) for num in list_)
    
        for list_, max_number in zip(lists, max_numbers):
    
            list_size = len(list_)
            
            n_digits = num_digits(list_)
    
            is_neg = 1 if any(num < 0 for num in list_) else 0

            if list_size == 3:
                    
                if max(list_) == max_number:
                    correct_size3[is_neg, n_digits-1] += 1
                total_size3[is_neg, n_digits-1] += 1 

            elif list_size == 5:

                if max(list_) == max_number:
                    correct_size5[is_neg, n_digits - 1] += 1
                total_size5[is_neg, n_digits-1] += 1

            else:
                    
                if max(list_) == max_number:
                    correct_size10[is_neg, n_digits-1] += 1
                total_size10[is_neg, n_digits-1] += 1                                  
                
        
        accuracies_size3 = correct_size3/total_size3
        accuracies_size5 = correct_size5/total_size5
        accuracies_size10 = correct_size10/total_size10
    
        #plot how the accuracy varies with the number of digits in the numbers. draw two curves, one for when all the numbers are positive, and one for when at least one number is negative. Show the points through scatter plot.
        #separate plots for each list size.

        for size, accuracies in zip([3, 5, 10], [accuracies_size3, accuracies_size5, accuracies_size10]):

            plt.figure()
            x_range = np.arange(1, max_num_digits+1)
            plt.plot(x_range, accuracies[0], label="All numbers are positive")
            plt.scatter(x_range, accuracies[0])
            plt.plot(x_range, accuracies[1], label="At least one number is negative")
            plt.scatter(x_range, accuracies[1])

            plt.xlabel("Number of digits in the numbers")
            plt.ylim(0.9, 1.01)
            plt.xticks(x_range)
            plt.yticks(np.arange(0.9, 1.01, 0.02))
            plt.ylabel("Accuracy")
            plt.title("Accuracy for finding the maximum number in a list of size " + str(size))
            plt.legend()
            plt.grid()
            plt.savefig("./list_max_plots/size" + str(size) + ".png")
    

def plot_for_list_sort(responses_path):

    #format is [0, 1, 4]

    with open(responses_path, "r") as f:
        responses = f.readlines()
    
    #extract the lists and the sorted lists
    sorted_lists = []

    def check_sorted(list_):
        return all(list_[i] <= list_[i+1] for i in range(len(list_)-1))

    for response in responses:
        
        #each line is [0, 1, 4
        #we can directly convert to list

        #check if response follows the format of a list. if not, we continue.
        if not response.startswith("[") or not response.endswith("]\n"):
            continue

        sorted_list = json.loads(response)
        sorted_lists.append(sorted_list)



    max_num_digits = 5

    def num_digits(list_):
    
        def get_num_digits(num):
            return len(str(num).replace("-", ""))
        
        return max(get_num_digits(num) for num in list_)

    correct_size_3 = np.zeros((2, max_num_digits)) # 2 -> one for case when all the numbers are positive, one for case when at least one number is negative
    correct_size_5 = np.zeros((2, max_num_digits))
    correct_size_10 = np.zeros((2, max_num_digits))

    total_size_3 = np.zeros((2, max_num_digits))
    total_size_5 = np.zeros((2, max_num_digits))
    total_size_10 = np.zeros((2, max_num_digits))

    for index, list_ in enumerate(sorted_lists):
            
        list_size = len(list_)
        
        n_digits = min(num_digits(list_), 5) #responses may contain lists with numbers having more than 5 digits. These responses are simply incorrect since no list had such numbers.

        is_neg = 1 if any(num < 0 for num in list_) else 0

        if list_size == 3:

            if check_sorted(list_):
                correct_size_3[is_neg, n_digits-1] += 1
            total_size_3[is_neg, n_digits-1] += 1
        
        elif list_size == 5:

            if check_sorted(list_):
                correct_size_5[is_neg, n_digits-1] += 1
            total_size_5[is_neg, n_digits-1] += 1
        
        else:

            if check_sorted(list_):
                correct_size_10[is_neg, n_digits-1] += 1
            total_size_10[is_neg, n_digits-1] += 1
            

    accuracies_size_3 = correct_size_3/total_size_3
    accuracies_size_5 = correct_size_5/total_size_5
    accuracies_size_10 = correct_size_10/total_size_10

    #plot how the accuracy varies with the number of digits in the numbers. draw two curves, one for when all the numbers are positive, and one for when at least one number is negative. Show the points through scatter plot.
    #separate plots for each list size.

    for size, accuracies in zip([3, 5, 10], [accuracies_size_3, accuracies_size_5, accuracies_size_10]):
            
        plt.figure()
        x_range = np.arange(1, max_num_digits+1)
        plt.plot(x_range, accuracies[0], label="All numbers are positive")
        plt.scatter(x_range, accuracies[0])
        plt.plot(x_range, accuracies[1], label="At least one number is negative")
        plt.scatter(x_range, accuracies[1])

        plt.xlabel("Number of digits in the numbers")
        plt.ylabel("Accuracy")
        plt.xticks(x_range)
        plt.title("Accuracy for sorting a list of size " + str(size))
        plt.legend()
        plt.grid()
        plt.savefig("./list_sort_plots/size" + str(size) + ".png")



if __name__ == "__main__":
    plot_for_int_addition("./int_addition_responses.txt")
    plot_for_list_min("./list_min_responses.txt")
    plot_for_list_max("./list_max_responses.txt")
    plot_for_list_sort("./list_sort_responses.txt")
