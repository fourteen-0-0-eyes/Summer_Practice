def calculate_trees(stakes_height, stakes_count, trees_height):
    from math import ceil
    stakes_from_tree = trees_height // stakes_height
    return ceil(stakes_count / stakes_from_tree)


if __name__ == '__main__':
    with open('INPUT.txt', 'r') as file_input:
        data = [int(i) for i in file_input.read().split('\n')]

    if 1 <= data[0] <= data[2] <= 100 and 1 <= data[1] <= 100:
        with open('OUTPUT.txt', 'w') as file_output:
            file_output.write(str(calculate_trees(data[0], data[1], data[2])))
    else:
        print("Incorrect input")
