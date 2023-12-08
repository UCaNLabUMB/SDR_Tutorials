
import sys
import random
import string

def generate_random_string(length):
    '''Generates a random string of the given length.'''
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def main(rows, total_chars_per_row, output_file):
    with open(output_file, 'w') as file:
        for row_num in range(1, rows + 1):
            # The last 5 characters are reserved for '0000n'
            random_string_length = total_chars_per_row - len('0000' + str(row_num))
            random_string = generate_random_string(random_string_length)
            final_string = random_string + '0000' + str(row_num)
            file.write(final_string + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <number_of_rows> <total_chars_per_row> <output_file>")
        sys.exit(1)

    rows = int(sys.argv[1])
    total_chars_per_row = int(sys.argv[2])
    output_file = sys.argv[3]

    main(rows, total_chars_per_row, output_file)
