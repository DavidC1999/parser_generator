#include "memory_arena.h"

#define MAX(a, b) (a > b ? a : b)

memory_arena* arena_create(size_t initial_capacity) {
    memory_arena* arena = malloc(sizeof(memory_arena));
    arena->capacity = initial_capacity;
    arena->size = 0;
    arena->buffer = malloc(initial_capacity);

    return arena;
}

void* arena_alloc(memory_arena* arena, size_t size) {
    if (arena->size + size > arena->capacity) {
        size_t new_capacity = MAX(arena->size + size, arena->capacity * 1.2);
        arena->buffer = realloc(arena->buffer, new_capacity);
    }

    void* ret_val = &arena->buffer[arena->size];
    arena->size += size;
    return ret_val;
}

void arena_reset(memory_arena* arena) {
    arena->size = 0;
}

void arena_destroy(memory_arena* arena) {
    free(arena->buffer);
    free(arena);
}
