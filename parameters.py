
def func(a, b, c):
    return (a, b, c)

def test_func():

    assert func(1, 2, 3) == (1, 2, 3)
    assert func(**dict(a=4, b=5, c=6)) == (4, 5, 6)
    assert func(a=7, **dict(b=8, c=9)) == (7, 8, 9)

    with open('/tmp/params.txt', 'w') as f:
        f.write("a=10\nb=11\nc=12\n")

    d = {}
    with open('/tmp/params.txt') as f:
        d.update(dict(item.strip().split("=") for item in f))
    assert func(**d) == ('10', '11', '12')

def func2(filename=None, a=None, b=None, c=None):
    print(locals())
    return (a, b, c)

def test_func2():
    func2()

if __name__ == "__main__":
    test_func2()