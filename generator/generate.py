import re

class Token:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

tokens = [
    Token("CURLY_BRACE", "{")
]