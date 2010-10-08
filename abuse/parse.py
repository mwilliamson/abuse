from abuse.generate import NonTerminal

def parse(text, rule_set):
    for line in filter(lambda l: l.strip(), text.split("\n")):
        parse_line(line, rule_set)
    
def parse_line(text, rule_set):
    left, right = map(str.strip, text.split("->"))
    result = []
    while right.find("$") != -1:
        dollar_index = right.find("$")
        result.append(right[:dollar_index])
        
        end_of_non_terminal = dollar_index + 1
        while right[end_of_non_terminal:end_of_non_terminal + 1] != " " and len(right) > end_of_non_terminal:
            end_of_non_terminal += 1
        result.append(NonTerminal(right[dollar_index + 1:end_of_non_terminal]))
        
        right = right[end_of_non_terminal:]
    
    if right:
        result.append(right)
    rule_set.add(NonTerminal(left[1:]), *result)
