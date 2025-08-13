from grammar import *

def node_enum_name(node: NodeType):
    return f"NODE_{node.name.upper()}"

def token_enum_name(token: Token | TokenType):
    return f"TOKEN_{token.name.upper()}"