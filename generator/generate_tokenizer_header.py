from grammar import *
from name_generators import *

def generate_tokenizer_header(template_dir: str):
    enum = ""
    enum += "typedef enum token_id {\n"
    
    for token_type in token_types:
        if token_type.ignored == False:
            enum += f"    {token_enum_name(token_type)},\n"

    enum += "} token_id;\n"

    with open(f"{template_dir}/tokenizetemplate.h", "r") as f:
        template = f.read()

    template = template.replace("[enum]", enum)

    return template