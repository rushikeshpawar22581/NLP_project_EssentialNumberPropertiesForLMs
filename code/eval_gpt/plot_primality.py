import matplotlib.pyplot as plt
import numpy as np
import json
import re
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def plot_cm_primality(y_true, y_pred, title, path):
    
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Composite", "Prime"])
    disp.plot()
    plt.title(title)
    plt.savefig(path)

def plot_acc_with_digits(responses_array, primes, composites, title, path):
    #responses_array is of the form [[num, response], [num, response], ...]
    #primes is a set of prime numbers
    #composites is a set of composite numbers

    #we will plot the accuracy of the model as a function of the number of digits in the number
    max_digits = max([len(str(num)) for num, _ in responses_array])

    correct = np.zeros((max_digits))
    total = np.zeros((max_digits))

    for response in responses_array:
        
        num = response[0]
        resp = response[1]

        if num not in primes and num not in composites: #model returned a response for a number that we did not even ask it to classify. So we will skip this.
            continue

        if num in primes and resp == 1:
            correct[len(str(num))-1] += 1
        
        elif num in composites and resp == 0:
            correct[len(str(num))-1] += 1
        
        total[len(str(num))-1] += 1
    
    acc = correct * 100/total

    #plot the figure
    plt.figure(figsize=(8, 6))
    plt.ylim(0, 110)
    plt.plot(range(1, max_digits+1), acc, marker="o")
    plt.xlabel("Number of digits")
    plt.ylabel("Accuracy (%)")
    plt.title(title)
    plt.xticks(range(1, max_digits+1))
    plt.grid()
    plt.savefig(path)

def plot_acc_vs_number(responses_array, primes, composites, title, path):
    #responses_array is of the form [[num, response], [num, response], ...]
    #primes is a set of prime numbers
    #composites is a set of composite numbers

    #we will plot the accuracy of the model as a function of the number of digits in the number
    max_num = max([num for num, _ in responses_array])

    correct = np.zeros((max_num))
    total = np.zeros((max_num))

    for response in responses_array:
        
        num = response[0]
        resp = response[1]

        if num not in primes and num not in composites: #model returned a response for a number that we did not even ask it to classify. So we will skip this.
            continue

        if num in primes and resp == 1:
            correct[num-1] += 1
        
        elif num in composites and resp == 0:
            correct[num-1] += 1
        
        total[num-1] += 1
    
    #only plot the numbers for which we have data
    #retain_indices = np.where(total > 0)[0]
    #correct = correct[retain_indices]
    #total = total[retain_indices]

    for i in range(0, len(total), 5000):
        #do a sum of total and correct for every 5000 numbers
        total_sum = np.sum(total[i:i+5000])
        correct_sum = np.sum(correct[i:i+5000])
        if total_sum == 0:
            continue

    #create 20 bins of equal size
    bins = np.linspace(0, 10**5, 21, dtype=int) #we have numbers upto 100000

    acc = np.zeros((20))

    for i in range(20):
        correct_sum = np.sum(correct[bins[i]:bins[i+1]])
        total_sum = np.sum(total[bins[i]:bins[i+1]])
        acc[i] = correct_sum * 100/total_sum
    
    #make a bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, 21), acc, tick_label=[f"{bins[i]}-{bins[i+1]}" for i in range(20)], color='orange')
    plt.xlabel("Number")
    plt.ylabel("Accuracy (%)")
    plt.title(title)
    plt.xticks(range(1, 21), rotation=45)
    plt.grid()
    plt.savefig(path)

    






