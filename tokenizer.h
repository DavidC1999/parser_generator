#ifndef TOKENIZER_H
#define TOKENIZER_H

#include "memory_arena.h"

typedef enum {
    TOKEN_NONE,
    TOKEN_OPEN_CURLY,
    TOKEN_CLOSE_CURLY,
    TOKEN_COLON,
    TOKEN_STRLIT,
    TOKEN_INTLIT
} token_id;

typedef struct token {
    struct token* next;
    token_id id;
    void* arg;
    int32_t line;
} token;

typedef struct {
    token* head;
    token* tail;
    token* it;
} token_list;

void tokenize(memory_arena* arena, token_list* tokens, const char* text);

#endif //TOKENIZER_H
