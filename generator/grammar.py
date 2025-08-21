from grammar_types import *

class TokenName:
    open_curly = "open_curly"
    close_curly = "close_curly"
    open_square = "open_square"
    close_square = "close_square"
    open_round = "open_round"
    close_round = "close_round"
    comma = "comma"
    colon = "colon"
    semicolon = "semicolon"
    plus = "plus"
    lessthan = "lessthan"
    greaterthan = "greaterthan"
    doubleequals = "doubleequals"
    equals = "equals"
    strlit = "strlit"
    symbol = "symbol"
    intlit = "intlit"
    decimallit = "decimallit"
    keyword_func = "keyword_func"
    keyword_var = "keyword_var"
    keyword_while = "keyword_while"
    keyword_if = "keyword_if"
    keyword_return = "keyword_return"

token_types = [
    TokenType(
        name=None,
        expression=CharacterSet(" \n\t"),
        ignored=True
    ),
    TokenType(
        name=TokenName.open_curly,
        expression=String("{")
    ),
    TokenType(
        name=TokenName.close_curly,
        expression=String("}")
    ),
    TokenType(
        name=TokenName.open_square,
        expression=String("[")
    ),
    TokenType(
        name=TokenName.close_square,
        expression=String("]")
    ),
    TokenType(
        name=TokenName.open_round,
        expression=String("(")
    ),
    TokenType(
        name=TokenName.close_round,
        expression=String(")")
    ),
    TokenType(
        name=TokenName.comma,
        expression=String(",")
    ),
    TokenType(
        name=TokenName.colon,
        expression=String(":")
    ),
    TokenType(
        name=TokenName.semicolon,
        expression=String(";")
    ),
    TokenType(
        name=TokenName.plus,
        expression=String("+")
    ),
    TokenType(
        name=TokenName.lessthan,
        expression=String("<")
    ),
    TokenType(
        name=TokenName.doubleequals,
        expression=String("==")
    ),
    TokenType(
        name=TokenName.equals,
        expression=String("=")
    ),
    TokenType(
        name=TokenName.keyword_var,
        expression=String("var")
    ),
    TokenType(
        name=TokenName.keyword_func,
        expression=String("func")
    ),
    TokenType(
        name=TokenName.keyword_while,
        expression=String("while")
    ),
    TokenType(
        name=TokenName.keyword_if,
        expression=String("if")
    ),
    TokenType(
        name=TokenName.keyword_return,
        expression=String("return")
    ),
    TokenType(
        name=TokenName.strlit,
        expression=Sequence(
            String("\""),
            Repeat(
                OneOf(
                    CharacterRange("a", "z"),
                    CharacterRange("A", "Z"),
                    CharacterRange("0", "9"),
                    String("\\\""),
                    CharacterSet("!@#$%^&*()`~/*-\\ _"),
                )
            ).bind_to_field(),
            String("\"")
        ),
        field=StringField()
    ),
    TokenType(
        name=TokenName.symbol,
        expression=Sequence(
            OneOf(
                CharacterRange("a", "z"),
                CharacterRange("A", "Z"),
                CharacterSet("_"),
            ),
            Repeat(
                OneOf(
                    CharacterRange("a", "z"),
                    CharacterRange("A", "Z"),
                    CharacterRange("0", "9"),
                    CharacterSet("_"),
                )
            )
        ).bind_to_field(),
        field=StringField()
    ),
    TokenType(
        name=TokenName.decimallit,
        expression=Sequence(
            Repeat(
                CharacterRange("0", "9"),
            ),
            String("."),
            Repeat(
                CharacterRange("0", "9")
            )
        ).bind_to_field(),
        field=DoubleField()
    ),
    TokenType(
        name=TokenName.intlit,
        expression=Repeat(
            CharacterRange("0", "9")
        ).bind_to_field(),
        field=Int64Field()
    ),
]

class NodeName:
    program = "program"
    vardef = "vardef"
    funcdef = "funcdef"
    statement = "statement"
    compound_statement = "compound_statement"
    func_param = "func_param" # TODO: Get rid of this node type. We must add a list field type instead for function parameters

grammar = [
    NodeType(
        name=NodeName.program,
        fields=[
            NodeListField(name="subnodes")
        ],
        expression=Repeat(
            OneOf(
                Node(NodeName.vardef),
                Node(NodeName.funcdef),
            )
        ).bind_to("subnodes")
    ),
    NodeType(
        name=NodeName.vardef,
        fields=[
            StringField(name="name")
        ],
        expression=Sequence(
            Token(TokenName.keyword_var),
            Token(TokenName.symbol).bind_to("name"),
            Token(TokenName.semicolon)
        )
    ),
    NodeType(
        name=NodeName.funcdef,
        fields=[
            StringField(name="name"),
            NodeListField(name="parameters"),
            NodeField(name="body"),
        ],
        expression=Sequence(
            Token(TokenName.keyword_func),
            Token(TokenName.symbol).bind_to("name"),
            Token(TokenName.open_round),
            OneOf(
                # TODO: This OneOf could be replaced with a Maybe() or somthing like that.
                Sequence(
                    Node(NodeName.func_param).bind_to("parameters"),
                    Repeat(
                        Token(TokenName.comma),
                        Node(NodeName.func_param).bind_to("parameters")
                    ),
                    Token(TokenName.close_round),
                ),
                Token(TokenName.close_round),
            ),
            Node(NodeName.compound_statement).bind_to("body")
        )
    ),
    NodeType(
        name=NodeName.func_param,
        fields=[
            StringField("name")
        ],
        expression=Token(TokenName.symbol).bind_to("name")
    ),
    NodeType(
        name=NodeName.compound_statement,
        fields=[
            NodeField("statements")
        ],
        expression=Sequence(
            Token(TokenName.open_curly),
            Repeat(Node(NodeName.statement)).bind_to("statements"),
            Token(TokenName.close_curly),
        )
    ),
    NodeType(
        name=NodeName.statement,
        fields=[
            NodeField("subnode")
        ],
        expression=OneOf(
            Node(NodeName.vardef)
        )
    ),
]