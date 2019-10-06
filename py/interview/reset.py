#! /bin/pythong

class Reset:
    def __init__(self, values = []):
        self._values = {}

        if len(values) > 0:
            for value in values:
                self._values[value] = True

    def get_values(self):
        return self._values

    def intersect(self, reset2):
        new_values = []

        r2_values = reset2.get_values()
        for k, v in self._values.items():
            if k in r2_values:
                new_values.append(k)

        return Reset(new_values)

    def union(self, reset2):
        new_values = []

        r2_values = reset2.get_values()
        for k, v in self._values.items():
            new_values.append(k)

        for k, v in r2_values.items():
            new_values.append(k)

        return Reset(new_values)

    def difference(self, reset2):
        new_values = []

        r2_values = reset2.get_values()
        for k, v in self._values.items():
            if k not in r2_values:
                new_values.append(k)

        for k, v in r2_values.items():
            if k not in self._values:
                new_values.append(k)

        return Reset(new_values)

    def __str__(self):
        keys = self._values.keys()
        return ", ".join([str(k) for k in keys])

if __name__ == "__main__":
    r1 = Reset([1,2,3,4])
    r2 = Reset([3,4,5,6])

    r3 = r1.intersect(r2)
    r4 = r1.union(r2)
    r5 = r1.difference(r2)

    print r3
    print r4
    print r5
