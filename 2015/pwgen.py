#!/usr/bin/env python
import re
from random import randint


class PasswordGenerator:
    def __init__(self, elements=5, word_length=6):
        self.elements = [None] * elements
        self.picked = []
        self.words = []
        with open('/usr/share/dict/words', 'r') as words:
            for w in words:
                w = w.strip()
                if len(w) == word_length and self.match(w):
                    self.words.append(w)

    def match(self, strg, search=re.compile(r'[^A-Za-z0-9]').search):
        # http://stackoverflow.com/a/1325265/267777
        return not bool(search(strg))

    def pick_one(self):
        candidate = randint(0, len(self.words))
        if candidate not in self.picked:
            self.picked.append(candidate)
            return candidate
        return self.pick_one()

    def build(self):
        if len(self.words) < len(self.elements):
            raise Exception("")
        for i in range(len(self.elements)):
            self.elements[i] = self.words[self.pick_one()]

    def __str__(self):
        return '-'.join([e.lower() for e in self.elements])

if __name__ == '__main__':
    p = PasswordGenerator()
    p.build()
    print p
