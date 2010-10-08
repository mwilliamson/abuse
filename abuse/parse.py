from abuse.generate import NonTerminal

def parse(text, rule_set):
    for line in filter(lambda l: l.strip(), text.split("\n")):
        parse_line(line, rule_set)
    
def parse_line(text, rule_set):
    left, right = map(str.strip, text.split("->"))
    rule_set.add(NonTerminal(left[1:]), right)
