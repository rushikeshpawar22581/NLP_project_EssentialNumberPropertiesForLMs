import json
import random

#Generate all primes < 100000
primes = []
composites = []
buckets = [0 for _ in range(10)]

for i in range(2, 100000):
    is_prime = True
    for j in range(2, i):
        if i % j == 0:
            is_prime = False
            break
    if is_prime:
        primes.append(i)
        buckets[i//10000] += 1
    else:
        composites.append(i)

#sample 5000 primes from the list
primes = random.sample(primes, 5000)

#sample 5000 composites from the list
composites = random.sample(composites, 5000)

data = {}
data["primes"] = primes
data["composites"] = composites

with open("../../data/primality_test.json", "w") as f:
    json.dump(data, f)

#print(len(primes))
#print(buckets)