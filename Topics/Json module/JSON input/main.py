import json


# write your code here
json_string = input()
json_data = json.loads(json_string)
print(type(json_data))
print(json_data)
