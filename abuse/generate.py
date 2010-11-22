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
        return map(self._to_node, result)
        
    def expand_all(self, left):
        rules = self._rules[left]
        return [map(self._to_node, rule) for rule in rules]
    
    def _to_node(self, value):
        if isinstance(value, basestring):
            return TerminalNode(value)
        else:
            return NonTerminalNode(value)

class NonTerminalNode(object):
    def __init__(self, non_terminal):
        self._non_terminal = non_terminal
        
    def expand(self, rule_set, selector):
        return rule_set.expand(self._non_terminal, selector)
        
    def expand_all(self, rule_set):
        return rule_set.expand_all(self._non_terminal)
    
    def value(self):
        return ""
        
    def __str__(self):
        return "<Non-terminal node: %s>" % self._non_terminal
        
    def __repr__(self):
        return str(self)
    
class TerminalNode(object):
    def __init__(self, terminal):
        self._terminal = terminal
        
    def expand(self, rule_set, selector):
        return []
        
    def expand_all(self, rule_set):
        return []
        
    def value(self):
        return self._terminal
        
    def __str__(self):
        return "<Terminal node: %s>" % self._terminal
        
    def __repr__(self):
        return str(self)
    
def generate(rule_set, selector):
    sentence_node = NonTerminalNode(sentence)
    unexpanded_nodes = [sentence_node]
    result = []
    while unexpanded_nodes:
        unexpanded_node = unexpanded_nodes.pop()
        result.append(unexpanded_node.value())
        unexpanded_nodes += reversed(unexpanded_node.expand(rule_set, selector))
    
    return ''.join(result)

def generate_all(rule_set, current_result=None, unexpanded_nodes=None):
    if current_result is None:
        current_result = []
    if unexpanded_nodes is None:
        unexpanded_nodes = [NonTerminalNode(sentence)]
    
    if unexpanded_nodes:
        unexpanded_node = unexpanded_nodes.pop()
        current_result.append(unexpanded_node.value())
        rules = unexpanded_node.expand_all(rule_set)
        if rules:
            unflattened_results = (generate_all(rule_set, current_result[:], unexpanded_nodes + rule[::-1]) for rule in rules)
            return [result for result_set in unflattened_results for result in result_set]
        else:
            return generate_all(rule_set, current_result[:], unexpanded_nodes)
    else:
        return [''.join(current_result)]

def generate_all_iterative(rule_set):
    sentence_node = NonTerminalNode(sentence)
    all_unused_rules = [[[sentence_node]]]
    current_result = [""]
    all_results = []
    unexpanded_nodes = []
    unexpanded_node_history = [[]]
    while all_unused_rules:
        unused_rules = all_unused_rules[-1]
        if unused_rules:
            unused_rule = unused_rules.pop()
            first_node = unused_rule[0]
            all_unused_rules.append(first_node.expand_all(rule_set)[::-1])
            unexpanded_node_history.append(unexpanded_nodes[:])
            unexpanded_nodes += reversed(unused_rule[1:])
            current_result.append(first_node.value())
            added_node = True
        elif unexpanded_nodes and added_node:
            unexpanded_node = unexpanded_nodes.pop()
            current_result.append(unexpanded_node.value())
            all_unused_rules.append(unexpanded_node.expand_all(rule_set)[::-1])
            unexpanded_node_history.append(unexpanded_nodes[:])
            added_node = True
        else:
            if added_node:
                all_results.append(''.join(current_result))
            current_result.pop()
            all_unused_rules.pop()
            unexpanded_nodes = unexpanded_node_history.pop()
            added_node = False
            
    return all_results
