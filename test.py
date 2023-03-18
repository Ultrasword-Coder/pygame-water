
class classone:
    def __init__(self):
        self.v = 0


class classtwo(classone):
    def __init__(self):
        super().__init__()
        self.val = 0


class classthree(classtwo):
    def __init__(self):
        super().__init__()
        self.val2 = 2


a = classone()
b = classtwo()
c = classthree()


def recursive_retrieve_parent_classes(obj, level=0):
    result = []
    itt = obj.__class__.__bases__ if level == 0 else obj.__bases__
    if itt:
        for base in itt:
            if base == object:
                continue
            result.append(base)
            result += recursive_retrieve_parent_classes(base, level + 1)
    return result


print(recursive_retrieve_parent_classes(c))
