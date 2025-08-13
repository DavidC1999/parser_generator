// THIS CODE HAS BEEN GENERATED. DO NOT MODIFY BY HAND.

#ifndef TOKENIZER_H
#define TOKENIZER_H

#include <stdint.h>

#include "memory_arena.h"
#include "linked_list.h"

typedef enum token_id {
    TOKEN_OPEN_CURLY,
    TOKEN_CLOSE_CURLY,
    TOKEN_OPEN_SQUARE,
    TOKEN_CLOSE_SQUARE,
    TOKEN_COMMA,
    TOKEN_COLON,
    TOKEN_STRLIT,
    TOKEN_INTLIT,
} token_id;


typedef struct token {
    struct token* next;
    token_id id;
    uint32_t line;
    union {
        const char* strlit_value;
        int64_t intlit_value;
    };
} token;


void tokenize(memory_arena* arena, linked_list* output, const char* text);

#endif // TOKENIZER_H
