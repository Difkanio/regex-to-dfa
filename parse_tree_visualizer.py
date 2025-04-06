from parser_nodes import *

INDENT_PREFIX = ' '
INDENT_SYMBOL = '-'
INDENT_INCREMENT = 2

class ParseTreeVisualizer:
    def visualize(self, parse_tree):
        self.visualize_node(parse_tree)

    def visualize_node(self, node, indent = 1):
        assert isinstance(node, (NonTerminalNode, TerminalNode))

        print((indent - 1) * INDENT_PREFIX + INDENT_SYMBOL + " ", end='')

        if isinstance(node, NonTerminalNode):
            print(type(node).__name__.removesuffix('Node'))
            for child in node.children:
                self.visualize_node(child, indent + INDENT_INCREMENT)
        elif isinstance(node, TerminalNode):
            print(f'TOKEN < {node.token_type} ⟚  {node.value}')