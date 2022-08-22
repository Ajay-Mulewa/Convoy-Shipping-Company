for i in range(1, 11):
    with open(f'file{str(i)}.txt', 'w') as file:
        file.write(str(i))

