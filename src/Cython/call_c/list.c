#include "list.h"
#include <stdio.h>
#include <stdlib.h>

void list_push_front(list_element **list, point *p) {

	list_element *el = (list_element *)malloc(sizeof(list_element));
	el->p = p;

	if (*list == NULL) {
		el->next = NULL;
		*list = el;
	} else {
		el->next = *list;
		*list = el;
	}
}

void list_clean(list_element **list){
	if (*list == NULL){
		printf("List clean!\n");
		return;
	}
	else{
		list_element *first_el = *list;
		//printf("Cleaning Point x=%d,y=%d\n",first_el->p->x,first_el->p->y);
		*list = (*list)->next;
		free(first_el);
		list_clean(list);
	}
}

void list_print(list_element *list){
	if (list == NULL)
		printf("End\n");
	else{
		printf("Point x=%d,y=%d\n",list->p->x,list->p->y);
		list_print(list->next);
	}
}

/**
 * Got to build similar function in cython!
 */
int main_test(int argc, char** args) {
	list_element *list = NULL;
	point p1 = {1,2};
	point p2 = {3,4};
	point p3 = {5,6};

	list_push_front(&list,&p1);
	list_push_front(&list,&p2);
	list_push_front(&list,&p3);

	list_print(list);

	list_clean(&list);

	list_print(list);

	return 0;
}
