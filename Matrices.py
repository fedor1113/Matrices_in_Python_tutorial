class Matrix:
    """A simple wrapper around a two-dimensional list"""

    def __init__(self, lst=[[]]):
        self._lst = lst
        self.update_order()
    # ...

    def __getitem__(self, index):
        return self._lst[index]

    def __setitem__(self, index, val):
        self._lst[index] = val

    def __delitem__(self, index):
        del self._lst[index]
        self.update_order()

    def __iter__(self):
        return self._lst.__iter__()

    def __len__(self):
        # return len([r for r in self._lst])
        return self.order[0] * self.order[1]

    def __contains__(self, item):
        return item in self._lst

    def __add__(self, other):
        assert type(other) is Matrix
        return Matrix([[e1 + e2 for e1, e2 in zip(r1, r2)]
                       for r1, r2 in zip(self._lst, other)])

    def __sub__(self, other):
        assert type(other) is Matrix
        return Matrix([[e1 - e2 for e1, e2 in zip(r1, r2)]
                       for r1, r2 in zip(self._lst, other)])

    def update_order(self):
        self.order = (len(self._lst), len(self._lst[0]))
        # количество строк, количество столбцов

    def __matmul__(self, multiplier):
        if self.order[1] != multiplier.order[0]:
            raise ArithmeticError("Matrices are non-conformable.")

        return Matrix([[sum(a*b for a, b in zip(srow, mcol))
                        for mcol in zip(*multiplier._lst)]
                       for srow in self._lst])

    def __rmatmul__(self, multiplicand):
        if multiplicand.order[1] != self.order[0]:
            raise ArithmeticError("Matrices are non-conformable.")

        return Matrix([[sum(a*b for a, b in zip(mrow, scol))
                        for scol in zip(*self._lst)]
                       for mrow in multiplicand._lst])

    def __imatmul__(self, multiplier):
        """For a @= b"""
        self._lst = self @ multiplier
        return Matrix(self._lst)

    def transpose(self):
        self._lst = list(zip(*self._lst))

    def arithmetic_mean(self):
        s, cnt = 0, 0
        for r in self._lst:
            for e in r:
                cnt += 1
                s += e

        return s / cnt

    def unformatted_str(self):
        # def _process_row(r):
        #     return " ".join(map(str, r)) + "\n"
        srepr = "".join((" ".join(map(str, r)) + "\n"
                         for r in self._lst))

        return srepr

    def __str__(self):
        from functools import partial

        def _frmt(el, max_len=0):
            r = f"{el:>{max_len}}"  # PEP 498 -- Literal String Interpolation
            # >= Python 3.6

            # r = "{:>{}}".format(el, max_len)
            # compatible with everything

            return r

        srepr = ""
        max_len = 0
        max_len = max((len(str(elem))
                       for row in self._lst
                       for elem in row),
                      default=0)
        _frmt = partial(_frmt, max_len=max_len)

        for row in self._lst:
            srepr += " ".join(map(_frmt,
                                  map(str, row))) + "\n"

        return srepr


def main():
    rows, cols = map(int, input().split())
    lst = [list(map(int, input().split())) for r in range(rows)]
    m1 = Matrix(lst)
    rows, cols = map(int, input().split())
    lst = [list(map(int, input().split())) for r in range(rows)]
    m2 = Matrix(lst)

    print(m1 @ m2)


if __name__ == "__main__":
    main()
