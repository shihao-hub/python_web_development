from functools import partial


def test_partial():
    def fn(a, b, c):
        print(a, b, c)

    fn(1, 2, 3)

    fn2 = partial(fn, 11, 22)
    fn2(33)


if __name__ == '__main__':
    test_partial()
