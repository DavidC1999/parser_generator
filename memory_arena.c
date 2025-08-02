#include "memory_arena.h"
#include <assert.h>

#define MAX(a, b) (a > b ? a : b)

void* arena_alloc(memory_arena* arena, size_t size) {
    assert(arena->size + size < arena->capacity);

    void* ret_val = &arena->buffer[arena->size];
    arena->size += size;
    return ret_val;
}

void arena_reset(memory_arena* arena) {
    arena->size = 0;
}