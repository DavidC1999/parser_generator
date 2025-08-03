from typing import List
from grammar import *
from name_generators import *
from generate_prototypes import generate_prototypes

def generate_header(template_dir: str):
    enum = "typedef enum {\n"

    struct = """typedef struct node {
        struct node* next;
        node_id id;
        
        union {\n"""


    for node in grammar:
        enum += f"    {node_enum_name(node)},\n"

        struct += "        struct {\n"
        for field in node.fields:
            struct += f"            {field.type} {field.name};\n"
        
        struct += f"            struct node* children;\n"
        struct += f"        }} {node.name};\n\n"

        


    enum += "} node_id;\n"

    struct += "    };\n"
    struct += "} node;\n"

    with open(f"{template_dir}/template.h", "r") as f:
        template_h = f.read()

    template_h = template_h.replace("[enum]", enum)
    template_h = template_h.replace("[struct]", struct)
    template_h = template_h.replace("[prototypes]", generate_prototypes())

    return template_h

    