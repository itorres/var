import csv
import sys
import re
import hashlib

class Record:
    def __init__(self, d):
        self.d = d

        self.text = "{}\n---\n".format(d['password'])
        for i in d.keys():
            self.text += "{}: {}\n".format(i, d[i])

        self.md5 = hashlib.md5(self.text).hexdigest()

        self.id = "@".join([self.d['username'], self.d['name']])
        if self.id == "@":
            self.id = self.md5

    def slug(self):
        return re.sub(r"[ /:]", "_", self.id)

    def __str__(self):
        return self.slug()

fn = sys.argv[1]

class Records:
    def __init__(self):
        self.d = dict()

    def add(self, r):
        if r.id not in self.d:
            self.d[r.id] = [r]
        else:
            self.d[r.id].append(r)

with open(fn, 'rb') as cf:
    lp = csv.DictReader(cf, delimiter = ',')
    print dir(lp)
    rs = Records()
    for l in lp:
        r = Record(l)
        rs.add(r)
    import pdb; pdb.set_trace()

