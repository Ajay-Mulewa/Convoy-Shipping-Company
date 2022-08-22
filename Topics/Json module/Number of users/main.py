
with open('users.json', 'r') as user_json:
    print(len(json.load(user_json)['users']))