# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument
"""test cases"""
import pytest

import fizzbuzz


def test_fizzbuzz_red_1():
    assert fizzbuzz.fizzbuzz_1(1) == [1]


def test_fizzbuzz_green_1():
    assert fizzbuzz.fizzbuzz_2(1) == [1]


def test_fizzbuzz_red_2():
    assert fizzbuzz.fizzbuzz_2(2) == [1, 2]


def test_fizzbuzz_green_2():
    assert fizzbuzz.fizzbuzz_3(2) == [1, 2]
    assert fizzbuzz.fizzbuzz_3(3) == [1, 2, "Fizz"]


def test_fizzbuzz_red_3():
    assert fizzbuzz.fizzbuzz_3(5) == [1, 2, "Fizz", 4, "Buzz"]


def test_fizzbuzz_green_3():
    assert fizzbuzz.fizzbuzz_4(5) == [1, 2, "Fizz", 4, "Buzz"]


def test_fizzbuzz_red_4():
    assert fizzbuzz.fizzbuzz_4(15) == [
        1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
        11, "Fizz", 13, 14, "Buzz"
    ]


def test_fizzbuzz_green_4():
    assert fizzbuzz.fizzbuzz_5(15) == [
        1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
        11, "Fizz", 13, 14, "FizzBuzz"
    ]


def test_fizzbuzz_red_5():
    with pytest.raises(ValueError):
        fizzbuzz.fizzbuzz_5(0)


def test_fizzbuzz_green_5():
    with pytest.raises(ValueError):
        fizzbuzz.fizzbuzz_pure(0)


@pytest.mark.parametrize(
    ("nmax", "expected"),
    ((1, [1]),
     (3, [1, 2, "Fizz"]),
     (5, [1, 2, "Fizz", 4, "Buzz"]),
     (15,
      [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz",
       11, "Fizz", 13, 14, "FizzBuzz"]),
     ),
)
def test_fizzbuzz(nmax, expected):
    assert fizzbuzz.fizzbuzz_pure(nmax) == expected
