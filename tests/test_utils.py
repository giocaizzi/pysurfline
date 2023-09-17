from pysurfline.utils import flatten
from dataclasses import dataclass


def test_flatten_dict():
    @dataclass
    class A:
        a: int
        b: int

    d = {
        "a": 1,
        "b": {"c": 2, "d": {"e": 3}},
        "f": [4, {"g": 5}],
        "h": {"i": {"j": {"k": 6}}},
        "l": A(1, 2),
        "m": [A(1, 2), A(3, 4)],
    }
    expected = {
        "a": 1,
        "b_c": 2,
        "b_d_e": 3,
        "f_0": 4,
        "f_1_g": 5,
        "h_i_j_k": 6,
        "l_a": 1,
        "l_b": 2,
        "m_0_a": 1,
        "m_0_b": 2,
        "m_1_a": 3,
        "m_1_b": 4,
    }
    assert flatten(d) == expected
