import json
import random

MAX_DIGITS = 60

def gen_num_n_digit(n):
    return random.randrange(10**(n-1), 10**n)

if __name__ == "__main__":

    random.seed(42)
    #store the data in a json file
    filepath_int = "../../data/int_addition.json"
    filepath_decimal = "../../data/decimal_addition.json"

    data_int = []
    data_decimal = []
    
    for num_digits in range(1, MAX_DIGITS+1):
        #both positive
        for _ in range(100):
            a = gen_num_n_digit(num_digits)
            b = gen_num_n_digit(num_digits)
            c = a + b
            data_int.append([a, b, c])

            #choose a random number of decimal places
            decimal_places = random.randint(1, 10)
            a = a/(10**decimal_places)
            b = b/(10**decimal_places)
            c = a + b
            data_decimal.append([a, b, c])
        
        #second one negative
        for _ in range(100):
            a = gen_num_n_digit(num_digits)
            b = -gen_num_n_digit(num_digits)
            c = a + b
            data_int.append([a, b, c])

            decimal_places = random.randint(1, 10)
            a = a/(10**decimal_places)
            b = b/(10**decimal_places)
            c = a + b
            data_decimal.append([a, b, c])

        
        #first one negative
        for _ in range(100):
            a = -gen_num_n_digit(num_digits)
            b = gen_num_n_digit(num_digits)
            c = a + b
            data_int.append([a, b, c])

            decimal_places = random.randint(1, 10)
            a = a/(10**decimal_places)
            b = b/(10**decimal_places)
            c = a + b
            data_decimal.append([a, b, c])
        
        #both negative
        for _ in range(100):
            a = -gen_num_n_digit(num_digits)
            b = -gen_num_n_digit(num_digits)
            c = a + b
            data_int.append([a, b, c])

            decimal_places = random.randint(1, 10)
            a = a/(10**decimal_places)
            b = b/(10**decimal_places)
            c = a + b
            data_decimal.append([a, b, c])


    with open(filepath_int, "w") as f:
        json.dump(data_int, f)
    
    with open(filepath_decimal, "w") as f:
        json.dump(data_decimal, f)
    
    print("Integer addition data generated and stored in", filepath_int)
    print("Decimal addition data generated and stored in", filepath_decimal)