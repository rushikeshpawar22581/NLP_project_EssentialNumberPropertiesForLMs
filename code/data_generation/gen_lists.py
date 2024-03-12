import json
import random
from copy import deepcopy

NUM_SAMPLES_PER_CATEGORY = 100


if __name__=="__main__":

    random.seed(42)

    lists_size_3_pos = []
    lists_size_5_pos = []
    lists_size_10_pos = []

    for max_num_digits in range(1, 6):

        range_ = 10**max_num_digits-1

        for _ in range(NUM_SAMPLES_PER_CATEGORY):
            
            list_ = [random.randint(0, range_) for _ in range(3)]
            lists_size_3_pos.append(list_[:])

            list_.extend([random.randint(0, range_) for _ in range(2)])
            lists_size_5_pos.append(list_[:])

            list_.extend([random.randint(0, range_) for _ in range(5)])
            lists_size_10_pos.append(list_[:])
    
    #now create negative lists
    lists_size_3_neg = deepcopy(lists_size_3_pos)
    lists_size_5_neg = deepcopy(lists_size_5_pos)
    lists_size_10_neg = deepcopy(lists_size_10_pos)

    #now randomly set some of the numbers to negative
    for lists in [lists_size_3_neg, lists_size_5_neg, lists_size_10_neg]:
        for list_ in lists:
            for i in range(len(list_)):
                if random.random() < 0.5:
                    list_[i] = -list_[i]
    
    #note that usage of numpy array was possible for this data generation, but it was not used, to keep the code consistent with the rest of the data generation scripts (since numpy does not support very large integers).
                    
    data = {"lists_size_3_pos": lists_size_3_pos, "lists_size_5_pos": lists_size_5_pos, "lists_size_10_pos": lists_size_10_pos, "lists_size_3_neg": lists_size_3_neg, "lists_size_5_neg": lists_size_5_neg, "lists_size_10_neg": lists_size_10_neg}

    with open("../../data/lists.json", "w") as f:
        json.dump(data, f)
    
    print("Data generated and saved to ../../data/lists.json")
