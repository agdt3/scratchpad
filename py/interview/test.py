#!/bin/python
import json

class Quicksort:
    def __init__(self, unsorted):
        self.unsorted = unsorted
        self.sorted = []

    def sort(self):
        self.sorted = self._sort(self.unsorted)
        return self.sorted

    def _sort(self, unsorted):
        if len(unsorted) <= 1:
            return unsorted

        less = []
        equal = []
        greater = []
        pivot = unsorted[0]

        for v in unsorted:
            if v < pivot:
                less.append(v)
            elif v > pivot:
                greater.append(v)
            else:
                equal.append(v)

        sorted_full = []
        sorted_full.extend(self._sort(less[:]))
        sorted_full.extend(equal)
        sorted_full.extend(self._sort(greater[:]))

        return sorted_full

class Powerset:
    def __init__(self, base_combos):
        self.base_combos = base_combos
        self.powerset = []

    def generate(self):
        self.powerset = self._generate(0, self.base_combos)
        return self.powerset

    def _generate(self, index, current_set):
        new_set = current_set[:]
        current_value = current_set[index]
        new_combo_created = False

        for v in current_set[index+1:]:
            new_combo = self._create_combo(current_value, v, new_set)
            if new_combo:
                new_combo_created = True
                new_set.append(new_combo)

        if not new_combo_created:
            return new_set
        else:
            return self._generate(index+1, new_set)

    def _create_combo(self, first, second, current_combos):
        # Check for inclusion in second part of set
        if first in second or first == second:
            return None
        else:
            new_combo = first | second

        # Check for existence in real sets
        for v in current_combos:
            if new_combo == v:
                new_combo = None
                break

        return new_combo

class Tree:
    def __init__(self, values):
        self.values = values
        self.tree = None
        self.insert_all(self.values)

    def insert_all(self, values):
        for v in values:
            self.tree = self._insert(v, self.tree)

    def _insert(self, v, tree):
        if tree is None:
            return self._node(v)
        else:
            if v < tree['value']:
                if tree['left'] is None:
                    tree['left'] = self._node(v)
                else:
                    self._insert(v, tree['left'])
            elif v > tree['value']:
                if tree['right'] is None:
                    tree['right'] = self._node(v)
                else:
                    self._insert(v, tree['right'])

            return tree

    def _node(self, v):
        return {
                'value': v,
                'left': None,
                'right': None
                }

class Mergesort:
    def __init__(self, unsorted_list):
        self.unsorted_list = unsorted_list

    def sort(self):
        self._split(self.unsorted_list)

    def _split(self):
        pass

    def _merge(self):
        pass

class Stringprocess:
    def __init__(self, string):
        self.string = string
        self.histogram = {}
        self.process()

    def process(self):
        index = 0
        for c in self.string:
            if c in self.histogram:
                self.histogram[c]['frequency'] += 1
            else:
                self.histogram[c] = {
                        'index': index,
                        'frequency': 1
                        }
                index += 1

    def find_first_by_frequency(self, frequency):
        lowest_index = len(self.histogram.keys()) - 1
        character = ''
        for k, v in self.histogram.iteritems():
            if v['frequency'] == frequency and v['index'] < lowest_index:
                lowest_index = v['index']
                character = k

        return character

if __name__ == "__main__":
    t = Quicksort([3,2,4,5,6,2,1,8,10,89,3,6])
    res = t.sort()
    print res

    t2 = Powerset([set('a'), set('b'), set('c'), set('d')])
    res2 = t2.generate()
    print res2

    t3 = Tree([3,2,4,5])
    print json.dumps(t3.tree, indent=4)

    t4 = Stringprocess("asdffdsaaqwerx")
    print t4.find_first_by_frequency(2)

