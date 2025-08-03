#ifndef LINKED_LIST_H
#define LINKED_LIST_H

typedef struct list_item {
    struct list_item* next;
} list_item;

typedef struct {
    list_item* head;
    list_item* tail;
    list_item* current;
} linked_list;

void linked_list_append(linked_list* list, list_item* new_item);

void linked_list_clear(linked_list* list);

#endif //LINKED_LIST_H
