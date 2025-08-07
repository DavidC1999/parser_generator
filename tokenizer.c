//
// Created by david on 8/2/25.
//

#include <string.h>
#include <stdlib.h>
#include <assert.h>

#include "tokenizer.h"
#include "memory_arena.h"
#include "linked_list.h"

#include <pcre.h>

#define ARRAY_LEN(arr) (sizeof(arr)/sizeof(arr[0]))

typedef struct {
    memory_arena* arena;
    linked_list* token_list;
    int32_t line;
} tokenizer;

static void new_token(tokenizer* me, token_id id, void* arg) {
    token* item = arena_alloc(me->arena, sizeof(token));
    item->id = id;
    item->arg = arg;
    item->next = NULL;
    item->line = me->line;
    linked_list_append(me->token_list, (list_item*)item);
}

static bool is_digit(char c) {
    return c >= '0' && c <= '9';
}

static bool is_skip(char c) {
    return c == ' ' ||
           c == '\t' ||
           c == '\n' ||
           c == '\r';
}

void* arg_as_str(memory_arena* arena, size_t length, const char* text) {
    char* output = arena_alloc(arena, length + 1);
    memcpy(output, text, length);
    output[length] = '\0';
    return output;
}

void* arg_as_int(memory_arena* arena, size_t length, const char* text) {
    int64_t* number = arena_alloc(arena, sizeof(int64_t));
    char* end_ptr;
    *number = strtol(text, &end_ptr, 10);
    assert(end_ptr == text + length);

    return number;
}

typedef struct {
    char* pattern;
    pcre* compiled_pattern;
    token_id id;

    void* (* argument_handler)(memory_arena*, size_t, const char*);
} token_matcher;

void panic(tokenizer* me, const char* message) {
    printf("error on line %d: %s", me->line, message);
    exit(1);
}

void tokenize(memory_arena* arena, linked_list* output, const char* text) {
    const char* current = text;

    tokenizer me = {
            .arena = arena,
            .token_list = output,
            .line = 1,
    };

    token_matcher token_matchers[] = {
            {
                    .id = TOKEN_NONE,
                    .pattern = "^[ \\n\\r\\t]+",
            },
            {
                    .id = TOKEN_OPEN_CURLY,
                    .pattern = "^{",
                    .argument_handler = NULL,
            },
            {
                    .id = TOKEN_CLOSE_CURLY,
                    .pattern = "^}",
                    .argument_handler = NULL,
            },
            {
                    .id = TOKEN_OPEN_SQUARE,
                    .pattern = "^\\[",
                    .argument_handler = NULL,
            },
            {
                    .id = TOKEN_CLOSE_SQUARE,
                    .pattern = "^\\]",
                    .argument_handler = NULL,
            },
            {
                    .id = TOKEN_COLON,
                    .pattern = "^:",
                    .argument_handler = NULL,
            },
            {
                    .id = TOKEN_COMMA,
                    .pattern = "^,",
                    .argument_handler = NULL,
            },
            {
                    .id = TOKEN_STRLIT,
                    .pattern = "^\"([^\"\\\\]*(?:\\\\.[^\"\\\\]*)*)\"",
                    .argument_handler = arg_as_str,
            },
            {
                    .id = TOKEN_INTLIT,
                    .pattern = "^([0-9]+)",
                    .argument_handler = arg_as_int,
            }
    };

    for (int32_t i = 0; i < ARRAY_LEN(token_matchers); i++) {
        const char* error;
        int error_offset;
        token_matchers[i].compiled_pattern = pcre_compile(
                token_matchers[i].pattern,
                0,
                &error,
                &error_offset,
                NULL);
        if (token_matchers[i].compiled_pattern == NULL) {
            char error_message[500];
            sprintf(error_message, "PCRE compilation failed for pattern %s offset %d: %s\n", token_matchers[i].pattern,
                    error_offset, error);
            panic(&me, error_message);
        }
    }

    while (*current != '\0') {
        if (*current == '\n') {
            me.line++;
        }

        bool matched = false;

        for (int32_t i = 0; i < ARRAY_LEN(token_matchers); i++) {
            int ovector[10];
            int rc = pcre_exec(
                    token_matchers[i].compiled_pattern,
                    NULL,
                    current,
                    (int) strlen(current),
                    0,
                    0,
                    ovector,
                    10);
            if (rc < 0) {
                // no match
                continue;
            }

            matched = true;

            int32_t full_capture_size = ovector[1] - ovector[0];
            void* arg = NULL;
            if (rc > 1) {
                if (token_matchers[i].argument_handler != NULL) {
                    int len = ovector[3] - ovector[2];
                    int offset = ovector[2];
                    arg = token_matchers[i].argument_handler(arena, len, current + offset);
                }
            }

            // token none must not be added to the list.
            if (token_matchers[i].id != TOKEN_NONE) {
                new_token(&me, token_matchers[i].id, arg);
            }

            current += full_capture_size;
        }

        if (!matched) {
            char error_message[100];
            sprintf(error_message, "Unexpected character: %c", *current);
            panic(&me, error_message);
        }
    }
}