import funk
from funk import expects

from abuse.generate import RuleSet
from abuse.generate import NonTerminal
from abuse.parse import parse

def test_can_parse_source_with_only_whitespace():
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
def test_whitespace_is_trimmed_from_right(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "I hate you!")

    parse("$SENTENCE -> I hate you!    \t\t", rule_set)

@funk.with_context
def test_final_terminal_is_only_trimmed_on_the_right(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("VERY"), "", NonTerminal("VERY"), " very")

    parse("$VERY -> $VERY very", rule_set)

@funk.with_context
def test_ignores_blank_lines(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "I hate you!")
    expects(rule_set).add(NonTerminal("SENTENCE"), "You smell!")

    parse("\n    \t\n\n$SENTENCE -> I hate you!\n     \n\n$SENTENCE -> You smell!\n\n\n", rule_set)

@funk.with_context
def test_can_read_non_terminals_on_right(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "You're as ", NonTerminal("ADJ"), " as a ", NonTerminal("ANIMAL"))
    
    parse("$SENTENCE -> You're as $ADJ as a $ANIMAL", rule_set)

@funk.with_context
def test_non_terminals_are_alphanumeric_and_underscores_only(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "You smell of ", NonTerminal("Smell2"), ".")
    
    parse("$SENTENCE -> You smell of $Smell2.", rule_set)

@funk.with_context
def test_can_use_braces_to_indicate_non_terminals(context):
    rule_set = context.mock(RuleSet)
    expects(rule_set).add(NonTerminal("SENTENCE"), "You're ", NonTerminal("RUDE_ADJ"), "er than I thought")
    
    parse("$SENTENCE -> You're ${RUDE_ADJ}er than I thought", rule_set)
    
