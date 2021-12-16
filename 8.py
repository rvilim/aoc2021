from typing import Tuple, List
from collections import defaultdict


def test_input() -> List[Tuple[List[str], List[str]]]:
    raw = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""
    split = raw[:-1].split("\n")

    return [(s.split(" ")[:10], s.split(" ")[11:]) for s in split]


def real_input() -> List[Tuple[List[str], List[str]]]:
    with open("data/8.txt") as f:
        return [(s.rstrip().split(" ")[:10], s.rstrip().split(" ")[11:]) for s in f]


def count_1478(input):
    return sum(1 for row in input for signal in row[1] if len(signal) in (2, 3, 4, 7))


def group(unique_signals: List[str]):
    groups = defaultdict(list)

    for signal in unique_signals:
        groups[len(signal)].append({s for s in signal})
    return groups


def solve_a(grouped_signals):
    one = grouped_signals[2][0]
    seven = grouped_signals[3][0]

    return list(seven - one)[0]


def solve_c(grouped_signals):
    one = grouped_signals[2][0]

    for signal in grouped_signals[6]:
        # Of all the 6 segment numbers, the only one which changes length when you union
        # its segments with one is 6, that's because the 'c' segment is added. We can figure
        # out what c is if we just subtract them
        if len(one.union(signal)) != len(signal):
            return list(one - signal)[0]


def solve_f(grouped_signals, a, c):
    seven = grouped_signals[3][0]

    return list(seven - {a} - {c})[0]


def solve_b(grouped_signals, c, f):
    signals = grouped_signals[5]

    for signal in signals:
        # Figure out if this signal represents 5 or not
        if f in signal and c not in signal:
            # If its a 5, then b must be the only segment that isn't in the union of 2 and 3
            return list(signal - set.union(*[s for s in signals if s != signal]))[0]


def solve_e(grouped_signals, c, f):
    signals = grouped_signals[5]

    for signal in signals:
        # Test if this represents a 2 or not
        if c in signal and f not in signal:
            # If its a 2, then e must be the only segment that isn't in the union of 5 and 6
            return list(signal - set.union(*[s for s in signals if s != signal]))[0]


def solve_d(grouped_signals, b, c, f):
    return list(grouped_signals[4][0] - {b} - {c} - {f})[0]


def solve_g(grouped_signals, a, e):
    return list(grouped_signals[7][0] - grouped_signals[4][0] - {a} - {e})[0]


def solve_segments(grouped_signals):
    solution = {}

    solution["a"] = solve_a(grouped_signals)
    solution["c"] = solve_c(grouped_signals)
    solution["f"] = solve_f(grouped_signals, solution["a"], solution["c"])
    solution["b"] = solve_b(grouped_signals, solution["c"], solution["f"])
    solution["e"] = solve_e(grouped_signals, solution["c"], solution["f"])
    solution["d"] = solve_d(grouped_signals, solution["b"], solution["c"], solution["f"])
    solution["g"] = solve_g(grouped_signals, solution["a"], solution["e"])

    solution = {v: k for k, v in solution.items()}

    return solution


def decode(solution, digits):
    decoder = {
        "abcefg": "0",
        "cf": "1",
        "acdeg": "2",
        "acdfg": "3",
        "bcdf": "4",
        "abdfg": "5",
        "abdefg": "6",
        "acf": "7",
        "abcdefg": "8",
        "abcdfg": "9",
    }

    return int("".join([decoder["".join(sorted(solution[d] for d in digit))] for digit in digits]))


def solve(inputs):

    for signals, output in inputs:
        grouped = group(signals)
        solution = solve_segments(grouped)
        digits = decode(solution, output)
        yield digits
        #  digits
    #     yield digits


if __name__ == "__main__":
    t = test_input()
    assert count_1478(t) == 26

    r = real_input()
    print(count_1478(r))

    # part 2
    for expected, actual in zip(solve(t), [8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315]):
        assert expected == actual
    assert sum(solve(t)) == 61229

    print(sum(solve(r)))
