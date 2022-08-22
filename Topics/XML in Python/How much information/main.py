from lxml import etree

root = etree.fromstring(input())
print(len(root), len(root.attrib))
