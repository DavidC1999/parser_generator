from grammar import *

def node_enum_name(node: NodeType):
    return f"NODE_{node.name.upper()}"

def token_enum_name(token: Token | TokenType):
    return f"TOKEN_{token.name.upper()}"

def token_field_name(token: Token | TokenType):
    if isinstance(token, Token):
        token = token.get_token_type()
    
    token_type: TokenType = token
    return f"{token_type.name}_value"