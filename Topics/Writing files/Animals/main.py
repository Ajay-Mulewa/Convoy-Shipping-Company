# read animals.txt
# and write animals_new.txt
r_file = open('animals.txt', 'r')
w_file = open('animals_new.txt', 'w')
for animal in r_file.readlines():
    w_file.write(animal.replace('\n', ' '))

r_file.close()
w_file.close()
