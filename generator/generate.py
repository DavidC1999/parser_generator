import sys
import os
from grammar import *
from name_generators import *
from generate_parser_header import generate_parser_header
from generate_parser_implementation import generate_parser_implementation
from generate_tokenizer_header import generate_tokenizer_header
from generate_tokenizer_implementation import generate_tokenizer_implementation

print("Generating parser....")

template_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = sys.argv[1]

with open(f"{output_dir}/parser.c", "w") as f:
    f.write(generate_parser_implementation(template_dir))

with open(f"{output_dir}/parser.h", "w") as f:
    f.write(generate_parser_header(template_dir))

with open(f"{output_dir}/tokenizer.c", "w") as f:
    f.write(generate_tokenizer_implementation(template_dir))

with open(f"{output_dir}/tokenizer.h", "w") as f:
    f.write(generate_tokenizer_header(template_dir))