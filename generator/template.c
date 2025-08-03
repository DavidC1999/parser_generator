// THIS CODE HAS BEEN GENERATED. DO NOT MODIFY BY HAND.

#include <stdlib.h>
#include "parser.h"
#include "memory_arena.h"
#include "tokenizer.h"
#include "linked_list.h"

static void panic(const char* message, token* item) {
    printf("Error on line %d: %s\n", item->line, message);
    exit(1);
}

static token* current_token(linked_list* tokens) {
    return (token*)tokens->current;
}

static void consume_token(linked_list* tokens) {
    tokens->current = tokens->current->next;
}

static void expect_token(linked_list* tokens, token_id id) {
    if (current_token(tokens)->id != id) {
        panic("Unexpected token", tokens->current);
    }
}

[functions]