from grammar import *

def node_enum_name(node: Node):
    return f"NODE_{node.name.upper()}"

def token_enum_name(token: Token):
    return f"TOKEN_{token.type.name.upper()}"