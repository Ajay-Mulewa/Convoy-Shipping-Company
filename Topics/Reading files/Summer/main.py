data_set = open('.\hyperskill-dataset-66681789.txt', 'r')
counter = 0
word = 'summer\n'
for data in data_set:
    if data == word:
        counter += 1

print(counter)
