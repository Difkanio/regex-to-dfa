class INode():
    pass

class TerminalNode(INode):
    def __init__(self, token_type, value, source_position = None):
        self.token_type = token_type
        self.value = value
        self.source_position = source_position

class NonTerminalNode():
    def __init__(self, *children): 
        if len(children) == 1 and isinstance(children[0], (list, tuple)):
            self.children = list(children[0])
        else:
            self.children = list(children)

'''
class NonTerminalNode(INode):
    def __init__(self, type : str,left : INode, right : INode = None):
        self.left = left
        self.right = right
        self.type = type
'''

class ExpressionNode(NonTerminalNode):
    pass

class TermNode(NonTerminalNode):
    pass

class FactorNode(NonTerminalNode):
    pass

class GroupNode(NonTerminalNode):
    pass

class StarNode(NonTerminalNode):
    pass