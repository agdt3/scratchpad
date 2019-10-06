#! /bin/python

class Mergesort:
    def __init__(self, values):
        self._values = values

    def sort(self):
        if len(self._values) < 2:
            return self._values
        else:
           self._values = self._breakdown(self._values)

    def _breakdown(self, values):
        if len(values) == 1:
            return values
        else:
            half = len(values) / 2
            left = values[0:half]
            right = values[half:len(values)]
            return self._merge(self._breakdown(left), self._breakdown(right))

    def _merge(self, values1, values2):
        # both left and right are already internally sorted
        # hence leftmost value will always be smaller than value
        # to the right in each list

        values = []
        while True:
            if len(values1) == 0 or len(values2) == 0:
                break
            if values1[0] < values2[0]:
                values.append(values1.pop(0))
            elif values1[0] > values2[0]:
                values.append(values2.pop(0))
            else:
                values.append(values1.pop(0))
                values.append(values2.pop(0))

        # sort one of remaineder
        for v in values1:
            values.append(v)

        for v2 in values2:
            values.append(v2)

        return values

    def __str__(self):
       return ", ".join([str(v) for v in self._values])


if __name__ == "__main__":
    m = Mergesort([4,3,1,6,3,8,2,5])
    m.sort()
    print m
