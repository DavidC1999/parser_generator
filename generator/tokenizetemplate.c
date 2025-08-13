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

[function]
