from grammar import *
from name_generators import *

def generate_tokenizer_header(template_dir: str):
    enum = ""
    enum += "typedef enum token_id {\n"
    enum += "    TOKEN_NONE = 0,\n"
    
    for token_type in token_types:
        if token_type.ignored == False:
            enum += f"    {token_enum_name(token_type)},\n"

    enum += "} token_id;\n"

    struct = ""
    struct += f"typedef struct token {{\n"
    struct += f"    struct token* next;\n"
    struct += f"    token_id id;\n"
    struct += f"    uint32_t line;\n"
    struct += f"    union {{\n"
    for token_type in token_types:
        if token_type.ignored == False and token_type.field is not None:
            struct += f"        {token_type.field.type} {token_field_name(token_type)};\n"
    struct += f"    }};\n"
    struct += f"}} token;\n"

    with open(f"{template_dir}/tokenizetemplate.h", "r") as f:
        template = f.read()

    template = template.replace("[enum]", enum)
    template = template.replace("[struct]", struct)

    return template