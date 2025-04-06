from lexer import *
from parse import *
from parser_nodes import *
from finite_automata import *
import re

sub_pattern = re.compile(r'(?<!^)([A-Z])')

class Interpreter():
    def __init__(self, alphabet : list[str], special_symobls = ['+', '*', '(', ')', '{' , '}', ',', 'ε']):
        self.alphabet = alphabet + special_symobls
        self.special_symobls = special_symobls
        self.alphabet2 : list[str] = alphabet

    def remove_exccess_alphabet_transitions(self, dfa : DFA) -> DFA:
        new_transitions = {}
        for (state, symbol), next_state in dfa.transitions.items():
            if symbol in self.alphabet2:
                new_transitions[(state, symbol)] = next_state

        return DFA(new_transitions, dfa.start_state, dfa.accepting_states)

    def interpret_node(self, node) -> eNFA:
        assert isinstance(node, NonTerminalNode)
        node_class_name = type(node).__name__.removesuffix('Node')
        method_name = node_class_name
        method_name = sub_pattern.sub(r'_\1', method_name).lower()
        method = getattr(self, method_name)
        assert callable(method)
        return method(node)

    def interpret(self, parse_tree : ExpressionNode) -> DFA:
        enfa = self.expression(parse_tree)
        dfa = eNFA_to_DFA(enfa)
        dfa_minimized = minimize_dfa(dfa)
        dfa_final = self.remove_exccess_alphabet_transitions(dfa_minimized)
        return dfa_final

    def expression(self, node : NonTerminalNode) -> eNFA:
        if len(node.children) == 1:
            return self.term(node.children[0])
        elif len(node.children) == 3:
            return eNFA_union(self.term(node.children[0]), self.expression(node.children[2]))
        else:
            raise Exception("Unknown number of children in expression node")

    def term(self, node : NonTerminalNode) -> eNFA:
        if len(node.children) == 1:
            return self.interpret_node(node.children[0])
        elif len(node.children) == 2:
            return eNFA_concat(self.interpret_node(node.children[0]), self.interpret_node(node.children[1]))
        else:
            raise Exception(f"Unknown number of children in term node, {len(node.children)}")


    def factor(self, node : NonTerminalNode) -> eNFA:
        if len(node.children) == 1:
            if node.children[0].value in self.special_symobls:
                self.alphabet2.append(node.children[0].value)
            return construct_eNFA(self.alphabet, node.children[0].value)
        elif len(node.children) == 3:
            return self.expression(node.children[1])
        else:
            raise Exception(f"Unknown number of children in factor node, {len(node.children)}")


    def group(self, node : NonTerminalNode) -> eNFA:
        if len(node.children) == 4:
            enfa = self.factor(node.children[0])
            num_repeats : int = int(node.children[2].value)

            if num_repeats < 0:
                raise Exception(f"Number of repeats must be non-negative {num_repeats}")
            
            result_enfa = eNFA_repeated(enfa, num_repeats)
            return result_enfa
            
        elif len(node.children) == 5:
            enfa = self.factor(node.children[0])
            num_repeats : int = int(node.children[2].value)

            if num_repeats < 0:
                raise Exception(f"Number of repeats must be non-negative {num_repeats}")
            
            repeated_enfa = eNFA_repeated(enfa, num_repeats)
            star_enfa = eNFA_star(enfa)
            result_enfa = eNFA_concat(repeated_enfa, star_enfa)
            return result_enfa

        elif len(node.children) == 6:
            enfa = self.factor(node.children[0])
            lower_bound = int(node.children[2].value)
            upper_bound = int(node.children[4].value)

            if lower_bound < 0 or upper_bound < 0:
                raise Exception(f"Number of repeats must be non-negative {lower_bound} {upper_bound}")
            
            if lower_bound > upper_bound:
                raise Exception(f"Lower bound must be less than or equal to upper bound {lower_bound} {upper_bound}")
            
            result_enfa = eNFA_repeated(enfa, lower_bound)
            for i in range(lower_bound + 1, upper_bound + 1):
                temp = eNFA_repeated(enfa, i)
                result_enfa = eNFA_union(result_enfa, temp)

            return result_enfa

        else:
            raise Exception("Unknown number of children in group node")


    def star(self, node : NonTerminalNode) -> eNFA:
        if len(node.children) == 2:
            return eNFA_star(self.factor(node.children[1]))
        else:
            raise Exception("Unknown number of children in star node")