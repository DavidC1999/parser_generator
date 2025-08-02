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

static node* parse_number(memory_arena* arena, token_list* tokens) {
    node* ret_val = arena_alloc(arena, sizeof(node));
    expect_token(tokens, TOKEN_INTLIT);
    ret_val->id = NODE_TYPE_NUMBER;
    ret_val->number.value = *(int64_t*)tokens->it->arg;

    return ret_val;
}

static node* parse_member(memory_arena* arena, token_list* tokens) {
    node* ret_val = arena_alloc(arena, sizeof(node));
    ret_val->id = NODE_TYPE_MEMBER;
    if (tokens->it->id != TOKEN_STRLIT) {
        return NULL;
    }
    ret_val->member.name = (const char*) tokens->it->arg;
    consume_token(tokens);
    expect_and_consume_token(tokens, TOKEN_COLON);
    ret_val->member.value = parse_number(arena, tokens);
    return ret_val;
}

static node* parse_object(memory_arena* arena, token_list* tokens) {
    expect_and_consume_token(tokens, TOKEN_OPEN_CURLY);
    node* ret_val = arena_alloc(arena, sizeof(node));
    ret_val->id = NODE_TYPE_OBJECT;
    ret_val->object.child = parse_member(arena, tokens);

    return ret_val;
}

node* parse(memory_arena* arena, token_list* tokens) {
    return parse_object(arena, tokens);
}