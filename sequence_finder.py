# SPDX-License-Identifier: MIT
# pylint: disable=missing-function-docstring
r"""Find sequence.

.. seealso:: https://twitter.com/Sheeeeepla/status/1554028833942441984

Example:

ssato@fedora% python3 sequence_finder.py --help
Usage: sequence_finder.py [OPTIONS]

  entry point.

Options:
  --needle TEXT    A sequence of words separated with ' ' (a space) to search
  --haystack TEXT  A list of words separated with ' ' (a space) to search from
  --msg TEXT       A message to print if it was found
  -v, --verbose    Verbose mode
  --help           Show this message and exit.
ssato@fedora% python3 sequence_finder.py
スコ スコ スコ スコ ドド ドド スコ スコ ドド スコ スコ ドド スコ ドド ドド スコ スコ スコ
ラブ注入♡
ssato@fedora% python3 sequence_finder.py -v
スコ スコ スコ スコ ドド ドド スコ スコ ドド ドド ドド スコ スコ スコ
ラブ注入♡  (at: 11)
ssato@fedora% python3 sequence_finder.py --needle 'G A T C' \
> --haystack 'G G A A T T C C G A G A T C' \
> --msg 'Found the gene pattern' --verbose
G G A A T T C C G A G A T C
Found the gene pattern  (at: 11)
ssato@fedora%
"""
import os
import random
import sys
import typing

import click


def sequence_(*keys: str) -> str:
    while True:
        yield random.choice(keys)


class FoundExc(Exception):
    pass


def find_a_needle_in_a_haystack_itr(
    haystack: typing.Iterator[str],
    needle: list[str],
    acc: typing.Union[bool, list[str]] = False
) -> typing.Iterator[str]:
    """Find a needle ``needle`` in a haystack ``haystack``."""
    head: str = needle[0]
    last: str = needle[-1]
    lead: list[str] = needle[:-1]

    for item in haystack:
        yield item

        if item == head:
            acc = [head]
            continue

        if acc:
            if item == last and acc == lead:
                raise FoundExc()

            acc.append(item)


NEEDLE: str = 'ドド スコ スコ スコ'
MSG: str = 'ラブ注入♡ '


@click.command()
@click.option(
    '--needle', default=NEEDLE,
    help="A sequence of words separated with ' ' (a space) to search"
)
@click.option(
    '--haystack', default='',
    help="A list of words separated with ' ' (a space) to search from"
)
@click.option(
    '--msg', default=MSG, help="A message to print if it was found"
)
@click.option(
    '--verbose', '-v', is_flag=True, default=False, help="Verbose mode"
)
def main(
    needle: str = NEEDLE,
    haystack: str = '',
    msg: str = MSG,
    verbose: bool = False
) -> None:
    """entry point."""
    ndl = needle.split()
    hstk = haystack.split() if haystack else sequence_(*set(ndl))
    vitr = find_a_needle_in_a_haystack_itr(hstk, ndl)

    try:
        nitems = 0
        for val in vitr:
            print(f'{val}', end=' ')
            nitems += 1

        print(f'{os.linesep}Not found: {needle}')
        sys.exit(1)

    except FoundExc:
        if verbose:
            pos: int = nitems - len(ndl) + 1
            print(f'{os.linesep}{msg} (at: {pos})')
        else:
            print(f'{os.linesep}{msg}')


if __name__ == '__main__':
    main()
