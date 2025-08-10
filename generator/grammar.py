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
    TokenType(TokenName.open_curly),
    TokenType(TokenName.close_curly),
    TokenType(TokenName.open_square),
    TokenType(TokenName.close_square),
    TokenType(TokenName.comma),
    TokenType(TokenName.colon),
    TokenType(TokenName.strlit, "const char*"),
    TokenType(TokenName.intlit, "int64_t"),
]

grammar = [
    NodeType(
        name=NodeName.json,
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                Node(NodeName.primitive, binds_to="subnode"),
                Node(NodeName.container, binds_to="subnode"),
            )
        ]
    ),
    NodeType(
        name=NodeName.primitive,
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                Node(NodeName.number, binds_to="subnode"),
                Node(NodeName.string, binds_to="subnode")
            )
        ]
    ),
    NodeType(
        name=NodeName.number,
        fields=[
            Int64Field(name="value")
        ],
        expression=[
            Token(TokenName.intlit, binds_to="value")
        ]
    ),
    NodeType(
        name=NodeName.string,
        fields=[
            StringField("value")
        ],
        expression=[
            Token(TokenName.strlit, binds_to="value")
        ]
    ),
    NodeType(
        name=NodeName.container,
        fields=[
            NodeField(name="subnode")
        ],
        expression=[
            OneOf(
                Node(NodeName.object, binds_to="subnode"),
                Node(NodeName.array, binds_to="subnode"),
            )
        ]
    ),
    NodeType(
        name=NodeName.array,
        fields=[
            NodeListField("items")
        ],
        expression=[
            Token(TokenName.open_square),
            Node(NodeName.json, binds_to="items"),
            Repeat(
                Token(TokenName.comma),
                Node(NodeName.json, binds_to="items"),
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
            Node(NodeName.member, binds_to="members"),
            Repeat(
                Token(TokenName.comma),
                Node(NodeName.member, binds_to="members"),
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
            Token(TokenName.strlit, binds_to="key"),
            Token(TokenName.colon),
            Node(NodeName.json, binds_to="value")
        ]
    ),
]