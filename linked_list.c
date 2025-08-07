#include "linked_list.h"

#include <stdlib.h>

void linked_list_append(linked_list* list, list_item* new_item) {
    list->count++;

    if (list->head == NULL) {
        list->head = new_item;
        list->tail = new_item;
        list->current = new_item;
        return;
    }

    list->tail->next = new_item;
    list->tail = new_item;
}

void linked_list_clear(linked_list* list) {
    list->head = NULL;
    list->tail = NULL;
    list->current = NULL;
    list->count = 0;
}