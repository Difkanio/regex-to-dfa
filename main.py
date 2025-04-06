from lexer import *
from parse import *
from parse_tree_visualizer import *
from finite_automata import *
from interpreter import *


def main():
    # Example usage
    string = "(abc+((ab*+c+b*)))(abc+((ab*+ε+b*)))*+c*"
    alphabet = ["c","b","a"]

    lexer1 = Lexer(string, alphabet)
    parser : Parser = Parser(lexer1)
    parse_tree = parser.build_parse_tree()
    visualizer = ParseTreeVisualizer()
    visualizer.visualize(parse_tree)
    interpreter = Interpreter(parser.lexer.alphabet)
    dfa = interpreter.interpret(parse_tree)
    print(dfa)

if __name__ == "__main__":
    main()