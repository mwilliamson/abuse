import re
from abuse.generate import NonTerminal

_non_terminal_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_"
_split_string = "->"

class MissingArrow(object):
    def __init__(self, line_number):
        self.message = "Missing symbol on line %s: %s" % (line_number, _split_string)
        self.line_number = line_number
    
    def __str__(self):
        return self.message
        
    def __repr__(self):
        return self.message

class MissingClosingBrace(object):
    def __init__(self, line_number, opening_brace_character_number):
        self.line_number = line_number
        self.opening_brace_character_number = opening_brace_character_number
        self.message = "Missing closing brace on line %s (opening brace at character %s)" % \
            (line_number, opening_brace_character_number)
        
    def __str__(self):
        return self.message
        
    def __repr__(self):
        return self.message

def parse(text, rule_set, errors):
    for line_number, line in enumerate(text.split("\n")):
        if len(line.strip()) > 0:
            parse_line(line_number + 1, line, rule_set, errors)

def parse_line(line_number, text, rule_set, errors):
    if _split_string not in text:
        errors.append(MissingArrow(line_number))
        return
    left, right = text.split(_split_string)
    result = []
    search_results = re.search("\S", right)
    if search_results is not None:
        index = search_results.start()
    else:
        index = 0
    while right.find("$", index) != -1:
        dollar_index = right.find("$", index)
        remainder = right[index:dollar_index]
        if remainder:
            result.append(remainder)
        
        if right[dollar_index + 1] == "{":
            closing_brace_index = right.find("}", dollar_index)
            if closing_brace_index == -1:
                errors.append(MissingClosingBrace(line_number, len(left) + len(_split_string) + dollar_index + 2))
                return
            end_of_non_terminal = closing_brace_index + 1
            non_terminal_name = right[dollar_index + 2:closing_brace_index]
        else:
            end_of_non_terminal = dollar_index + 1
            while is_non_terminal_char(right, end_of_non_terminal):
                end_of_non_terminal += 1
            non_terminal_name = right[dollar_index + 1:end_of_non_terminal]
        result.append(NonTerminal(non_terminal_name))
        
        index = end_of_non_terminal
    
    remainder = right[index:].rstrip()
    if remainder:
        result.append(remainder)
    rule_set.add(NonTerminal(left[1:].strip()), *result)

def is_non_terminal_char(string, index):
    return string[index:index + 1] in _non_terminal_chars and len(string) > index
