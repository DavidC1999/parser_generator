// THIS CODE HAS BEEN GENERATED. DO NOT MODIFY BY HAND.

#include "tokenizer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char* create_null_terminated_string(memory_arena* arena, const char* start, const char* end) {
    size_t size = end - start + 1;
    char* new_string = arena_alloc(arena, size);
    memcpy(new_string, start, size);
    new_string[size - 1] = '\0';

    return new_string;
}

static bool is_character_range(char c, char from, char to) {
    return c >= from && c <= to;
}

static bool is_character_set(char c, const char* set) {
    size_t len = strlen(set);
    for (size_t i = 0; i < len; i++) {
        if (c == set[i]) {
            return true;
        }
    }

    return false;
}

static void panic(const char* text) {
    printf("Tokenizer error: %s\n", text);
    exit(1);
}

void tokenize(memory_arena* arena, linked_list* output, const char* text) {
    const char* iterator = text;
    uint32_t line = 1;
    while (*iterator != '\0') {
        if (*iterator == '\n') line++;
        token* new_token;
        if (0) {
        } else if (is_character_set(*iterator, " \\n\\t")) {
            // Ignored.
            iterator += 1;
            continue;
        } else if (strncmp(iterator, "{", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_OPEN_CURLY;
            new_token->line = line;
            const char* start = iterator;
            iterator += 1;
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        } else if (strncmp(iterator, "}", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_CLOSE_CURLY;
            new_token->line = line;
            const char* start = iterator;
            iterator += 1;
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        } else if (strncmp(iterator, "[", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_OPEN_SQUARE;
            new_token->line = line;
            const char* start = iterator;
            iterator += 1;
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        } else if (strncmp(iterator, "]", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_CLOSE_SQUARE;
            new_token->line = line;
            const char* start = iterator;
            iterator += 1;
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        } else if (strncmp(iterator, ",", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_COMMA;
            new_token->line = line;
            const char* start = iterator;
            iterator += 1;
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        } else if (strncmp(iterator, ":", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_COLON;
            new_token->line = line;
            const char* start = iterator;
            iterator += 1;
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        } else if (strncmp(iterator, "\"", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_STRLIT;
            new_token->line = line;
            const char* start = iterator;
            iterator += 1;
            bool loop = true;
            while(loop) {
                if (is_character_range(*iterator, 'a', 'z') || is_character_range(*iterator, 'A', 'Z') || is_character_range(*iterator, '0', '9') || strncmp(iterator, "\\\"", 2) == 0 || is_character_set(*iterator, "!@#$%^&*()`~/*-\\")) {
                    if (is_character_range(*iterator, 'a', 'z')) {
                        iterator += 1;
                    } else if (is_character_range(*iterator, 'A', 'Z')) {
                        iterator += 1;
                    } else if (is_character_range(*iterator, '0', '9')) {
                        iterator += 1;
                    } else if (strncmp(iterator, "\\\"", 2) == 0) {
                        iterator += 2;
                    } else if (is_character_set(*iterator, "!@#$%^&*()`~/*-\\")) {
                        iterator += 1;
                    }
                    continue;
                }
                loop = false;
            }
            if(!(strncmp(iterator, "\"", 1) == 0)) {;
                panic("Unexpected character");
            }
            iterator += 1;
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        } else if (is_character_range(*iterator, '0', '9')) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_INTLIT;
            new_token->line = line;
            const char* start = iterator;
            bool loop = true;
            while(loop) {
                if (is_character_range(*iterator, '0', '9')) {
                    iterator += 1;
                    continue;
                }
                loop = false;
            }
            const char* end = iterator;
            new_token->value = create_null_terminated_string(arena, start, end);
        }
        linked_list_append(output, (list_item*)new_token);
    }
}

