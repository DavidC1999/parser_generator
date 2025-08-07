#ifndef LINKED_LIST_H
#define LINKED_LIST_H

#include <stdint.h>

typedef struct list_item {
    struct list_item* next;
} list_item;

typedef struct {
    list_item* head;
    list_item* tail;
    list_item* current;
    uint32_t count;
} linked_list;

// Useful for defining linked lists which are easily inspectible with your debugger.
// "type" MUST be type-compatible with list_item.   
#define LINKED_LIST_T(type) \
    struct {                \
        type* head;         \
        type* tail;         \
        type* current;      \
        uint32_t count;     \
    }

void linked_list_append(linked_list* list, list_item* new_item);

void linked_list_clear(linked_list* list);

#endif //LINKED_LIST_H
