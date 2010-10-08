from nose.tools import assert_equals

from abuse.generate import NonTerminal
from abuse.generate import RuleSet
from abuse.generate import generate
from abuse.generate import sentence

class StaticSelector(object):
    def __init__(self, *choices):
        self._choices = list(choices[::-1])
        
    def select(self, lower, upper):
        return self._choices.pop()

def test_adding_rule_to_convert_sentence_to_terminal():
    rule_set = RuleSet()
    rule_set.add(sentence, "I hate you!")
    assert_equals("I hate you!", generate(rule_set, StaticSelector(0)))

def test_selector_is_used_to_pick_rule_when_there_are_many_possible_rules():
    rule_set = RuleSet()
    rule_set.add(sentence, "I hate you!")
    rule_set.add(sentence, "Go to hell!")
    assert_equals("I hate you!", generate(rule_set, StaticSelector(0)))
    assert_equals("Go to hell!", generate(rule_set, StaticSelector(1)))
    
def test_can_use_intermediate_rules():
    rule_set = RuleSet()
    smell = NonTerminal("SMELL")
    rule_set.add(sentence, "You smell of ", smell)
    rule_set.add(smell, "elderberries")
    rule_set.add(smell, "dogfood")
    
    assert_equals("You smell of elderberries", generate(rule_set, StaticSelector(0, 0)))
    assert_equals("You smell of dogfood", generate(rule_set, StaticSelector(0, 1)))
