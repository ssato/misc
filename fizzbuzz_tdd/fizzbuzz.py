# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=unused-argument
import typing


FIZZ: typing.Literal[str] = "Fizz"
BUZZ: typing.Literal[str] = "Buzz"
FIZZ_BUZZ: typing.Literal[str] = "FizzBuzz"


FizzBuzzT = typing.Union[int, FIZZ, BUZZ, FIZZ_BUZZ]


def fizzbuzz_0(nmax: int):
    pass


def fizzbuzz_1(nmax: int) -> list[FizzBuzzT]:
    return []


def fizzbuzz_2(nmax: int) -> list[FizzBuzzT]:
    return [nmax]


def fizzbuzz_3(nmax: int) -> list[FizzBuzzT]:
    def gen(nmax: int) -> typing.Iterator[FizzBuzzT]:
        for n in range(1, nmax + 1):
            if n % 3 == 0:
                yield FIZZ
            else:
                yield n

    return list(gen(nmax))


def fizzbuzz_4(nmax: int) -> list[FizzBuzzT]:
    def gen(nmax: int) -> typing.Iterator[FizzBuzzT]:
        for n in range(1, nmax + 1):
            if n % 3 == 0:
                yield FIZZ
            elif n % 5 == 0:
                yield BUZZ
            else:
                yield n

    return list(gen(nmax))


def fizzbuzz_5(nmax: int) -> list[FizzBuzzT]:
    def gen(nmax: int) -> typing.Iterator[FizzBuzzT]:
        for n in range(1, nmax + 1):
            if n % 15 == 0:
                yield FIZZ_BUZZ
            elif n % 3 == 0:
                yield FIZZ
            elif n % 5 == 0:
                yield BUZZ
            else:
                yield n

    return list(gen(nmax))


def fizzbuzz_pure(nmax: int) -> list[FizzBuzzT]:
    def gen(nmax: int) -> typing.Iterator[FizzBuzzT]:
        for n in range(1, nmax + 1):
            if n % 15 == 0:
                yield FIZZ_BUZZ
            elif n % 3 == 0:
                yield FIZZ
            elif n % 5 == 0:
                yield BUZZ
            else:
                yield n

    # i want dependent type support ...
    if nmax < 1:
        raise ValueError(
            f"Argument #1 must be greater than 0: {nmax}."
        )

    return list(gen(nmax))


def fizzbuzz(nmax: int) -> None:
    for x in fizzbuzz_pure(nmax):
        print(x)
