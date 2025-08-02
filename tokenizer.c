//
// Created by david on 8/2/25.
//

#include <string.h>
#include <stdlib.h>
#include "tokenizer.h"
#include "memory_arena.h"
#include "re.h"

#define ARRAY_LEN(arr) (sizeof(arr)/sizeof(arr[0]))

typedef struct {
    memory_arena* arena;
    token_list* list;
} tokenizer;

static void append(token_list* list, token* item) {
    if (list->head == NULL) {
        list->head = item;
        list->tail = item;
        return;
    }

    token* old_tail = list->tail;
    old_tail->next = item;
    list->tail = item;
}

static void new_token(tokenizer* me, token_id id, void* arg) {
    token* item = arena_alloc(me->arena, sizeof(token));
    item->id = id;
    item->arg = arg;
    append(me->list, item);
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

typedef struct {
    re_t re;
    token_id id;
} tokenmatcher;

const char* tokenize(memory_arena* arena, token_list* tokens, const char* text) {
    const char* current = text;

    tokenizer me = {
            .arena = arena,
            .list = tokens,
    };

    re_t curly = re_compile("{");

    tokenmatcher tokenmatchers[] = {
            {
                    .id = TOKEN_OPEN_CURLY,
                    .re = re_compile("{")
            },
            {
                    .id = TOKEN_CLOSE_CURLY,
                    .re = re_compile("}")
            },
            {
                    .id = TOKEN_COLON,
                    .re = re_compile(":")
            },
    };

    while (*current != '\0') {

        bool found = false;
        for (int32_t i = 0; i < ARRAY_LEN(tokenmatchers); i++) {
            int match_length;
            if (re_matchp(tokenmatchers[i].re, current, &match_length) == 0) {
                char* match = arena_alloc(arena, match_length + 1);
                memcpy(match, current, match_length);
                match[match_length + 1] = '\0';

                new_token(&me, tokenmatchers[i].id, match);
                current += match_length;

                found = true;
                break;
            }
        }

        if (found) {
            continue;
        }

        if (*current == '"') {
            current++;
            const char* start = current;
            while (*current != '\0' && *current != '"') {
                current++;
            }

            if (*current == '\0') {
                return "Unexpected end of file";
            }

            const char* end = current;

            char* copy = arena_alloc(arena, end - start + 1);
            memcpy(copy, start, end - start);
            copy[end - start] = '\0';

            new_token(&me, TOKEN_STRLIT, copy);
            current++;
            continue;
        }

        if (is_digit(*current)) {
            const char* start = current;
            while (is_digit(*current)) {
                current++;
            }
            current++;

            const char* end = current;


            int64_t* number = arena_alloc(arena, sizeof(int64_t));
            *number = strtol(start, NULL, 10);

            new_token(&me, TOKEN_INTLIT, number);
            continue;
        }

        if (is_skip(*current)) {
            current++;
            continue;
        }

        return "Unexpected character";
    }
}