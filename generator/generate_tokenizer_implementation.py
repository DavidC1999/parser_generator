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
            raise Exception("Repeat must have at least one atom")
        return generate_condition(repeat.atoms[0])
    elif atom.is_oneof():
        oneof: OneOf = atom
        if len(oneof.atoms) == 0:
            raise Exception("OneOf must have at least one atom")
        return " || ".join([generate_condition(a) for a in oneof.atoms])
    elif atom.is_sequence():
        sequence: Sequence = atom
        return generate_condition(sequence.atoms[0])
    else:
        raise Exception(f"Unsupported in tokenizer: {atom.atom_type}")

counter = 0

def generate_atom_handling(indent_num: int, atom: Atom, break_label:str, skip_check: bool = False) -> str:
    global counter

    indent = " " * indent_num
    code = ""

    if atom.is_bound_to_field():
        code += f"{indent}const char* start = iterator;\n"

    if atom.is_string():
        string: String = atom
        _, length = escape_c_string(string.value)
        if not skip_check:
            code += f"{indent}if(!({generate_condition(atom)})) {{;\n"
            code += f"{indent}    iterator = restore_point;\n"
            code += f"{indent}    goto {break_label};\n"
            code += f"{indent}}}\n"
        code += f"{indent}iterator += {length};\n"
    elif atom.is_character_range() or atom.is_character_set():
        if not skip_check:
            code += f"{indent}if(!({generate_condition(atom)})) {{;\n"
            code += f"{indent}    iterator = restore_point;\n"
            code += f"{indent}    goto {break_label};\n"
            code += f"{indent}}}\n"
        code += f"{indent}iterator += 1;\n"
    elif atom.is_repeat():
        repeat: Repeat = atom
        
        code += f"{indent}bool loop_{counter} = true;\n"
        code += f"{indent}while(loop_{counter}) {{\n"
        for repeat_atom in repeat.atoms:
            code += f"{indent}    if ({generate_condition(repeat_atom)}) {{\n"
            code += generate_atom_handling(indent_num + 8, repeat_atom, break_label, skip_check=True)
            code += f"{indent}        continue;\n"
            code += f"{indent}    }}\n"
            code += f"{indent}    loop_{counter} = false;\n"
        code += f"{indent}}}\n"

        counter += 1
    elif atom.is_oneof():
        oneof: OneOf = atom
        
        parts = []
        for oneof_atom in oneof.atoms:
            part = ""
            part += f"if ({generate_condition(oneof_atom)}) {{\n"
            part += generate_atom_handling(indent_num + 4, oneof_atom, break_label, skip_check=True)
            part += f"{indent}}}"

            parts.append(part)

        code += indent + " else ".join(parts)
  
        if not skip_check:
            code += f" else {{\n"
            code += f"{indent}    iterator = restore_point;\n"
            code += f"{indent}    goto {break_label};\n"
            code += f"{indent}}}"
        
        code += "\n"
    elif atom.is_sequence():
        sequence: Sequence = atom
        skip_check = True
        for sequence_atom in sequence.atoms:
            code += generate_atom_handling(indent_num, sequence_atom, break_label, skip_check)
            skip_check = False
    else:
        raise Exception(f"Unsupported in tokenizer: {atom.atom_type}")
    
    if atom.is_bound_to_field():
        code += f"{indent}const char* end = iterator;\n"

    return code

def generate_interpret_field(token_type: TokenType):
    field: Field = token_type.field
    if field.is_string():
        return "convert_to_string(line, arena, start, end)"
    if field.is_integer():
        return f"({field.type})convert_to_int(line, arena, start, end)"
    if field.is_double():
        return f"convert_to_double(line, arena, start, end)"
    
    raise Exception("Unable to interpret token field data")


def generate_token_type_handling(indent_num: int, token_type: TokenType, break_label: str):
    indent = " " * indent_num
    code = ""
    code += f"{indent}new_token = arena_alloc(arena, sizeof(token));\n"
    code += f"{indent}new_token->id = {token_enum_name(token_type)};\n"
    code += f"{indent}new_token->line = line;\n"
    code += generate_atom_handling(indent_num, token_type.expression, break_label, skip_check=True)

    if token_type.field is not None:
        if token_type.field.name is not None:
            raise Exception("Token fields must not have a name")
        code += f"{indent}new_token->{token_field_name(token_type)} = {generate_interpret_field(token_type)};\n"

    return code

def generate_ignored_token_type_handling(indent_num: int, token_type: TokenType, break_label: str):
    indent = " " * indent_num
    code = ""
    code += f"{indent}// Ignored.\n"
    code += generate_atom_handling(indent_num, token_type.expression, break_label, skip_check=True)
    code += f"{indent}continue;\n"

    return code

def generate_tokenizer_implementation(template_dir: str):
    func = ""
    func += "void tokenize(memory_arena* arena, linked_list* output, const char* text) {\n"
    func += "    const char* iterator = text;\n"
    func += "    uint32_t line = 1;\n"
    func += "    const char* restore_point;\n"
    func += "    while (*iterator != '\\0') {\n"
    func += "        if (*iterator == '\\n') line++;\n"
    func += "        token* new_token;\n"

    for token_type in token_types:
        if token_type.expression == None:
            raise Exception("Token must have an expression")
        func += f"        if ({generate_condition(token_type.expression)}) {{\n"
        func += f"            restore_point = iterator;\n"
        if token_type.ignored:
            func += generate_ignored_token_type_handling(12, token_type, f"break_{token_type.name}")
        else:
            func += generate_token_type_handling(12, token_type, f"break_{token_type.name}")
        func += f"            linked_list_append(output, (list_item*)new_token);\n"
        func += f"            continue;\n"
        func += f"        }}\n"
        func += f"break_{token_type.name}:\n\n"

    func += "        panic(line, \"Unexpected character\");\n"
    func += "    }\n"
    func += "}\n"



    with open(f"{template_dir}/tokenizetemplate.c", "r") as f:
        template = f.read()

    template = template.replace("[function]", func)

    return template