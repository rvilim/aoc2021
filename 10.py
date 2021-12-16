from typing import List, Optional, Tuple


def real_data() -> List[str]:
    with open("data/10.txt") as f:
        return [line.rstrip() for line in f]


def test_data() -> List[str]:
    raw = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

    return raw.split("\n")


def is_corrupt(line: str) -> Tuple[Optional[str], List[str]]:
    chars = {"(": ")", "[": "]", "{": "}", "<": ">"}
    openings = tuple(chars.keys())
    closings = tuple(chars.values())

    stack = []

    for pos, char in enumerate(line):
        if char in openings:
            stack.append(char)
        elif char in closings:
            s = stack.pop()
            if chars[s] != char:
                return char, stack

            if not stack and pos == len(line) - 1:
                return None, stack

    return None, stack


def score_1(chars: List[Tuple[Optional[str], List[str]]]) -> int:
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum(scores[s[0]] for s in chars if s[0] is not None)


def score_2(completions: List[str]) -> int:
    char_scores = {")": 1, "]": 2, "}": 3, ">": 4}
    scores = []
    for completion in completions:
        if completion is None:
            continue

        score = 0
        for char in completion:
            score *= 5
            score += char_scores[char]

        scores.append(score)

    if len(scores) == 1:
        return scores[0]

    return sorted(scores)[len(scores) // 2]


def complete_stack(stack: List[str]) -> str:
    chars = {"(": ")", "[": "]", "{": "}", "<": ">"}
    return "".join(chars[s] for s in reversed(stack))


def score_completions(input: List[str]) -> int:
    completions = [complete_stack(is_corrupt(line)[1]) for line in input if is_corrupt(line)[0] is None]
    return score_2(completions)


if __name__ == "__main__":
    t = test_data()

    expecteds = [None, None, "}", None, ")", "]", None, ")", ">", None]
    for line, expected in zip(t, expecteds):
        assert is_corrupt(line)[0] == expected

    assert score_1([is_corrupt(line) for line in t]) == 26397

    r = real_data()
    print(score_1([is_corrupt(line) for line in r]))

    # Part 2

    expecteds = [r"}}]])})]", r")}>]})", None, r"}}>}>))))", None, None, r"]]}}]}]}>", None, None, r"])}>"]
    for line, expected in zip(t, expecteds):
        if expected is not None:
            corrupt_char, stack = is_corrupt(line)

            assert complete_stack(stack) == expected

    assert score_2([r"}}]])})]"]) == 288957
    assert score_2([r")}>]})"]) == 5566
    assert score_2([r"}}]])})]", r")}>]})", r"}}>}>))))", r"]]}}]}]}>", r"])}>"]) == 288957

    assert score_completions(t) == 288957
    print(score_completions(r))
