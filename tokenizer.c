// THIS CODE HAS BEEN GENERATED. DO NOT MODIFY BY HAND.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "tokenizer.h"

static void panic(uint32_t line, const char* text) {
    printf("Tokenizer error on line %d: %s\n", line, text);
    exit(1);
}

static const char* convert_to_string(uint32_t line, memory_arena* arena, const char* start, const char* end) {
    size_t size = end - start + 1;
    char* new_string = arena_alloc(arena, size);
    memcpy(new_string, start, size);
    new_string[size - 1] = '\0';

    return new_string;
}

static int64_t convert_to_int(uint32_t line, memory_arena* arena, const char* start, const char* end) {
    char* end_ptr;
    int64_t output = strtol(start, &end_ptr, 10);

    if (end_ptr != end) {
        panic(line, "Unable to parse int");
    }

    return output;
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

void tokenize(memory_arena* arena, linked_list* output, const char* text) {
    const char* iterator = text;
    uint32_t line = 1;
    while (*iterator != '\0') {
        if (*iterator == '\n') line++;
        token* new_token;
        if (0) {
        } else if (is_character_set(*iterator, " \n\t")) {
            // Ignored.
            iterator += 1;
            continue;
        } else if (strncmp(iterator, "{", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_OPEN_CURLY;
            new_token->line = line;
            iterator += 1;
        } else if (strncmp(iterator, "}", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_CLOSE_CURLY;
            new_token->line = line;
            iterator += 1;
        } else if (strncmp(iterator, "[", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_OPEN_SQUARE;
            new_token->line = line;
            iterator += 1;
        } else if (strncmp(iterator, "]", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_CLOSE_SQUARE;
            new_token->line = line;
            iterator += 1;
        } else if (strncmp(iterator, ",", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_COMMA;
            new_token->line = line;
            iterator += 1;
        } else if (strncmp(iterator, ":", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_COLON;
            new_token->line = line;
            iterator += 1;
        } else if (strncmp(iterator, "\"", 1) == 0) {
            new_token = arena_alloc(arena, sizeof(token));
            new_token->id = TOKEN_STRLIT;
            new_token->line = line;
            iterator += 1;
            const char* start = iterator;
            bool loop = true;
            while(loop) {
                if (is_character_range(*iterator, 'a', 'z') || is_character_range(*iterator, 'A', 'Z') || is_character_range(*iterator, '0', '9') || strncmp(iterator, "\\\"", 2) == 0 || is_character_set(*iterator, "!@#$%^&*()`~/*-\\ ")) {
                    if (is_character_range(*iterator, 'a', 'z')) {
                        iterator += 1;
                    } else if (is_character_range(*iterator, 'A', 'Z')) {
                        iterator += 1;
                    } else if (is_character_range(*iterator, '0', '9')) {
                        iterator += 1;
                    } else if (strncmp(iterator, "\\\"", 2) == 0) {
                        iterator += 2;
                    } else if (is_character_set(*iterator, "!@#$%^&*()`~/*-\\ ")) {
                        iterator += 1;
                    }
                    continue;
                }
                loop = false;
            }
            const char* end = iterator;
            if(!(strncmp(iterator, "\"", 1) == 0)) {;
                panic(line, "Unexpected character");
            }
            iterator += 1;
            new_token->strlit_value = convert_to_string(line, arena, start, end);
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
            new_token->intlit_value = (int64_t)convert_to_int(line, arena, start, end);
        }
        linked_list_append(output, (list_item*)new_token);
    }
}

