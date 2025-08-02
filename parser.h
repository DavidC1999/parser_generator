#ifndef PARSER_H
#define PARSER_H
#include "memory_arena.h"
#include "tokenizer.h"

typedef enum {
    NODE_TYPE_OBJECT,
    NODE_TYPE_MEMBER,
    NODE_TYPE_NUMBER
} node_id;

typedef struct node {
    node_id id;

    union {
        struct {
            int64_t value;
        } number;

        struct {
            const char* name;
            struct node* value;
        } member;

        struct {
            struct node* child;
        } object;
    };
} node;

node* parse(memory_arena* arena, token_list* tokens);

#endif //PARSER_H
