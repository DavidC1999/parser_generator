#include "memory_arena.h"
#include <assert.h>
#include <string.h>

void* arena_alloc(memory_arena* arena, size_t size) {
    assert(arena->size + size < arena->capacity);

    void* ret_val = &arena->buffer[arena->size];
    arena->size += size;
    memset(ret_val, 0, size);
    return ret_val;
}

void arena_reset(memory_arena* arena) {
    arena->size = 0;
}