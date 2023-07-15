import random
import numpy as np

rating0 = 95
rating1 = 80
rating2 = 60
rating3 = 40

rolls0 = []
rolls1 = []
rolls2 = []
rolls3 = []


for y in range(60):
    for x in range(2):
        roll = min(10,round(abs(np.random.normal(0,rating0*(rating0/100)))))
        rolls0.append(roll)


for y in range(60):
    for x in range(2):
        roll = min(10,round(abs(np.random.normal(0,rating1*(rating1/100)))))
        rolls1.append(roll)


for y in range(60):
    for x in range(2):
        roll = min(10,round(abs(np.random.normal(0,rating2*(rating2/100)))))
        rolls2.append(roll)


for y in range(60):
    for x in range(2):
        roll = min(10,round(abs(np.random.normal(0,rating3*(rating3/100)))))
        rolls3.append(roll)




print()
print(rating0)
print()
print(sum(rolls0))
print(f"X: {rolls0.count(10)} - {len(rolls0)} ({round(rolls0.count(10)/len(rolls0),3)})")
print(f"0: {rolls0.count(0)} - {len(rolls0)} ({round(rolls0.count(0)/len(rolls0),3)})")
print(f"1: {rolls0.count(1)} - {len(rolls0)} ({round(rolls0.count(1)/len(rolls0),3)})")
print()
print(rating1)
print()
print(sum(rolls1))
print(f"X: {rolls1.count(10)} - {len(rolls1)} ({round(rolls1.count(10)/len(rolls1),3)})")
print(f"0: {rolls1.count(0)} - {len(rolls1)} ({round(rolls1.count(0)/len(rolls1),3)})")
print(f"1: {rolls1.count(1)} - {len(rolls1)} ({round(rolls1.count(1)/len(rolls1),3)})")
print()
print(rating2)
print()
print(sum(rolls2))
print(f"X: {rolls2.count(10)} - {len(rolls2)} ({round(rolls2.count(10)/len(rolls2),3)})")
print(f"0: {rolls2.count(0)} - {len(rolls2)} ({round(rolls2.count(0)/len(rolls2),3)})")
print(f"1: {rolls2.count(1)} - {len(rolls2)} ({round(rolls2.count(1)/len(rolls2),3)})")
print()
print(rating3)
print()
print(sum(rolls3))
print(f"X: {rolls3.count(10)} - {len(rolls3)} ({round(rolls3.count(10)/len(rolls3),3)})")
print(f"0: {rolls3.count(0)} - {len(rolls3)} ({round(rolls3.count(0)/len(rolls3),3)})")
print(f"1: {rolls3.count(1)} - {len(rolls3)} ({round(rolls3.count(1)/len(rolls3),3)})")
print()