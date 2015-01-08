#ifndef LIST_H
#define LIST_H

#include <stdio.h>

/* Forward declare a type "point" to be a struct. */
typedef struct point point;
/* Declare the struct with integer members x, y */
struct point {
   int    x;
   int    y;
};

typedef struct list_element list_element;
struct list_element {
   point *p;
   list_element * next;
};


void list_push_front(list_element **list, point *p);
void list_clean(list_element **list);
void list_print(list_element *list);

#endif //LIST_H
