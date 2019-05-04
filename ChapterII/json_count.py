import json

with open('sample') as file:
    collection = json.loads(file.read())
counter = 0


def recurence_serch(elements):
    global counter
    for element in elements:
        if isinstance(element, dict):
            recurence_serch(element.values())
        if isinstance(element, list):
            recurence_serch(element)
        if isinstance(element, int):
            counter += element


recurence_serch(collection.values())
print(f'value of all numbers is {counter}')
