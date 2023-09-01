import sys


def read_file(filename):
    A = []
    B = []
    S = {}

    with open(filename, 'r') as f:
        lines = f.readlines()

        for letter in lines[0].strip():
            A.append(letter)

        for letter in lines[1].strip():
            B.append(letter)

        B_keys = lines[2].strip().split()[1:]
        for i in range(3, 8):
            vals = lines[i].strip().split()
            A_key = vals.pop(0)
            S[A_key] = {}
            for v, key in zip(vals, B_keys):
                S[A_key][key] = int(v)

    return A, B, S


def create_matrix(A, B, S):
    A_len = len(A) + 1
    B_len = len(B) + 1
    M = [[] for i in range(A_len)]  # M[col][row]
    M[0].append(0)  # dead corner

    for i in range(1, A_len):  # '-' penalty for A
        M[i].append(M[i - 1][0] + S[A[i - 1]]['-'])

    for j in range(1, B_len):  # '-' penalty for B
        M[0].append(M[0][j - 1] + S['-'][B[j - 1]])

    return fill_matrix(A, B, S, A_len, B_len, M)


def fill_matrix(A, B, S, I, J, M):
    for i in range(1, I):
        for j in range(1, J):
            M[i].append(max(
                M[i - 1][j - 1] + S[A[i - 1]][B[j - 1]],  # do not add gap (gene match)
                M[i][j - 1] + S['-'][B[j - 1]],  # add '-' in B
                M[i - 1][j] + S[A[i - 1]]['-']  # add '-' in A
            ))
    return M


def get_alignments(A, B, S, M):
    A_len = len(A)
    B_len = len(B)
    new_A = ''
    new_B = ''
    score = str(M[A_len][B_len])

    while A_len != 0 and B_len != 0:
        A_gene = A[A_len - 1]
        B_gene = B[B_len - 1]

        if M[A_len][B_len] == M[A_len - 1][B_len - 1] + S[A_gene][B_gene]:
            # did not add gap
            new_A = A_gene + new_A
            new_B = B_gene + new_B
            A_len -= 1
            B_len -= 1
        elif M[A_len][B_len] == M[A_len][B_len - 1] + S['-'][B_gene]:
            # added '-' in A
            new_A = '-' + new_A
            new_B = B_gene + new_B
            B_len -= 1
        else:
            # added '-' in B
            new_A = A_gene + new_A
            new_B = '-' + new_B
            A_len -= 1

    # add last value (since all 3 directions WILL be the '-' score)
    while A_len != 0:
        new_A = A[A_len - 1] + new_A
        new_B = '-' + new_B
        A_len -= 1

    while B_len != 0:
        new_A = '-' + new_A
        new_B = B[B_len - 1] + new_B
        B_len -= 1

    print('x: ' + ' '.join([l for l in new_A]))
    print('y: ' + ' '.join([l for l in new_B]))
    print('Score: ' + score)


def main(argv):
    A, B, S = read_file(argv[1])
    M = create_matrix(A, B, S)
    get_alignments(A, B, S, M)


if __name__ == '__main__':
    main(sys.argv)
