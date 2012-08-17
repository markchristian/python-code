#!/usr/bin/env python

import sys, subprocess

INPUT = sys.argv[1]
TO_PARSE = subprocess.Popen("/bin/awk '/host/' " + INPUT,stdout=subprocess.PIPE,shell=True).stdout.read()
print TO_PARSE.replace("|","\n")
