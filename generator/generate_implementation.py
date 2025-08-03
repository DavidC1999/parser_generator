from typing import List
from grammar import *
from name_generators import *
from generate_parse_function import generate_parse_function

def generate_implementation(template_dir: str):
    parse_functions = ""

    for node in grammar:
        parse_functions += generate_parse_function(node)

    with open(f"{template_dir}/template.c", "r") as f:
        template_c = f.read()

    template_c = template_c.replace("[functions]", parse_functions)

    return template_c