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

[function]
