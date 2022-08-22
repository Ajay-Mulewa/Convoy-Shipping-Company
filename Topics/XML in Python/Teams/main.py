#  write your code here
from lxml import etree


root = etree.parse('C:\\Users\\psc\\PycharmProjects\\Convoy Shipping Company1\\Topics\XML in Python\\Teams\\data\\dataset\\input.txt').getroot()

members = root[0]

for member in members:
    print(member.get('name'), end=' ')
