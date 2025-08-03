#ifndef TOKENIZER_H
#define TOKENIZER_H

#include "memory_arena.h"
#include "linked_list.h"

typedef enum {
    TOKEN_NONE,
    TOKEN_OPEN_CURLY,
    TOKEN_CLOSE_CURLY,
    TOKEN_COLON,
    TOKEN_COMMA,
    TOKEN_STRLIT,
    TOKEN_INTLIT
} token_id;

typedef struct token {
    struct token* next;
    token_id id;
    void* arg;
    int32_t line;
} token;

void tokenize(memory_arena* arena, linked_list* output, const char* text);

#endif //TOKENIZER_H
