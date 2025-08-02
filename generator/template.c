#include <stdlib.h>
#include "parser.h"
#include "memory_arena.h"
#include "tokenizer.h"

static void panic(const char* message, token* item) {
    printf("Error on line %d: %s\n", item->line, message);
    exit(1);
}

static void consume_token(token_list* tokens) {
    tokens->it = tokens->it->next;
}

static void expect_token(token_list* tokens, token_id id) {
    if (tokens->it->id != id) {
        panic("Unexpected token", tokens->it);
    }
}

static void expect_and_consume_token(token_list* tokens, token_id id) {
    expect_token(tokens, id);
    consume_token(tokens);
}

[functions]