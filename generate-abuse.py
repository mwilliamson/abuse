#!/usr/bin/env python

import sys
import random

from abuse.parse import parse
from abuse.generate import generate
from abuse.generate import RuleSet

class RandomSelector(object):
    def select(self, lower, upper):
        return random.randint(lower, upper - 1)

rule_set = RuleSet()
parse(open(sys.argv[1]).read(), rule_set)
print generate(rule_set, RandomSelector())
