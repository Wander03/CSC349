import sys


def find_singleton(lst, min_i, max_i):
    mid_i = (max_i + min_i) // 2

    if min_i == max_i:
        return lst[mid_i]
    elif mid_i % 2 == 0:
        if lst[mid_i] == lst[mid_i + 1]:                            # even + next same -> left is good
            return find_singleton(lst, mid_i + 2, max_i)
        else:                                                       # even + diff -> left is bad
            return find_singleton(lst, min_i, mid_i)
    else:
        if lst[mid_i] == lst[mid_i - 1]:                            # odd + previous same -> left is good
            return find_singleton(lst, mid_i + 1, max_i)
        else:                                                       # odd + previous diff -> left is bad
            return find_singleton(lst, min_i, mid_i)


def main(argv):
    with open(argv[1], 'r') as f:
        lst = f.read().strip().split(sep=', ')

    if len(lst) == 0:
        print()
    else:
        print(find_singleton(lst, 0, len(lst) - 1))


if __name__ == '__main__':
    main(sys.argv)
