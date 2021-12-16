from typing import Dict, Tuple
from collections import Counter


def real_input() -> str:
    with open("data/14.txt", "r") as f:
        return f.read()


def test_input() -> str:
    return """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def parse(input: str) -> Tuple[str, Dict[str, str]]:
    pattern, rules_raw = input.split("\n\n")

    rules = {line.split(" -> ")[0]: line.split(" -> ")[1] for line in rules_raw.split("\n")}

    return pattern, rules


def step(pattern: str, rules: Dict[str, str]) -> str:
    new_pattern = ""
    # NCNB
    for pos in range(len(pattern) - 1):
        if pattern[pos : pos + 2] in rules:
            new_pattern += f"{pattern[pos]}{rules[pattern[pos:pos+2]]}"

            # If this is our last double insertion we need to append the last char
            if pos + 1 == len(pattern) - 1:
                new_pattern += pattern[pos + 1]
        else:
            new_pattern += pattern[pos]
    return new_pattern


def apply_steps(pattern: str, rules: Dict[str, str], steps: int) -> str:
    for i in range(steps):
        # print(i, len(pattern))
        pattern = step(pattern, rules)

    return pattern


def score(pattern: str) -> int:
    c = Counter(iter(pattern))
    return c.most_common()[0][1] - c.most_common()[-1][1]


def apply_count_40(pattern: str, rules: Dict[str, str]) -> int:

    counts = {k: Counter(iter(apply_steps(k, rules, 20))) for k, v in rules.items()}

    mid_string = apply_steps(pattern, rules, 20)

    s: Counter = Counter()
    for i in range(len(mid_string) - 1):
        s += counts[mid_string[i : i + 2]]

    s -= Counter(mid_string[1:-1])
    return s.most_common()[0][1] - s.most_common()[-1][1]


if __name__ == "__main__":
    pattern, rules = parse(test_input())

    assert step(pattern, rules) == "NCNBCHB"
    assert apply_steps(pattern, rules, 1) == "NCNBCHB"
    assert apply_steps(pattern, rules, 2) == "NBCCNBBBCBHCB"
    assert apply_steps(pattern, rules, 3) == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    assert apply_steps(pattern, rules, 4) == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    assert score(apply_steps(pattern, rules, 10)) == 1588

    pattern, rules = parse(real_input())

    print(score(apply_steps(pattern, rules, 10)))

    # Part 2
    pattern, rules = parse(test_input())

    assert 2188189693529 == apply_count_40(pattern, rules)

    pattern, rules = parse(real_input())
    print(apply_count_40(pattern, rules))
