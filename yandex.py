def check_win(board, row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        remem_r, remem_c = row, col
        while (row + dr, col + dc) in board[player]:
            row += dr
            col += dc
            count += 1

        row, col = remem_r, remem_c
        while (row - dr, col - dc) in board[player]:
            row -= dr
            col -= dc
            count += 1

        row, col = remem_r, remem_c

        if count >= 5:
            return True
    return False


n = int(input())
board = {'First': set(), 'Second': set()}
winner = None
lg = 0

for k in range(n):
    lg = k
    r, c = map(int, input().split())
    player = 'First' if k % 2 == 0 else 'Second'
    if check_win(board, r, c, player):
        winner = player
        break
    board[player].add((r, c))


if lg < n - 1:
    print("Inattention")
elif winner:
    print(winner)
else:
    print("Draw")
