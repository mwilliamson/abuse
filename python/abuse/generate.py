class NonTerminal(object):
    def __init__(self, name):
        self.name = name
        
    def __hash__(self):
        return hash(self.name)
        
    def __eq__(self, other):
        if not isinstance(other, NonTerminal):
            return False
        return self.name == other.name
        
    def __ne__(self, other):
        return not (self == other)
        
    def __str__(self):
        return "<Non-terminal: %s>" % self.name
        
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
        if left not in self._rules:
            return None
        rules = self._rules[left]
        index = selector.select(0, len(rules))
        result = rules[index]
        return map(self._to_node, result)
        
    def expand_all(self, left):
        if left not in self._rules:
            return []
        rules = self._rules[left]
        return [map(self._to_node, rule) for rule in rules]
    
    def _to_node(self, value):
        if isinstance(value, basestring):
            return TerminalNode(value)
        else:
            return NonTerminalNode(value)

class NonTerminalNode(object):
    expandable = True
    
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
    expandable = False
    
    def __init__(self, terminal):
        self._terminal = terminal
        
    def value(self):
        return self._terminal
        
    def __str__(self):
        return "<Terminal node: %s>" % self._terminal
        
    def __repr__(self):
        return str(self)
    
def generate(rule_set, selector, max_depth=float("inf")):
    sentence_node = NonTerminalNode(sentence)
    unexpanded_nodes = [sentence_node]
    result = []
    depth = -1
    
    def generate_from_all_sentences():
        all_sentences = generate_all(rule_set, max_depth)
        return all_sentences[selector.select(0, len(all_sentences))]
    
    while unexpanded_nodes:
        if depth > max_depth:
            return generate_from_all_sentences()
        depth += 1
        unexpanded_node = unexpanded_nodes.pop()
        result.append(unexpanded_node.value())
        if unexpanded_node.expandable:
            new_nodes = unexpanded_node.expand(rule_set, selector)
            if new_nodes is None:
                return generate_from_all_sentences()
            unexpanded_nodes += reversed(new_nodes)
    
    return ''.join(result)

def _generate_all_recursive(rule_set, current_result, unexpanded_nodes, max_depth):
    if max_depth == -1:
        return []
    if unexpanded_nodes:
        unexpanded_node = unexpanded_nodes.pop()
        current_result.append(unexpanded_node.value())
        if not unexpanded_node.expandable:
            return _generate_all_recursive(rule_set, current_result[:], unexpanded_nodes, max_depth)
        rules = unexpanded_node.expand_all(rule_set)
        if rules is not None:
            unflattened_results = (_generate_all_recursive(rule_set, current_result[:], unexpanded_nodes + rule[::-1], max_depth - 1) for rule in rules)
            return [result for result_set in unflattened_results for result in result_set]
        else:
            return []
    else:
        return [''.join(current_result)]

def generate_all(rule_set, max_depth=float("inf")):
    return _generate_all_recursive(rule_set, [], [NonTerminalNode(sentence)], max_depth)
