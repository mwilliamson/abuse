class NonTerminal(object):
    def __init__(self, name):
        self._name = name
        
    def __hash__(self):
        return hash(self._name)
        
    def __eq__(self, other):
        if not isinstance(other, NonTerminal):
            return False
        return self._name == other._name
        
    def __ne__(self, other):
        return not (self == other)
        
    def __str__(self):
        return "<Non-terminal: %s>" % self._name
        
    def __repr__(self):
        return str(self)
    
sentence = NonTerminal("SENTENCE")

class RuleSet(object):
    def __init__(self):
        self._rules = {}
    
    def add(self, left, *result):
        if left not in self._rules:
            self._rules[left] = [result]
        else:
            self._rules[left].append(result)
            
    def expand(self, left, selector):
        rules = self._rules[left]
        index = selector.select(0, len(rules))
        result = rules[index]
        def to_node(value):
            if isinstance(value, basestring):
                return TerminalNode(value)
            else:
                return NonTerminalNode(value)
        return map(to_node, result)

class NonTerminalNode(object):
    is_terminal = False
    
    def __init__(self, non_terminal):
        self._non_terminal = non_terminal
        
    def expand(self, rule_set, selector):
        return rule_set.expand(self._non_terminal, selector)
    
    def value(self):
        return ""
    
class TerminalNode(object):
    is_terminal = True
    
    def __init__(self, terminal):
        self._terminal = terminal
        
    def expand(self, rule_set, selector):
        return []
        
    def value(self):
        return self._terminal
    
def generate(rule_set, selector):
    sentence_node = NonTerminalNode(sentence)
    unexpanded_nodes = [sentence_node]
    result = []
    while unexpanded_nodes:
        unexpanded_node = unexpanded_nodes.pop()
        result.append(unexpanded_node.value())
        unexpanded_nodes += reversed(unexpanded_node.expand(rule_set, selector))
    
    return ''.join(result)