if __name__ == "__main__":

    #read in the data
    with open("../../data/primality_test.json", "r") as f:
        data = json.load(f)

    primes = set(data["primes"])
    composites = set(data["composites"])

    #read in the responses when we had asked if the number is prime
    responses = []
    with open("./primality_responses_ask_if_prime.txt", "r") as f:
        for line in f:
            responses.append(line.strip())

    responses_array_prime = []

    for response in responses:
        #each response is of the format 54631:No
        num, resp = response.split(":")
        num = int(num)
        resp = resp.strip()
        if resp == "Yes":
            resp = 1
        else:
            resp = 0
        responses_array_prime.append([num, resp])

    responses_array_prime = np.array(responses_array_prime)

    y_true_prime = []
    y_pred_prime = []

    for response in responses_array_prime:
        num = response[0]

        if num in primes:
            y_true_prime.append(1)
            y_pred_prime.append(response[1])
        elif num in composites: #need to check for it as model may have returned a response for a number that we did not even ask it to classify.
            y_true_prime.append(0)
            y_pred_prime.append(response[1])

    #read in the responses when we had asked if the number is composite
    responses = []
    with open("./primality_responses_ask_if_composite.txt", "r") as f:
        for line in f:
            responses.append(line.strip())

    responses_array_composite = []

    for response in responses:
        #each response is of the format 54631:No
        num, resp = response.split(":")
        num = int(num)
        resp = resp.strip()
        if resp == "Yes":
            resp = 0
        else:
            resp = 1
        responses_array_composite.append([num, resp])

    responses_array_composite = np.array(responses_array_composite)

    y_true_composite = []
    y_pred_composite = []

    for response in responses_array_composite:
        num = response[0]

        if num in composites:
            y_true_composite.append(0)
            y_pred_composite.append(response[1])
        elif num in primes: #need to check for it as model may have returned a response for a number that we did not even ask it to classify.
            y_true_composite.append(1)
            y_pred_composite.append(response[1])

    plot_cm_primality(y_true_prime, y_pred_prime, "Confusion Matrix when asking if the number is prime", "./primality_plots/cm_prime.png")
    plot_cm_primality(y_true_composite, y_pred_composite, "Confusion Matrix when asking if the number is composite", "./primality_plots/cm_composite.png")
    #plot_acc_with_digits(responses_array_prime, primes, composites, "Accuracy as a function of number of digits when asking if the number is prime", "./primality_plots/acc_prime.png")
    #plot_acc_with_digits(responses_array_composite, primes, composites, "Accuracy as a function of number of digits when asking if the number is composite", "./primality_plots/acc_composite.png")
    plot_acc_vs_number(responses_array_prime, primes, composites, "Accuracy vs size of number when asking if the number is prime", "./primality_plots/acc_vs_num_prime.png")
    plot_acc_vs_number(responses_array_composite, primes, composites, "Accuracy vs size of number when asking if the number is composite", "./primality_plots/acc_vs_num_composite.png")

    #Now dealing with factor responses

    #read in the responses
    responses = []
    with open("./factor_responses.txt", "r") as f:
        for line in f:
            responses.append(line.strip())

    responses_array = [] # an array where each element is a list of the form [num, list_factors]

    for response in responses:

        #format 1. "Factors of 54631 are [1, 7, 7819, 54631]"

        match = re.match(r"Factors of (\d+) are \[(.*)\]", response)
        if match is None:
            continue
        num = int(match.group(1))
        try:
            factors = list(map(int, match.group(2).split(", ")))
        except:
            continue
        responses_array.append([num, factors])

    print("We obtained valid responses for ", len(responses_array), " numbers.")

    #decide if the number is prime or not using the factors
    y_true_factors = []
    y_pred_factors = []

    for response in responses_array:
        num = response[0]
        factors = response[1]

        if num in primes:
            y_true_factors.append(1)
        elif num in composites:
            y_true_factors.append(0)
        else:
            continue

        if len(factors) == 2 and 1 in factors and num in factors:
            y_pred_factors.append(1)
        
        else:
            y_pred_factors.append(0)
        
        if y_pred_factors[-1] != y_true_factors[-1]:
            print("Number:", num)
            print("Factors:", factors)
            print("True:", y_true_factors[-1])
            print("Predicted:", y_pred_factors[-1])
            print("\n\n")

    #count the toal number of primes and composites
    num_primes = 0
    num_composites = 0

    for response in responses_array:
        num = response[0]
        if num in primes:
            num_primes += 1
        elif num in composites:
            num_composites += 1

    print("True Number of primes:", num_primes)
    print("True Number of composites:", num_composites)

    #calc the number of primes and composites as predicted by the model
    num_primes_pred = np.sum(y_pred_factors)
    num_composites_pred = len(y_pred_factors) - num_primes_pred
        
    print("Predicted Number of primes:", num_primes_pred)
    print("Predicted Number of composites:", num_composites_pred)


    plot_cm_primality(y_true_factors, y_pred_factors, "Confusion Matrix when deducing primality from factors", "./primality_plots/cm_factors.png")

        
        






