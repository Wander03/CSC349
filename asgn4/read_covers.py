# Reads vertex lists from a file.
# Christopher Siu (cesiu@calpoly.edu)
# Sol'n format checker, CSC 349 Asgn. 5, Fall '17

import sys


def main(argv):
    covers = read_covers(argv[1])
    print("log-Approximation: %s" % ' '.join([str(v) for v in covers[0]]))
    print("2-Approximation: %s" % ' '.join([str(v) for v in covers[1]]))
    print("Exact Solution: %s" % ' '.join([str(v) for v in covers[2]]))


# Reads vertex covers from a file.
# filename - The name of the file from which to read
# Returns a list of lists of vertex numbers.
def read_covers(filename):
    with open(filename, "r") as student_out:
        return [[int(vert) for vert in cover.split(':')[-1].strip().split()]
                           for cover in student_out.readlines()[:3]]


if __name__ == "__main__":
    main(sys.argv)
