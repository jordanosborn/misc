//http://www.chessandpoker.com/einsteins-problem-solution.html

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define l 11
#define info 20
#define people 5

const char actors[people][l] = {
    "Brit","Dane","German","Norweigen","Swede",
};

const char properties[info][l] = {
    "Blue","Green","Red","White","Yellow",
    "Beer","Coffee","Milk","Tea","Water",
    "Bluemaster","Dunhill","Pall Mall", "Prince", "Blend",
    "Cat","Bird","Dog","Fish","Horse"
};

const char categories[info + people][l] = {
    "Person","Person", "Person", "Person","Person",
    "Color","Color","Color","Color","Color",
    "Drink","Drink","Drink","Drink","Drink",
    "Cigar","Cigar","Cigar", "Cigar", "Cigar",
    "Pet","Pet","Pet","Pet","Pet"
};

#define NO 0.0
#define MAYBE 0.5
#define YES 1.0

typedef struct {
    char value[l];
    char category[l];
} node;

typedef struct {
    node* start;
    node* end;
    float value;
} edge;

typedef struct {
    node nodes[info + people];
    edge edges[people * info];
    int node_count;
    int edge_count;
} graph;

int find_node(graph* a, const char value[l]) {
    for(int i = 0; i < a -> node_count; i++) {
        if (strcmp(a -> nodes[i].value, value) == 0) return i;
    }
    return -1;
}
int find_edge(graph* a, const char start[l], const char end[l]) {
    int person = -1;
    int fact = -1;
    for(int i = 0; i < people; i++) {
        if (strcmp(actors[i], start) == 0) {
            person = i;
            break;
        }
    }
    for (int i = 0; i < info; i++) {
        if (strcmp(properties[i], end) == 0) {
            fact = i;
            break;
        }
    }
    if (person == -1 || fact == -1) return -1;
    else return (person * info) + fact;
}

void create_node(graph* a, const char value[l]) {
    strcpy(a -> nodes[a -> node_count].value, value);
    strcpy(a -> nodes[a -> node_count].category, categories[a -> node_count]);
    a -> node_count++;
}

void create_edge(graph* a, node* start, node* end, float value) {
    a -> edges[a->edge_count].start = start;
    a -> edges[a->edge_count].end = end;
    a -> edges[a->edge_count].value = value;

    a -> edge_count++;
}

graph* create_graph() {
    graph* a = (graph*) malloc(sizeof(graph));
    a -> node_count = 0;
    a -> edge_count = 0;
    for (int i = 0; i < people; i++)
        create_node(a, actors[i]);
    for (int i = 0; i< info; i++)
        create_node(a, properties[i]);
    for (int i = 0; i < people; i++) {
        for (int j = people; j < a->node_count; j++)
            create_edge(a, &a->nodes[i], &a->nodes[j], MAYBE);
    }
    return a;
}

void set_fact(graph* a, const char node[l], const char property[l], float value, bool self_exclusive, bool exclusive) {
    int pos = find_node(a, property);
    for (int i = 0; i < a -> edge_count; i++) {
        if (strcmp(a -> edges[i].end->value, property) == 0) {
            if (strcmp(a -> edges[i].start->value, node) == 0) a -> edges[i].value = value;
            else if (exclusive) a -> edges[i].value = ((value == YES) ? NO: YES);
        }
        else if (self_exclusive && strcmp(a -> edges[i].start->value, node) == 0 && strcmp(a -> edges[i].end->category, a -> nodes[pos].category) == 0)
            a -> edges[i].value = ((value == YES) ? NO: YES);
    }

}

void print_graph(graph* a){
    for (int i = 0; i< people;i++){
        printf("%s\n", a->nodes[i].value);
        for (int j = 0; j < info; j++) {
            printf("\t-> %s : %.1f\n", a->nodes[j + people].value, a -> edges[(i * info) + j].value);
        }
    }
}

int main() {
    graph* a = create_graph();
    set_fact(a, "Brit", "Horse", YES, true, true);
    print_graph(a);
    return 0;
}
