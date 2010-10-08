import funk
from funk import expects

from abuse.generate import RuleSet
from abuse.generate import NonTerminal
from abuse.parse import parse

def test_ignores_blank_lines():
    parse("\n\n\n\n\n\r\t\t \n\n     \r\n\n", None)
    
@funk.with_context
def test_can_read_rule_for_terminal_to_non_terminal(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "I hate you!")
    
    parse("$SENTENCE -> I hate you!", rule_set)

@funk.with_context
def test_can_read_multiple_rules_separated_by_newlines(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "I hate you!")
    expects(rule_set).add(NonTerminal("SENTENCE"), "You smell!")
    
    parse("$SENTENCE -> I hate you!\n$SENTENCE -> You smell!", rule_set)

@funk.with_context
def test_can_read_non_terminals_on_right(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "You smell of ", NonTerminal("SMELL"))
    expects(rule_set).add(NonTerminal("SENTENCE"), "Your ", NonTerminal("BODYPART"), " looks funny")
    expects(rule_set).add(NonTerminal("SENTENCE"), "You're as ", NonTerminal("ADJ"), " as a ", NonTerminal("ANIMAL"))
    
    parse("$SENTENCE -> You smell of $SMELL", rule_set)
    parse("$SENTENCE -> Your $BODYPART looks funny", rule_set)
    parse("$SENTENCE -> You're as $ADJ as a $ANIMAL", rule_set)
