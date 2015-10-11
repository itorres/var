#!/usr/bin/env python

import csv
import sys
import json
import hashlib
from subprocess import Popen, PIPE
from urlparse import urlparse

DEFAULT_GROUP = "lastpass-import"


class Record:
    def __init__(self, d):
        self.d = d

        self.password = d['password']

        if d['grouping'] in [None, "", "(none)"]:
            self.group = DEFAULT_GROUP
        else:
            self.group = d['grouping']

        self.d['kind'] = "lastpass imported item"
        self.name = d['name']
        self.username = d['username']
        self.netloc = urlparse(d['url']).netloc
        self.text = "{}\n{}".format(
            self.password, json.dumps(self.d, sort_keys=True,
                                      indent=2, separators=(',', ': ')))
        self.md5 = hashlib.md5(self.text).hexdigest()

        if self.name is None or self.name == "":
            if self.netloc is None or self.netloc == "":
                self.name = self.md5
            else:
                self.name = self.netloc

        if self.username is None or self.username == "":
            self.username = "unknown"

        self.id = "{}/{}/{}".format(self.group,
                                    self.name.replace('/', '_'),
                                    self.username.replace('/', '_'))

        self.items = [self]

    def append(self, entry):
        self.items.append(entry)

    def writeToPass(self):
        if len(self.items) == 1:
            process = Popen(["pass", "insert", "-m", self.id], stdin=PIPE,
                            stdout=PIPE, stderr=None)
            self.stdout = process.communicate(str(self))
            self.result = process.returncode
        else:
            for (i, v) in enumerate(self.items):
                key = "{}/{}".format(self.id, i)
                process = Popen(["pass", "insert", "-m", key],
                                stdin=PIPE, stdout=PIPE, stderr=None)
                self.stdout = process.communicate(str(v))
                self.result = process.returncode

    def __str__(self):
        return self.text


class Records:
    def __init__(self):
        self.d = dict()

    def add(self, r):
        if r.id not in self.d:
            self.d[r.id] = r
        else:
            self.d[r.id].append(r)

    def get(self, k):
        return self.d[k]

fn = sys.argv[1]
with open(fn, 'rb') as cf:
    lp = csv.DictReader(cf, delimiter=',')
    rs = Records()
    for l in lp:
        r = Record(l)
        rs.add(r)
    for k, v in rs.d.items():
        v.writeToPass()
        if v.result != 0:
            print "{} {} {}".format(v.result, len(v.items), k)
