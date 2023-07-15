import random
import numpy as np

c1 = 40  # consistency rating
p1 = 95  # power rating

rolls = []

for x in range(1000):
    roll = min(10, max(0, round(np.random.normal(
        min(p1 / 0.15, 10),  # power rating
        95 / c1  # increased scale factor for inverse consistency rating
        ))))

    rolls.append(roll)

print(f"Consistency: {c1}")
print(f"Power: {p1}")
print()

for i in range(11):
    print(f"{i}: {rolls.count(i)}")
