from functools import cache

def part_1(start_1: int, start_2: int):
    positions = [start_1, start_2]
    scores = [0, 0]
    current_die = 1

    n_rolls = 0
    while True:
        for player in range(2):
            step = 0
            for _ in range(3):
                n_rolls += 1
                step += current_die
                if current_die == 100:
                    current_die = 1
                else:
                    current_die += 1

            new_position = positions[player] + step
            new_position = 1 + ((new_position - 1) % 10)
            positions[player] = new_position
            scores[player] += new_position

            if scores[player] >= 1000:
                return min(scores) * n_rolls


@cache
def n_wins(start_1: int, start_2: int, score_1: int, score_2: int, one_to_move: bool, winning_score:int):
    total_one_wins = 0
    total_two_wins = 0

    if one_to_move:
        for roll in (3, 4, 5, 4, 5, 6, 5, 6, 7, 4, 5, 6, 5, 6, 7, 6, 7, 8, 5, 6, 7, 6, 7, 8, 7, 8, 9):
            new_position = start_1 + roll
            new_position = 1 + ((new_position - 1) % 10)
            new_score_1 = score_1 + new_position

            if new_score_1 >= winning_score:
                total_one_wins += 1
            else:
                one_wins, two_wins = n_wins(new_position, start_2, new_score_1, score_2, False, winning_score)
                total_one_wins += one_wins
                total_two_wins += two_wins

    if not one_to_move:
        for roll in (i+j+k for i in range(1,3) for j in range(1,3) for k in range(1,3)):
            new_position = start_2 + roll
            new_position = 1 + ((new_position - 1) % 10)

            new_score_2 = score_2 + new_position

            if new_score_2 >= winning_score:
                total_two_wins += 1
            else:
                one_wins, two_wins = n_wins(start_1, new_position, score_1, new_score_2, True, winning_score)
                total_one_wins += one_wins
                total_two_wins += two_wins

    return total_one_wins, total_two_wins


if __name__ == "__main__":
    assert part_1(4, 8) == 739785
    print(part_1(9, 10))

    assert (444356092776315, 341960390180808) == n_wins(4, 8, 0, 0, True, 21)
    print(max(n_wins(9, 10, 0, 0, True, 21)))