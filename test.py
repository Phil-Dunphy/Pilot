import random

pointers_bereinigt = [5, 5, 5, 2, 6, 5, 4, 6, 8]

elements = list(range(9))
random.shuffle(elements)
print("Neue Reihenfolge:", elements)

korrekte_values = [pointers_bereinigt[i] for i in elements if i <= 3]
print("Werte der ursprünglichen ersten 4 in neuer Reihenfolge:", korrekte_values)