//
// Created by david on 8/2/25.
//

#ifndef MEMORY_ARENA_H
#define MEMORY_ARENA_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <malloc.h>


typedef struct {
    size_t capacity;
    size_t size;
    uint8_t* buffer;
} memory_arena;

void* arena_alloc(memory_arena* arena, size_t size);

void arena_reset(memory_arena* arena);

#endif //MEMORY_ARENA_H
