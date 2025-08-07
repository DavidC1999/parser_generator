from grammar import *
from name_generators import *

def _get_possible_tokens(atom: Atom) -> List[Token]:
    if atom.is_token():
        return [atom]
    
    if atom.is_noderef():
        as_node_ref: NodeReference = atom
        as_node: Node = as_node_ref.get_node()
        if len(as_node.expression) == 0: return[]
        return _get_possible_tokens(as_node.expression[0])
    
    if atom.is_repeat():
        as_repeat: Repeat = atom
        if len(as_repeat.expression) == 0: return[]
        return _get_possible_tokens(as_repeat.atoms[0])
    
    if atom.is_oneof():
        as_oneof: OneOf = atom
        ret_val = []
        for a in as_oneof.atoms:
            ret_val += _get_possible_tokens(a)
        return ret_val

        

def _generate_parse_atom(indent_num:int, node: Node, atom: Atom):
    code = ""
    indent = " " * indent_num
    if atom.is_token():
        token: Token = atom
        code += f"{indent}expect_token(tokens, {token_enum_name(token)});\n"
        if token.binds_to != None:
            field = next(f for f in node.fields if f.name == token.binds_to)
            if (field.type.endswith("*")): # is pointer
                code += f"{indent}ret_val->{node.name}.{field.name} = ({field.type})current_token(tokens)->arg;\n"
            else:
                code += f"{indent}ret_val->{node.name}.{field.name} = *({field.type}*)current_token(tokens)->arg;\n"
        code += f"{indent}consume_token(tokens);\n"
    elif atom.is_noderef():
        referenced_node = atom.get_node()
        code += f"{indent}linked_list_append(&children, (list_item*)parse_{referenced_node.name}(arena, tokens));\n"
    elif atom.is_repeat():
        if not atom.atoms[0].is_token():
            raise "First atom of repeat atom must be a token (for now)"
        token = atom.atoms[0]
        code += f"{indent}while (current_token(tokens)->id == {token_enum_name(token)}) {{\n"
        for repeated_atom in atom.atoms:
            code += _generate_parse_atom(indent_num + 4, node, repeated_atom)
        code += f"{indent}}}\n"
    elif atom.is_oneof():
        oneof: OneOf = atom
        code += f"{indent}switch(current_token(tokens)->id) {{\n"

        found_token_names = []
        for idx, option in enumerate(oneof.atoms):
            if not option.is_noderef():
                raise "OneOf must only contain nodereferences"
            
            referenced_node: Node = oneof.atoms[idx]

            tokens = _get_possible_tokens(option)
            for token in tokens:
                enum_name = token_enum_name(token)
                if enum_name in found_token_names:
                    raise "OneOf references do not resolve to unambiguous decision"
                
                found_token_names.append(enum_name)

                code += f"{indent}    case {enum_name}:\n"

            code += f"{indent}        linked_list_append(&children, (list_item*)parse_{referenced_node.name}(arena, tokens));\n"
            code += f"{indent}        break;\n"
        
        code += f"{indent}    default:\n"
        code += f"{indent}        panic(\"Unexpected token\", current_token(tokens));\n"
        code += f"{indent}}}\n"
        
    return code


def generate_parse_function(node: Node):
    code = ""

    code =  f"node* parse_{node.name}(memory_arena* arena, linked_list* tokens) {{\n"
    code +=  "    node* ret_val = arena_alloc(arena, sizeof(node));\n"
    code += f"    ret_val->id = {node_enum_name(node)};\n"
    code += f"    linked_list children;\n"
    code += f"    linked_list_clear(&children);\n"

    for atom in node.expression:
        code += _generate_parse_atom(4, node, atom)
    
    code += f"    ret_val->children = (node*)children.head;\n"
        
    code += "    return ret_val;\n"
    code += "}\n\n"
    
    return code