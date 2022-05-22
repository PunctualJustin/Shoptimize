from enum import Enum

from functools import reduce
from typing import List, Dict


class ColumnWidths(Enum):
    INDEX = 6
    NAME = 30
    PRICE = 10


def list_printer(
    headers: Dict[str, int], contents: List[List[str]], index=True, no_header=False
):
    if no_header:
        column_formatter = reduce(
            lambda x, y: (x if isinstance(x, str) else " {:<" + f"{x.value}" + "}")
            + " {:<"
            + f"{y.value}"
            + "}",
            headers,
        )
    else:
        column_formatter = reduce(
            lambda x, y: (x if isinstance(x, str) else " {:<" + f"{x.value}" + "}")
            + " {:<"
            + f"{y.value}"
            + "}",
            headers.values(),
        )
        print(column_formatter.format(*[header for header in headers]))
    if index:
        for index, row in enumerate(contents):
            print(column_formatter.format(index + 1, *row))
    else:
        for index, row in enumerate(contents):
            print(column_formatter.format(*row))
