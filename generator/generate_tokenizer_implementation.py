from grammar import *
from name_generators import *

def escape_c_string(text: str) -> tuple[str, int]:
    output = ""
    length = 0
    for c in text:
        if c == "\\":
            output += "\\\\"
        elif c == "\"":
            output += "\\\""
        elif c == "\n":
            output += "\\n"
        elif c == "\r":
            output += "\\r"
        elif c == "\t":
            output += "\\t"
        else:
            output += c
        length += 1
    return (output, length)

def generate_condition(atom: Atom) -> str:
    if atom.is_string():
        string: String = atom
        c_str, length = escape_c_string(string.value)
        return f"strncmp(iterator, \"{c_str}\", {length}) == 0"
    elif atom.is_character_range():
        char_range: CharacterRange = atom
        return f"is_character_range(*iterator, '{char_range.from_char}', '{char_range.to_char}')"
    elif atom.is_character_set():
        char_set: CharacterSet = atom
        c_str, length = escape_c_string(char_set.set)
        return f"is_character_set(*iterator, \"{c_str}\")"
    elif atom.is_repeat():
        repeat: Repeat = atom
        if len(repeat.atoms) == 0:
            raise "Repeat must have at least one atom"
        return generate_condition(repeat.atoms[0])
    elif atom.is_oneof():
        oneof: OneOf = atom
        if len(oneof.atoms) == 0:
            raise "OneOf must have at least one atom"
        return " || ".join([generate_condition(a) for a in oneof.atoms])
    else:
        raise f"Unsupported in tokenizer: {atom.atom_type}"

def generate_atom_handling(indent_num: int, atom: Atom, skip_check: bool = False) -> str:
    indent = " " * indent_num
    code = ""

    if atom.is_bound_to_field():
        code += f"{indent}const char* start = iterator;\n"

    if atom.is_string():
        string: String = atom
        _, length = escape_c_string(string.value)
        if not skip_check:
            code += f"{indent}if(!({generate_condition(atom)})) {{;\n"
            code += f"{indent}    panic(line, \"Unexpected character\");\n"
            code += f"{indent}}}\n"
        code += f"{indent}iterator += {length};\n"
    elif atom.is_character_range() or atom.is_character_set():
        if not skip_check:
            code += f"{indent}if(!({generate_condition(atom)})) {{;\n"
            code += f"{indent}    panic(line, \"Unexpected character\");\n"
            code += f"{indent}}}\n"
        code += f"{indent}iterator += 1;\n"
    elif atom.is_repeat():
        repeat: Repeat = atom
        
        code += f"{indent}bool loop = true;\n"
        code += f"{indent}while(loop) {{\n"
        for repeat_atom in repeat.atoms:
            code += f"{indent}    if ({generate_condition(repeat_atom)}) {{\n"
            code += generate_atom_handling(indent_num + 8, repeat_atom, skip_check=True)
            code += f"{indent}        continue;\n"
            code += f"{indent}    }}\n"
            code += f"{indent}    loop = false;\n"
        code += f"{indent}}}\n"
    elif atom.is_oneof():
        oneof: OneOf = atom

        parts = []
        for oneof_atom in oneof.atoms:
            part = ""
            part += f"if ({generate_condition(oneof_atom)}) {{\n"
            part += generate_atom_handling(indent_num + 4, oneof_atom, skip_check=True)
            part += f"{indent}}}"

            parts.append(part)

        code += indent + " else ".join(parts)
  
        if not skip_check:
            code += f" else {{\n"
            code += f"{indent}    panic(line, \"Unexpected character\");\n"
            code += f"{indent}}}"
        
        code += "\n"
    else:
        raise f"Unsupported in tokenizer: {atom.atom_type}"
    
    if atom.is_bound_to_field():
        code += f"{indent}const char* end = iterator;\n"

    return code

def generate_interpret_field(token_type: TokenType):
    field: Field = token_type.field
    if field.is_string():
        return "convert_to_string(line, arena, start, end)"
    if field.is_integer():
        return f"({field.type})convert_to_int(line, arena, start, end)"
    
    raise "Unable to interpret token field data"


def generate_token_type_handling(token_type: TokenType):
    code = ""
    code += f"            new_token = arena_alloc(arena, sizeof(token));\n"
    code += f"            new_token->id = {token_enum_name(token_type)};\n"
    code += f"            new_token->line = line;\n"
    skip_check = True
    for atom in token_type.expression:
        code += generate_atom_handling(12, atom, skip_check)
        skip_check = False

    if token_type.field is not None:
        if token_type.field.name is not None:
            raise "Token fields must not have a name"
        code += f"            new_token->{token_field_name(token_type)} = {generate_interpret_field(token_type)};\n"

    return code

def generate_ignored_token_type_handling(token_type: TokenType):
    code = ""
    skip_check = True
    code += "            // Ignored.\n"
    for atom in token_type.expression:
        code += generate_atom_handling(12, atom, skip_check)
        skip_check = False
    code += f"            continue;\n"

    return code

def generate_tokenizer_implementation(template_dir: str):
    func = ""
    func += "void tokenize(memory_arena* arena, linked_list* output, const char* text) {\n"
    func += "    const char* iterator = text;\n"
    func += "    uint32_t line = 1;\n"
    func += "    while (*iterator != '\\0') {\n"
    func += "        if (*iterator == '\\n') line++;\n"
    func += "        token* new_token;\n"

    func += "        "
    ifs = []
    for token_type in token_types:
        if len(token_type.expression) == 0:
            raise "Token must have an expression"
        new_if = ""
        new_if += f"if ({generate_condition(token_type.expression[0])}) {{\n"
        if token_type.ignored:
            new_if += generate_ignored_token_type_handling(token_type)
        else:
            new_if += generate_token_type_handling(token_type)
        new_if += f"        }}"
        ifs.append(new_if)
    func += " else ".join(ifs)

    func += "\n"
    func += "        linked_list_append(output, (list_item*)new_token);\n"
    func += "    }\n"
    func += "}\n"



    with open(f"{template_dir}/tokenizetemplate.c", "r") as f:
        template = f.read()

    template = template.replace("[function]", func)

    return template