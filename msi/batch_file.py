


def read_batchfile(filename):
    with open(filename, "r") as input:
        lines = input.readlines()
        print("batch length = " + str(len(lines)))
        return lines