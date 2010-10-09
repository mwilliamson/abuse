from nose.tools import assert_equals

from abuse.generate import NonTerminal
from abuse.generate import RuleSet
from abuse.generate import generate
from abuse.generate import generate_all
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
    
def test_can_generate_all_sentences():
    rule_set = RuleSet()
    rule_set.add(sentence, "I hate you!")
    smell = NonTerminal("SMELL")
    rude_adj = NonTerminal("RUDE_ADJ")
    pet = NonTerminal("PET")
    rule_set.add(sentence, "You smell of ", smell)
    rule_set.add(smell, "elderberries")
    rule_set.add(smell, "dogfood")
    rule_set.add(sentence, "You're as ", rude_adj, " as my ", pet)
    rule_set.add(rude_adj, "ugly")
    rule_set.add(rude_adj, "stupid")
    rule_set.add(pet, "rat")
    rule_set.add(pet, "dog")
    
    assert_equals(["I hate you!", "You smell of elderberries", "You smell of dogfood",
                   "You're as ugly as my rat", "You're as ugly as my dog",
                   "You're as stupid as my rat", "You're as stupid as my dog"], generate_all(rule_set))

