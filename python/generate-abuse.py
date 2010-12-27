#!/usr/bin/env python

import sys
import random

from abuse.parse import parse
from abuse.generate import generate
from abuse.generate import generate_all
from abuse.generate import RuleSet

class RandomSelector(object):
    def select(self, lower, upper):
        return random.randint(lower, upper - 1)

rule_set = RuleSet()

if "--all" in sys.argv:
    sys.argv.remove("--all")
    all_abuse = True
else:
    all_abuse = False
    
parse(open(sys.argv[1]).read(), rule_set)
if all_abuse:
    print "\n".join(generate_all(rule_set))
else:
    print generate(rule_set, RandomSelector())
