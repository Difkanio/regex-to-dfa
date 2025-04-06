from lexer import *
from parser_nodes import *

class Parser:
    def __init__(self, lexer : Lexer):
        self.lexer = lexer
        self.token : Token = self.lexer.next()

    #Complexity O(n) where n is the number of tokens in the lexer
    def build_parse_tree(self):
        return self.expression()

    def next(self):
        self.token = self.lexer.next()

    def token_type(self):
        return self.token.token_type
    
    def pos(self):
        return self.lexer.source_position
    
    def peek(self):
        return self.lexer.peek()

    def consume(self, expected_token_type = None):
        if expected_token_type is not None and self.token_type() != expected_token_type:
            raise ParserError(f"Expected {expected_token_type} but got {self.token_type()}", self.pos())
        
        terminal_node = TerminalNode(self.token.token_type,self.token.value, self.pos())
        self.token = self.lexer.next()
        return terminal_node

    # expr -> term | term + expr
    def expression(self) -> ExpressionNode:
        term = self.term()
        children : list = [term]

        if self.token_type() == "+":
            children.append(self.consume("+"))
            expression = self.expression()
            children.append(expression)
        
        return ExpressionNode(children)
        

    # term -> factor | factor.term
    def term(self) -> TermNode:
        factor = self.factor()
        children : list = [factor]  
        num_parentesis = 0

        if self.token_type() == "SYMBOL" or self.token_type() == "(":
            term = self.term()
            children.append(term)
        

        return TermNode(children)
    
    #factor -> SYMBOL | '(' expression ')' | factor* | factor{group} | ε | \SYMBOL
    def factor(self) -> INode:
        children : list = []
        group_node = None
        star_nodes = []

        if self.token_type() == "EOF":
            children.append(TerminalNode("SYMBOL", "ε", self.pos))

        elif self.token_type() == "SYMBOL":
            children.append(self.consume(self.token_type()))
        
        elif self.token_type() == "(":
            children += [self.consume("("), self.expression(), self.consume(")")]

        elif self.token_type() == "+":
            children.append(TerminalNode("SYMBOL", "ε", self.pos))

        factor_node = FactorNode(children)

        if self.token_type() == "{":
            group_node = self.group()
            group_node.children = [factor_node] + group_node.children
        
        i = 0
        if self.token_type == "*":
            star_nodes[i] = StarNode([self.consume("*") + factor_node])
            i = i+1

        while self.token_type() == "*":
            star_nodes[i] = StarNode(self.consume("*"), star_nodes[i -1 ])


        
        if star_nodes[i] != None and group_node != None:
            raise ParserError(f"Invalid syntax {self.token.value} ", self.pos())
        
        if star_nodes != None:
            return star_nodes 
        elif group_node != None:
            return group_node
        else:
            return factor_node

    #group -> INT | INT, | INT,INT
    def group(self) -> GroupNode:
        children : list = [self.consume("{")]
        children.append(self.consume("INT"))
        if self.token_type() == ',':
            children.append(self.consume(","))
        if self.token_type() == "INT":
            children.append(self.consume("INT"))
        children.append(self.consume("}"))
        
        return GroupNode(children)


class ParserError(ValueError):
    def __init__(self, message: str, position: int):
        self.message: str = message
        self.position: int = position