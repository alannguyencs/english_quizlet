

def get_longest_common_child(X, Y):
    # find the length of the strings
    m, n = len(X), len(Y)

    # declaring the array for storing the dp values
    lcc_length = [[None for _ in range(n+1)] for _ in range(m + 1)]
    lcc_content = [[None for _ in range(n+1)] for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                lcc_length[i][j] = 0
                lcc_content[i][j] = ''

            elif X[i - 1] == Y[j - 1]:
                lcc_length[i][j] = lcc_length[i-1][j-1] + 1
                lcc_content[i][j] = lcc_content[i-1][j-1] + '|' + X[i - 1]

            elif lcc_length[i - 1][j] > lcc_length[i][j - 1]:
                lcc_length[i][j] = lcc_length[i-1][j]
                lcc_content[i][j] = lcc_content[i-1][j]

            else: #lcc_length[i - 1][j] < lcc_length[i][j - 1]:
                lcc_length[i][j] = lcc_length[i][j-1]
                lcc_content[i][j] = lcc_content[i][j-1]

    lcc_content_ = lcc_content[m][n][1:].split('|')
    return lcc_content_

def get_similarity_score(X, Y):
    lcc_content = get_longest_common_child(X, Y)
    similarity_score = 2 * len(lcc_content) / (len(X) + len(Y))
    return similarity_score