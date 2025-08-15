#include <stdio.h>
#include <malloc.h>

#include "tokenizer.h"
#include "parser.h"

int main() {
    printf("Hello, World!\n");

    FILE * f = fopen ("../test.json", "rb");

    if (f == NULL) return 1;

    fseek (f, 0, SEEK_END);
    size_t length = ftell (f);
    fseek (f, 0, SEEK_SET);
    char* buffer = malloc(length + 1);
    fread (buffer, 1, length, f);
    fclose (f);
    buffer[length] = '\0';

    printf("%s", buffer);

    uint8_t arena_buffer[4096];
    memory_arena arena = {.size = 0, .buffer = arena_buffer, .capacity = 4096};
    linked_list tokens = {0};
    tokenize(&arena, &tokens, buffer);

    node* root = parse_json(&arena, &tokens);

    return 0;
}
