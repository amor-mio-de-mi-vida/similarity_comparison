import json

with open('output.json') as f:
    x = json.load(f)

# print(type(x))  # Output: dict
# print(x.keys())

# print(type(x['frames']))

print(x['frames'][0]['points'])