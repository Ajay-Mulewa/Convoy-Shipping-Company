def range_sum(numbers, start, end):
    sum = 0
    for num in numbers:
        if num >= start and num <= end:
            sum += num
    return sum


input_numbers = [int(x) for x in input().split(' ')]
a, b = [int(x) for x in input().split(' ')]
print(range_sum(input_numbers, a, b))