from abuse.generate import NonTerminal

_non_terminal_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_"

def parse(text, rule_set):
    for line in filter(lambda l: l.strip(), text.split("\n")):
        parse_line(line, rule_set)

def parse_line(text, rule_set):
    left, right = map(str.strip, text.split("->"))
    result = []
    index = 0
    while right.find("$", index) != -1:
        dollar_index = right.find("$", index)
        result.append(right[index:dollar_index])
        
        if right[dollar_index + 1] == "{":
            closing_brace_index = right.find("}", dollar_index)
            end_of_non_terminal = closing_brace_index + 1
            non_terminal_name = right[dollar_index + 2:closing_brace_index]
        else:
            end_of_non_terminal = dollar_index + 1
            while is_non_terminal_char(right, end_of_non_terminal):
                end_of_non_terminal += 1
            non_terminal_name = right[dollar_index + 1:end_of_non_terminal]
        result.append(NonTerminal(non_terminal_name))
        
        index = end_of_non_terminal
    
    remainder = right[index:]
    if remainder:
        result.append(remainder)
    rule_set.add(NonTerminal(left[1:]), *result)

def is_non_terminal_char(string, index):
    return string[index:index + 1] in _non_terminal_chars and len(string) > index
