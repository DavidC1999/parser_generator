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

node* parse_object(memory_arena* arena, token_list* tokens) {
    node* ret_val = arena_alloc(arena, sizeof(node));
    ret_val->id = NODE_OBJECT;
    expect_token(tokens, TOKEN_OPEN_CURLY);
    consume_token(tokens);
    ret_val->object.children[0] = parse_member(arena, tokens);
    expect_token(tokens, TOKEN_CLOSE_CURLY);
    consume_token(tokens);
    return ret_val;
}

node* parse_member(memory_arena* arena, token_list* tokens) {
    node* ret_val = arena_alloc(arena, sizeof(node));
    ret_val->id = NODE_MEMBER;
    expect_token(tokens, TOKEN_STRLIT);
    ret_val->member.name = (const char*)tokens->it->arg;
    consume_token(tokens);
    expect_token(tokens, TOKEN_COLON);
    consume_token(tokens);
    ret_val->member.children[0] = parse_number(arena, tokens);
    return ret_val;
}

node* parse_number(memory_arena* arena, token_list* tokens) {
    node* ret_val = arena_alloc(arena, sizeof(node));
    ret_val->id = NODE_NUMBER;
    expect_token(tokens, TOKEN_INTLIT);
    ret_val->number.value = *(int64_t*)tokens->it->arg;
    consume_token(tokens);
    return ret_val;
}

