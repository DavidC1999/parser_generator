from typing import List

class Atom:
    def __init__(self, atom_type):
        self.atom_type = atom_type
        self.binds_to = None
    
    def bind_to(self, target_name):
        self.binds_to = target_name
        return self

    def get_bound_to(self):
        return self.binds_to
    
    def is_token(self):
        return self.atom_type == "token"
    
    def is_repeat(self):
        return self.atom_type == "repeat"
    
    def is_noderef(self):
        return self.atom_type == "noderef"
    
    def is_oneof(self):
        return self.atom_type == "oneof"
    
    def is_string(self):
        return self.atom_type == "string"
    
    def is_character_set(self):
        return self.atom_type == "character_set"
    
    def is_character_range(self):
        return self.atom_type == "character_range"

class AtomList(Atom):
    # Don't use this by itself
    def __init__(self, atom_type, atoms: List[Atom]):
        super().__init__(atom_type)
        self.atoms = atoms
    
    def bind_to(self, target_name):
        super().bind_to(target_name)
        for atom in self.atoms:
            atom.bind_to(target_name)
        return self

class Repeat(AtomList):
    def __init__(self, *atoms: List[Atom]):
        super().__init__("repeat", atoms)
    
    def repr(self):
        return "OneOf"

class OneOf(AtomList):
    def __init__(self, *atoms: List[Atom]):
        super().__init__("oneof", atoms)

    
    def repr(self):
        return "OneOf"

# TOKENS:
tokenregistrations = {}

def ensure_char(*char_list: List[str]):
    for char in char_list:
        if char is None or len(char) != 1:
                raise f"Invalid character: {char}"

class TokenType:
    def __init__(self, name: str, expression: List[Atom], **kwargs):
        self.name = name
        self.expression = expression
        self.field = None
        self.ignored = False

        if "field" in kwargs:
            self.field = kwargs["field"] # string
        
        if "ignored" in kwargs:
            self.ignored = kwargs["ignored"] # bool

        tokenregistrations[name] = self
    
class String(Atom):
    def __init__(self, value: str):
        super().__init__("string")
        self.value = value

class CharacterSet(Atom):
    def __init__(self, set: str):
        super().__init__("character_set")
        self.set = set

class CharacterRange(Atom):
    def __init__(self, from_char: str, to_char: str):
        ensure_char(from_char, to_char)
        super().__init__("character_range")
        self.from_char = from_char
        self.to_char = to_char

# NODES:
class Field:
    def __init__(self, type: str, name: str):
        self.type = type
        self.name = name
    
    def is_primitive(self):
        return self.type in ["int64_t"]
    
    def is_integer(self):
        return self.type in ["int64_t"]
    
    def is_string(self):
        return self.type == "const char*"
    
    def is_pointer(self):
        return self.type.endswith("*")
    
    def is_node(self):
        return self.type == "struct node*"
    
    def is_node_list(self):
        return self.type == "LINKED_LIST_T(struct node)"
    


class Int64Field(Field):
    def __init__(self, name: str):
        super().__init__("int64_t", name)

class StringField(Field):
    def __init__(self, name: str):
        super().__init__("const char*", name)

class NodeField(Field):
    def __init__(self, name: str):
        super().__init__("struct node*", name)

class NodeListField(Field):
    def __init__(self, name: str):
        super().__init__("LINKED_LIST_T(struct node)", name)

noderegistrations = {}

class NodeType:
    def __init__(self, name: str, fields: List[Field], expression: List[Atom]):
        self.name = name
        self.fields = fields
        self.expression = expression

        noderegistrations[name] = self

class Node(Atom):
    def __init__(self, name: str):
        super().__init__("noderef")
        self.name = name
    
    def get_node_type(self) -> NodeType:
        return noderegistrations[self.name]
    
    def repr(self):
        return "NodeReference"
    
class Token(Atom):
    def __init__(self, name: str):
        super().__init__("token")
        self.name = name

    def get_token_type(self):
        return tokenregistrations[self.name]

    def repr(self):
        return "Token"