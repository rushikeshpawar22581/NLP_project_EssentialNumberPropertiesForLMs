import matplotlib.pyplot as plt
import numpy as np
import json
import re
import seaborn as sns
from utils import edit_distance_integers

MAX_DIGITS = 60

def plot_for_int_addition(responses_path1, responses_path2):

    responses = []

    with open(responses_path1, "r") as f:
        responses = f.readlines()

    responses1 = []

    with open(responses_path2, "r") as f:
        responses1 = f.readlines()

    
    #have to go through the responses manually and extract the numbers
    
    correct = np.zeros((3, MAX_DIGITS)) # 3 -> one for case when both numbers are positive, one for case when one number is negative, one for case when both numbers are negative
    total = np.zeros((3, MAX_DIGITS))

    triplets = []

    def is_correct(a, b, answer):
        return a+b == answer

    def get_num_digits(num):
        return len(str(num).replace("-", ""))
    
    #for first run (responses in int_addition_responses.txt)
    #There are 6 formats in which the responses were received, even though the model was asked to follow a certain pattern. 
    #since these formats are non-overlapping, we can use 6 different regex patterns to extract the numbers from the responses, looping over all the responses.

    for response in responses:

        #format 1. Format is '[2, 2, 4] = 4'.
        match = re.search(r'\[([-+]?\d+), ([-+]?\d+), ([-+]?\d+)\] = ([-+]?\d+)', response)

        if match:
            a, b, c, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue
        
        #format 3. Format is '[2, 2, 4]'.
        match = re.search(r'\[([-+]?\d+), ([-+]?\d+), ([-+]?\d+)\]', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue

        #format 6. format is '\[ -382080619849359354451962436565147864320463465990184530075 + 371914144627003178302099873114871577476724839546326059237 = -10166475222356176149862563450276286843738626443858470838 \]'.
        match = re.search(r'[\\]\[ ([-+]?\d+) \+ ([-+]?\d+) = ([-+]?\d+) [\\]\]', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            
        #format 5. format is '2106518290868 + (-5009410029817) = -2902891738949'.
        match = re.search(r'([-+]?\d+) \+ \(([-+]?\d+)\) = ([-+]?\d+)', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue

        #format 4. Format is '2 - 4 = -2'.
        match = re.search(r'([-+]?\d+) \- ([-+]?\d+) = ([-+]?\d+)', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), -int(b), int(answer)
            triplets.append((a, b, answer))
            continue

        #format 2. Format is '[-17 + -81 = -98]' or -17 + 81 = -98.
        match = re.search(r'(\[)?([-+]?\d+) \+ ([-+]?\d+) = ([-+]?\d+)(\])?', response)

        if match:
            a, b, answer = match.groups()[1: -1]
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))

    
    #for second run (responses in int_addition_responses1.txt)
    
    for response in responses1:

        #follow format 7. format is '-160666855963254480065007 + -292265345502247650599465 + -452932201465502130664472 = -905863402930004261268944'.
        match = re.search(r'([-+]?\d+) \+ ([-+]?\d+) \+ ([-+]?\d+) = ([-+]?\d+)', response)

        if match:
            a, b, answer, _ = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            #triplets.append((a, b, answer))
            #there is too much inconsistency in these responses. Sometimes in "a + b + c = d", a + b = c. Sometimes, it is a + b + c = d. So, we will not consider these responses.
            continue
        
        #follow format 1. Format is '[2, 2, 4] = 8'.
        match = re.search(r'\[([-+]?\d+), ([-+]?\d+), ([-+]?\d+)\] = ([-+]?\d+)', response)

        if match:
            a, b, answer, _ = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue

        #follow format 3. Format is '[2, 2, 4]'.
        match = re.search(r'\[([-+]?\d+), ([-+]?\d+), ([-+]?\d+)\]', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue

        #format 6. format is '\[-382080619849359354451962436565147864320463465990184530075 + 371914144627003178302099873114871577476724839546326059237 = -10166475222356176149862563450276286843738626443858470838\]'.
        match = re.search(r'[\\]\[([-+]?\d+) \+ ([-+]?\d+) = ([-+]?\d+)[\\]\]', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue

        #format 5. format is '2106518290868 + (-5009410029817) = -2902891738949'.
        match = re.search(r'([-+]?\d+) \+ \(([-+]?\d+)\) = ([-+]?\d+)', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue
        
        #format 4. Format is '2 - 4 = -2'.
        match = re.search(r'([-+]?\d+) \- ([-+]?\d+) = ([-+]?\d+)', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), -int(b), int(answer)
            triplets.append((a, b, answer))
            continue
        
        #format 2. Format is '[-17 + -81 = -98]' or -17 + 81 = -98.
        match = re.search(r'([-+]?\d+) \+ ([-+]?\d+) = ([-+]?\d+)', response)

        if match:
            a, b, answer = match.groups()
            a, b, answer = int(a), int(b), int(answer)
            triplets.append((a, b, answer))
            continue


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

    accuracy = correct*100/total

    """
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
                
        plt.savefig("./int_addition_plots/" + ["both_positive", "one_negative", "both_negative"][i] + ".png")"""
    
    #make a simple plot, include all the three cases. Only include those data points where total >= 40.
    plt.figure()
    #both_positive_x_vals is a list of x values where total >= 40 for the case when both numbers are positive
    both_positive_x_vals = np.where(total[0] >= 40)[0] + 1
    both_positive_y_vals = accuracy[0][total[0] >= 40]
    #plt.plot(both_positive_x_vals, both_positive_y_vals, label="Both positive", color="green")
    #plt.scatter(both_positive_x_vals, both_positive_y_vals, color="green")

    #one_negative_x_vals is a list of x values where total >= 40 for the case when one number is negative
    one_negative_x_vals = np.where(total[1] >= 40)[0] + 1
    one_negative_y_vals = accuracy[1][total[1] >= 40]
    #plt.plot(one_negative_x_vals, one_negative_y_vals, label="One positive, one negative", color="blue")
    #plt.scatter(one_negative_x_vals, one_negative_y_vals, color="blue")

    #both_negative_x_vals is a list of x values where total >= 40 for the case when both numbers are negative
    both_negative_x_vals = np.where(total[2] >= 40)[0] + 1
    both_negative_y_vals = accuracy[2][total[2] >= 40]
    #plt.plot(both_negative_x_vals, both_negative_y_vals, label="Both negative", color="red")
    #plt.scatter(both_negative_x_vals, both_negative_y_vals, color="red")

    def moving_average(a, n=3):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    # Apply moving average to y values
    both_positive_y_vals_smooth = moving_average(both_positive_y_vals, 2)
    one_negative_y_vals_smooth = moving_average(one_negative_y_vals, 2)
    both_negative_y_vals_smooth = moving_average(both_negative_y_vals, 2)

    # Adjust x values to match the length of the smoothed y values
    both_positive_x_vals = both_positive_x_vals[:len(both_positive_y_vals_smooth)]
    one_negative_x_vals = one_negative_x_vals[:len(one_negative_y_vals_smooth)]
    both_negative_x_vals = both_negative_x_vals[:len(both_negative_y_vals_smooth)]

    plt.plot(both_positive_x_vals, both_positive_y_vals_smooth, label="Both positive", color="green")
    plt.plot(one_negative_x_vals, one_negative_y_vals_smooth, label="One positive, one negative", color="blue")
    plt.plot(both_negative_x_vals, both_negative_y_vals_smooth, label="Both negative", color="red")

    plt.xticks(np.arange(0, 61, 5))
    plt.yticks(np.arange(0, 101, 20))
    plt.title("GPT-3.5 Turbo: Accuracy for integer addition")
    plt.grid()

    plt.xlabel('Number of digits')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.savefig("./int_addition_plots/accuracy_vs_digits.png")

    #now calc soft accuracy (= length of correct answer including '-' sign if present - edit distance between correct answer and predicted answer / length of correct ans) for each case
    #soft accuracy = 1 - edit distance / length of correct answer

    soft_correct_totals = np.zeros((3, MAX_DIGITS))

    for a, b, answer in triplets:
            
        num_digits = get_num_digits(a)

        if a >= 0 and b >= 0:
            correct_answer = str(a + b)
            soft_correct_totals[0, num_digits-1] += 1 - edit_distance_integers(a + b, answer)/len(correct_answer)

        elif a < 0 and b < 0:
            correct_answer = str(a + b)
            soft_correct_totals[2, num_digits-1] += 1 - edit_distance_integers(a + b, answer)/len(correct_answer)

        else:
            correct_answer = str(a + b)
            soft_correct_totals[1, num_digits-1] += 1 - edit_distance_integers(a + b, answer)/len(correct_answer)
    
    #calculate soft accuracy
    soft_accuracy = soft_correct_totals*100/total
    #plot the soft accuracies  but only use data points where the total > 40
    plt.figure()
    #both_positive_x_vals is a list of x values where total >= 40 for the case when both numbers are positive
    both_positive_x_vals = np.where(total[0] >= 40)[0] + 1
    both_positive_y_vals = soft_accuracy[0][total[0] >= 40]
    #plt.plot(both_positive_x_vals, both_positive_y_vals, label="Both positive", color="green")
    #plt.scatter(both_positive_x_vals, both_positive_y_vals, color="green")

    #one_negative_x_vals is a list of x values where total >= 40 for the case when one number is negative
    one_negative_x_vals = np.where(total[1] >= 40)[0] + 1
    one_negative_y_vals = soft_accuracy[1][total[1] >= 40]

    #plt.plot(one_negative_x_vals, one_negative_y_vals, label="One positive, one negative", color="blue")
    #plt.scatter(one_negative_x_vals, one_negative_y_vals, color="blue")

    #both_negative_x_vals is a list of x values where total >= 40 for the case when both numbers are negative
    both_negative_x_vals = np.where(total[2] >= 40)[0] + 1
    both_negative_y_vals = soft_accuracy[2][total[2] >= 40]
    #plt.plot(both_negative_x_vals, both_negative_y_vals, label="Both negative", color="red")
    #plt.scatter(both_negative_x_vals, both_negative_y_vals, color="red")

    # Apply moving average to y values
    both_positive_y_vals_smooth = moving_average(both_positive_y_vals, 2)
    one_negative_y_vals_smooth = moving_average(one_negative_y_vals, 2)
    both_negative_y_vals_smooth = moving_average(both_negative_y_vals, 2)

    # Adjust x values to match the length of the smoothed y values
    both_positive_x_vals = both_positive_x_vals[:len(both_positive_y_vals_smooth)]
    one_negative_x_vals = one_negative_x_vals[:len(one_negative_y_vals_smooth)]
    both_negative_x_vals = both_negative_x_vals[:len(both_negative_y_vals_smooth)]

    plt.plot(both_positive_x_vals, both_positive_y_vals_smooth, label="Both positive", color="green")
    plt.plot(one_negative_x_vals, one_negative_y_vals_smooth, label="One positive, one negative", color="blue")
    plt.plot(both_negative_x_vals, both_negative_y_vals_smooth, label="Both negative", color="red")

    plt.xticks(np.arange(0, 61, 5))
    plt.yticks(np.arange(0, 101, 20))
    plt.title("GPT-3.5 Turbo: Soft accuracy for integer addition")
    plt.grid()

    plt.xlabel('Number of digits')
    plt.ylabel('Soft accuracy (%)')
    plt.legend()
    plt.savefig("./int_addition_plots/soft_accuracy_vs_digits.png")


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
        

    accuracies_size3 = correct_size3*100/total_size3
    accuracies_size5 = correct_size5*100/total_size5
    accuracies_size10 = correct_size10*100/total_size10

    #plot how the accuracy varies with the number of digits in the numbers. draw two curves, one for when all the numbers are positive, and one for when at least one number is negative. Show the points through scatter plot.
    #separate plots for each list size.

    for size, accuracies in zip([3, 5, 10], [accuracies_size3, accuracies_size5, accuracies_size10]):

        plt.figure()
        x_range = np.arange(1, max_num_digits+1)
        plt.plot(x_range, accuracies[0], label="All numbers are positive", linestyle=":", marker="+", color="green")
        plt.scatter(x_range, accuracies[0])
        plt.plot(x_range, accuracies[1], label="At least one number is negative", linestyle="--", marker="*", color="red")
        plt.scatter(x_range, accuracies[1])

        plt.xlabel("Number of digits in the numbers")
        plt.ylabel("Accuracy (%)")

        plt.ylim(90, 101)
        plt.xticks(x_range)
        plt.yticks(np.arange(90, 101, 2))
        plt.title("GPT-3.5 Turbo: Finding the minimum number in a list of size " + str(size))
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
                
        
        accuracies_size3 = correct_size3*100/total_size3
        accuracies_size5 = correct_size5*100/total_size5
        accuracies_size10 = correct_size10*100/total_size10
    
        #plot how the accuracy varies with the number of digits in the numbers. draw two curves, one for when all the numbers are positive, and one for when at least one number is negative. Show the points through scatter plot.
        #separate plots for each list size.

        for size, accuracies in zip([3, 5, 10], [accuracies_size3, accuracies_size5, accuracies_size10]):

            plt.figure()
            x_range = np.arange(1, max_num_digits+1)
            plt.plot(x_range, accuracies[0], label="All positive", color="green", marker="+", linestyle=":")
            plt.scatter(x_range, accuracies[0], color="green")
            plt.plot(x_range, accuracies[1], label="At least one negative", color="red", linestyle="--", marker="*")
            plt.scatter(x_range, accuracies[1], color="red")

            plt.xlabel("Number of digits in the numbers")
            plt.ylim(90, 101)
            plt.xticks(x_range)
            plt.yticks(np.arange(90, 101, 2))
            plt.ylabel("Accuracy (%)")
            plt.title("GPT-3.5 Turbo: Finding the maximum number in a list of size " + str(size))
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
            

    accuracies_size_3 = correct_size_3*100/total_size_3
    accuracies_size_5 = correct_size_5*100/total_size_5
    accuracies_size_10 = correct_size_10*100/total_size_10

    #plot how the accuracy varies with the number of digits in the numbers. draw two curves, one for when all the numbers are positive, and one for when at least one number is negative. Show the points through scatter plot.
    #separate plots for each list size.

    for size, accuracies in zip([3, 5, 10], [accuracies_size_3, accuracies_size_5, accuracies_size_10]):
            
        plt.figure()
        x_range = np.arange(1, max_num_digits+1)
        plt.plot(x_range, accuracies[0], label="All numbers are positive", color="green", linestyle=":", marker="+")
        plt.scatter(x_range, accuracies[0], color="green")
        plt.plot(x_range, accuracies[1], label="At least one number is negative", color="red", linestyle="--", marker="*")
        plt.scatter(x_range, accuracies[1], color="red")

        plt.xlabel("Number of digits in the numbers")
        plt.ylabel("Accuracy (%)")
        plt.xticks(x_range)
        plt.title("GPT-3.5 Turbo: Accuracy for sorting a list of size " + str(size))
        plt.legend()
        plt.grid()
        plt.savefig("./list_sort_plots/size" + str(size) + ".png")



if __name__ == "__main__":
    plot_for_int_addition("./int_addition_responses.txt", "./int_addition_responses1.txt")
    plot_for_list_min("./list_min_responses.txt")
    plot_for_list_max("./list_max_responses.txt")
    plot_for_list_sort("./list_sort_responses.txt")
