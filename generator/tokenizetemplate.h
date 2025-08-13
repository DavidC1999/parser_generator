// THIS CODE HAS BEEN GENERATED. DO NOT MODIFY BY HAND.

#ifndef TOKENIZER_H
#define TOKENIZER_H

#include <stdint.h>

#include "memory_arena.h"
#include "linked_list.h"

[enum]

typedef struct token {
    token_id id;
    size_t value_size;
    const char* value;
    uint32_t line;
} token;

void tokenize(memory_arena* arena, linked_list* output, const char* text);

#endif // TOKENIZER_H
