#ifndef PARSER_H
#define PARSER_H

#include "memory_arena.h"
#include "tokenizer.h"

typedef enum {
    NODE_OBJECT,
    NODE_MEMBER,
    NODE_NUMBER,
} node_id;


typedef struct node {
    node_id id;
    
    union {
        struct {
            struct node* children[1];
        } object;

        struct {
            const char* name;
            struct node* children[1];
        } member;

        struct {
            int64_t value;
        } number;

    };
} node;


node* parse_object(memory_arena* arena, token_list* tokens);
node* parse_member(memory_arena* arena, token_list* tokens);
node* parse_number(memory_arena* arena, token_list* tokens);


#endif // PARSER_H
