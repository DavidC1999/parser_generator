import sys
import os
from grammar import *
from name_generators import *
from generate_header import generate_header
from generate_implementation import generate_implementation

print("Generating parser....")

template_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = sys.argv[1]

with open(f"{output_dir}/parser.c", "w") as f:
    f.write(generate_implementation(template_dir))

with open(f"{output_dir}/parser.h", "w") as f:
        f.write(generate_header(template_dir))