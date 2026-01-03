from typing import List, Tuple
def last_minus_first_equals_length_minus_one(sequence: List[int]):
    return sequence[-1] - sequence[0] == len(sequence) - 1

def lenA_plusB_minus_sumA_always_leB_when_sumA_leB(a: List[int], b: int) -> Tuple[bool, int]:
    v = len(a) + b - sum(a)
    return  v <= b, v