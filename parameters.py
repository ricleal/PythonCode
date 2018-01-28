
def func(a, b, c):
    print(a, b, c)


func(1, 2, 3)
func(**dict(a=4, b=5, c=6))
func(a=7, **dict(b=8, c=9))


with open('/tmp/params.txt', 'w') as f:
    f.write("a=10\nb=11\nc=12\n")

d = {}
with open('/tmp/params.txt') as f:
    d.update(dict(item.strip().split("=") for item in f))
func(**d)