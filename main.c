#include <stdio.h>
#include <malloc.h>

#include "tokenizer.h"

int main() {
    printf("Hello, World!\n");

    FILE * f = fopen ("../test.json", "rb");

    if (f == NULL) return 1;

    fseek (f, 0, SEEK_END);
    size_t length = ftell (f);
    fseek (f, 0, SEEK_SET);
    char* buffer = malloc(length);
    fread (buffer, 1, length, f);
    fclose (f);

    printf("%s", buffer);

    memory_arena* arena = arena_create(100);
    token_list output = {0};
    tokenize(arena, &output, buffer);

    arena_destroy(arena);

    return 0;
}
