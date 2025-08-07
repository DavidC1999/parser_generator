from typing import List

class TokenType:
    def __init__(self, name: str, value_type: str | None = None):
        self.name = name
        self.value_type = value_type

class Atom:
    def __init__(self, atom_type):
        self.atom_type = atom_type
    
    def is_token(self):
        return self.atom_type == "token"
    
    def is_repeat(self):
        return self.atom_type == "repeat"
    
    def is_noderef(self):
        return self.atom_type == "noderef"
    
    def is_oneof(self):
        return self.atom_type == "oneof"

class Field:
    def __init__(self, type: str, name: str):
        self.type = type
        self.name = name
    
    def is_primitive(self):
        return self.type in ["int64_t"]
    
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

class Token(Atom):
    def __init__(self, type: TokenType, binds_to: str | None = None):
        super().__init__("token")
        self.type = type
        self.binds_to = binds_to

    def repr(self):
        return "Token"

noderegistrations = {}

class Node:
    def __init__(self, name: str, fields: List[Field], expression: List[Atom]):
        self.name = name
        self.fields = fields
        self.expression = expression

        noderegistrations[name] = self

class NodeReference(Atom):
    def __init__(self, name: str, binds_to: str | None = None):
        super().__init__("noderef")
        self.name = name
        self.binds_to = binds_to
    
    def get_node(self) -> Node:
        return noderegistrations[self.name]
    
    def repr(self):
        return "NodeReference"

class AtomList(Atom):
    # Don't use this by itself
    def __init__(self, atom_type, atoms: List[Atom]):
        super().__init__(atom_type)
        self.atoms = atoms

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