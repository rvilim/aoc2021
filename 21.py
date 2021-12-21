from functools import cache

import time


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
def update_score_position(start, score, roll):
    new_position = start + roll
    new_position = 1 + ((new_position - 1) % 10)
    new_score = score + new_position

    return new_position, new_score


rolls = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


@cache
def n_wins(moving_start: int, other_start: int, moving_score: int, other_score: int, one_moving: bool):

    total_one_wins = 0
    total_two_wins = 0

    for roll, n in rolls.items():
        new_position, new_score = update_score_position(moving_start, moving_score, roll)

        if new_score < 21:
            one_wins, two_wins = n_wins(other_start, new_position, other_score, new_score, not one_moving)
            total_one_wins += n * one_wins
            total_two_wins += n * two_wins
        elif one_moving:
            total_one_wins += n
        else:
            total_two_wins += n

    return total_one_wins, total_two_wins


if __name__ == "__main__":
    assert part_1(4, 8) == 739785
    print(part_1(9, 10))

    assert (444356092776315, 341960390180808) == n_wins(4, 8, 0, 0, 1)

    t = time.process_time()
    p1_wins, p2_wins = n_wins(4, 8, 0, 0, 1)
    elapsed_time = time.process_time() - t
    print(f"{max(p2_wins,p1_wins)-min(p2_wins,p1_wins)} in {elapsed_time:.3f} seconds")
