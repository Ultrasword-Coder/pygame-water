class classone:
    def __init__(self):
        self.v = 0


class classtwo(classone):
    def __init__(self):
        super().__init__()
        self.val = 0


a = classtwo()
b = classone()

print(a, dir(a))
print(b, dir(b))
print(a.__class__)
t = a.__class__()
