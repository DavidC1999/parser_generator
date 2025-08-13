from grammar_types import *

class TokenName:
    open_curly = "OPEN_CURLY"
    close_curly = "CLOSE_CURLY"
    open_square = "OPEN_SQUARE"
    close_square = "CLOSE_SQUARE"
    comma = "COMMA"
    colon = "COLON"
    strlit = "STRLIT"
    intlit = "INTLIT"

class NodeName:
    json = "json"
    primitive = "primitive"
    number = "number"
    string = "string"
    container = "container"
    array = "array"
    object = "object"
    member = "member"

token_types = [
    TokenType(
        name=None,
        expression=[CharacterSet(" \\n\\t")],
        ignored=True
    ),
    TokenType(
        name=TokenName.open_curly,
        expression=[String("{")]
    ),
    TokenType(
        name=TokenName.close_curly,
        expression=[String("}")]
    ),
    TokenType(
        name=TokenName.open_square,
        expression=[String("[")]
    ),
    TokenType(
        name=TokenName.close_square,
        expression=[String("]")]
    ),
    TokenType(
        name=TokenName.comma,
        expression=[String(",")]
    ),
    TokenType(
        name=TokenName.colon,
        expression=[String(":")]
    ),
    TokenType(
        name=TokenName.strlit,
        expression=[
            String("\""),
            Repeat(
                OneOf(
                    CharacterRange("a", "z"),
                    CharacterRange("A", "Z"),
                    CharacterRange("0", "9"),
                    String("\\\""),
                    CharacterSet("!@#$%^&*()`~/*-\\"),
                )
            ),
            String("\"")
        ],
        value_type="const char*"
    ),
    TokenType(
        name=TokenName.intlit,
        expression=[
            Repeat(
                CharacterRange("0", "9")
            )
        ],
        value_type="int64_t"
    ),
]

grammar = [
    NodeType(
        name=NodeName.json,
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                Node(NodeName.primitive),
                Node(NodeName.container),
            ).bind_to("subnode")
        ]
    ),
    NodeType(
        name=NodeName.primitive,
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                Node(NodeName.number),
                Node(NodeName.string)
            ).bind_to("subnode")
        ]
    ),
    NodeType(
        name=NodeName.number,
        fields=[
            Int64Field(name="value")
        ],
        expression=[
            Token(TokenName.intlit).bind_to("value")
        ]
    ),
    NodeType(
        name=NodeName.string,
        fields=[
            StringField("value")
        ],
        expression=[
            Token(TokenName.strlit).bind_to("value")
        ]
    ),
    NodeType(
        name=NodeName.container,
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                Node(NodeName.object),
                Node(NodeName.array),
            ).bind_to("subnode")
        ]
    ),
    NodeType(
        name=NodeName.array,
        fields=[
            NodeListField("items")
        ],
        expression=[
            Token(TokenName.open_square),
            Node(NodeName.json).bind_to("items"),
            Repeat(
                Token(TokenName.comma),
                Node(NodeName.json).bind_to("items"),
            ),
            Token(TokenName.close_square)
        ]
    ),
    NodeType(
        name=NodeName.object,
        fields=[
            NodeListField("members")
        ],
        expression=[
            Token(TokenName.open_curly),
            Node(NodeName.member).bind_to("members"),
            Repeat(
                Token(TokenName.comma),
                Node(NodeName.member).bind_to("members"),
            ),
            Token(TokenName.close_curly)
        ]
    ),
    NodeType(
        name=NodeName.member,
        fields = [
           StringField("key"),
           NodeField("value")
        ],
        expression = [
            Token(TokenName.strlit).bind_to("key"),
            Token(TokenName.colon),
            Node(NodeName.json).bind_to("value")
        ]
    ),
]