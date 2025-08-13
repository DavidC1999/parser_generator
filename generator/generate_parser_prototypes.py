from grammar import *

def generate_prototypes():
    parse_prototypes = ""

    for node in grammar:
        parse_prototypes += f"node* parse_{node.name}(memory_arena* arena, linked_list* tokens);\n"
    
    return parse_prototypes