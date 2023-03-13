# YOUR CODE HERE

input_file = open('input.txt')
contents = input_file.read()
strings = contents.split('\n')

for s in strings:
    if 'xrj' in s:
        print(s)