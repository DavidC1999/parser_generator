from grammar_types import *

token_open_curly = TokenType("OPEN_CURLY")
token_close_curly = TokenType("CLOSE_CURLY")
token_open_square = TokenType("OPEN_SQUARE")
token_close_square = TokenType("CLOSE_SQUARE")
token_comma = TokenType("COMMA")
token_colon = TokenType("COLON")
token_strlit = TokenType("STRLIT", "const char*")
token_intlit = TokenType("INTLIT", "int64_t")

grammar = [
    Node(
        name="json",
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                NodeReference("primitive", binds_to="subnode"),
                NodeReference("container", binds_to="subnode"),
            )
        ]
    ),
    Node(
        name="primitive",
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                NodeReference("number", binds_to="subnode"),
                NodeReference("string", binds_to="subnode")
            )
        ]
    ),
    Node(
        name="number",
        fields=[
            Int64Field(name="value")
        ],
        expression=[
            Token(token_intlit, binds_to="value")
        ]
    ),
    Node(
        name="string",
        fields=[
            StringField("value")
        ],
        expression=[
            Token(token_strlit, binds_to="value")
        ]
    ),
    Node(
        name="container",
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                NodeReference("object", binds_to="subnode"),
                NodeReference("array", binds_to="subnode"),
            )
        ]
    ),
    Node(
        name="array",
        fields=[
            NodeListField("items")
        ],
        expression=[
            Token(token_open_square),
            NodeReference("json", binds_to="items"),
            Repeat(
                Token(token_comma),
                NodeReference("json", binds_to="items"),
            ),
            Token(token_close_square)
        ]
    ),
    Node(
        name="object",
        fields=[
            NodeListField("members")
        ],
        expression=[
            Token(token_open_curly),
            NodeReference("member", binds_to="members"),
            Repeat(
                Token(token_comma),
                NodeReference("member", binds_to="members"),
            ),
            Token(token_close_curly)
        ]
    ),
    Node(
        name="member",
        fields = [
           StringField("key"),
           NodeField("value")
        ],
        expression = [
            Token(token_strlit, binds_to="key"),
            Token(token_colon),
            NodeReference("json", binds_to="value")
        ]
    ),
]