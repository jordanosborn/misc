//http://www.chessandpoker.com/einsteins-problem-solution.html

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>

#define l 11
#define info 20
#define people 5
#define category_length 5

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

#define NO -1
#define MAYBE 0
#define YES 1

typedef struct {
    char value[l];
    char category[l];
} node;

typedef struct {
    node* start;
    node* end;
    int value;
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


//needs work setting exclusive etc
void set_condition(graph* a, const char first[l], const char second[l], bool equality) {
    char p[people][l];
    int val[people];
    int counter = 0;
    for (int i = 0; i < a -> edge_count; i++) {
        if (strcmp(a -> edges[i].end -> value, first) == 0) {
            if (a->edges[i].value == NO) {
                strcpy(p[counter], a->edges[i].start -> value);
                val[counter] = NO;
            }
            else if(a->edges[i].value == MAYBE) {
                strcpy(p[counter], a->edges[i].start -> value);
                val[counter] = MAYBE;
            }
            else if(a->edges[i].value == YES) {
                strcpy(p[counter], a->edges[i].start -> value);
                val[counter] = YES;
            }
            counter += 1;
        }
    }
    for (int i = 0; i< people; i++) {
        for (int j = 0; j < a -> edge_count; j++)
            if (strcmp(p[i], a->edges[j].start->value) == 0 && strcmp(second, a->edges[j].end->value) == 0) {
                if(a->edges[j].value != MAYBE) {
                    if (a->edges[find_edge(a, p[i], first)].value != MAYBE) assert(a->edges[j].value == a->edges[find_edge(a, p[i], first)].value);
                    else
                        a->edges[find_edge(a, p[i], first)].value = (equality)? a->edges[j].value: - a->edges[j].value;
                }
                else
                    a->edges[j].value = (equality) ? val[i]: - val[i];
            }
    }
}

void print_graph(graph* a){
    int v = 0;
    for (int i = 0; i< people;i++){
        printf("%s:\n", a->nodes[i].value);
        for (int j = 0; j < info; j++) {
            if (j % category_length ==  0) printf("\t%s:\n",a->nodes[j + people].category);
            v = a -> edges[(i * info) + j].value;
            if (v == NO) continue;
            printf("\t-> %s : %i\n", a->nodes[j + people].value, v);
        }
    }
}

int main() {
    graph* a = create_graph();
    set_fact(a, "Brit", "Red", YES, true, true);
    set_fact(a, "Swede", "Dog", YES, true, true);
    set_fact(a, "Dane", "Tea", YES, true, true);
    set_fact(a, "German", "Prince", YES, true, true);
    set_condition(a, "Green", "Coffee", true);
    set_condition(a, "Pall Mall", "Bird", true);
    set_condition(a, "Yellow", "Dunhill", true);
    set_condition(a, "Bluemaster", "Beer", true);
    print_graph(a);
    return 0;
}
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


//needs work setting exclusive etc
void set_condition(graph* a, const char first[l], const char second[l], bool equality) {
    char p[people][l];
    int val[people];
    int counter = 0;
    for (int i = 0; i < a -> edge_count; i++) {
        if (strcmp(a -> edges[i].end -> value, first) == 0) {
            if (a->edges[i].value == NO) {
                strcpy(p[counter], a->edges[i].start -> value);
                val[counter] = NO;
            }
            else if(a->edges[i].value == MAYBE) {
                strcpy(p[counter], a->edges[i].start -> value);
                val[counter] = MAYBE;
            }
            else if(a->edges[i].value == YES) {
                strcpy(p[counter], a->edges[i].start -> value);
                val[counter] = YES;
            }
            counter += 1;
        }
    }
    for (int i = 0; i< people; i++) {
        for (int j = 0; j < a -> edge_count; j++)
            if (strcmp(p[i], a->edges[j].start->value) == 0 && strcmp(second, a->edges[j].end->value) == 0) {
                printf("%s - %i\n - %i", p[i], val[i], a->edges[j].value);
                if(a->edges[j].value != MAYBE) {
                    if (a->edges[find_edge(a, p[i], first)].value != MAYBE) assert(a->edges[j].value == a->edges[find_edge(a, p[i], first)].value);
                    else
                        a->edges[find_edge(a, p[i], first)].value = a->edges[j].value;
                }
                else
                    a->edges[j].value = (equality) ? val[i]: - val[i];
            }
    }
}

void print_graph(graph* a){
    int v = 0;
    for (int i = 0; i< people;i++){
        printf("%s:\n", a->nodes[i].value);
        for (int j = 0; j < info; j++) {
            if (j % category_length ==  0) printf("\t%s:\n",a->nodes[j + people].category);
            v = a -> edges[(i * info) + j].value;
            if (v == NO) continue;
            printf("\t-> %s : %i\n", a->nodes[j + people].value, v);
        }
    }
}

int main() {
    graph* a = create_graph();
    set_fact(a, "Brit", "Red", YES, true, true);
    set_fact(a, "Swede", "Dog", YES, true, true);
    set_fact(a, "Dane", "Tea", YES, true, true);
    set_fact(a, "German", "Prince", YES, true, true);
    set_condition(a, "Green", "Coffee", true);
    set_condition(a, "Pall Mall", "Bird", true);
    print_graph(a);
    return 0;
}
