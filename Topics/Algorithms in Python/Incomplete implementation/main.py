def startswith_capital_counter(names):
    counter = 0
    for name in names:
        # if name starts with capital letter and is not empty and is not a number increment counter
        if name[0].isupper():
            counter += 1

    return counter
