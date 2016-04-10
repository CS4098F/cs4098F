/*
 * File: Traverse.c
 * Traverse graph built by parser, printing nodes visited.
 * $Id: traverse.c,v 1.1 2005/05/27 01:58:57 jnoll Exp $
 * Author: John Noll & Jigar Shah
 * Date Written: Aug 10 2003
 * Date Last Modified: Aug 11 2003
 *
 */
# include <stdio.h>
#include <stdarg.h>
# include <errno.h>
# include <stdlib.h>
# include <string.h>
# include <libgen.h>		/* basename */
# include <unistd.h>
# include <pml/scanner.h>
# include <pml/parser.h>
# include <pml/tokens.h>

#define TRUE 1
#define FALSE 0
#define MAX 512
#define MAX_COLORS 32
#define MYSIZE(A) (sizeof(A) / sizeof(A[0]))

typedef enum { FLOW = 0x1, XML=0x2, ANON=0x4} output_t;
output_t graph_type ;
typedef enum { NONE, NODES, LINKS } label_t;
label_t label_type = NONE;
typedef enum { GRAY, BLACK, WHITE } node_color_t;

int node_num = 0;
int num_of_agents =0;
char *agents [MAX];
int more = FALSE;
int counter = 0;

const char *colors[] = {"antiquewhite3","tan2","royalblue1","wheat4","brown1","chocolate","coral2",\
                        "cyan4","darkorange2","darkorchid4","deeppink3","gold4","goldenrod4","green2",\
                        "darkorchid2","lightsalmon2","maroon2","orangered1","yellow1","yellowgreen",\
                        "lightblue2","violetred4","turquoise4","tomato3","thistle4","aquamarine2","springgreen2",\
                        "slateblue", "bisque2", "salmon4","turquoise2", "violetred1"
                        };


static String usage = "\
usage: %s [options] [file ...]\n\
    -l label links\n\
    -n label nodes\n\
    -x output graph as XML \n";
/*
    -d  include dominator edges\n\
    -f  include control flow edges (default)\n\
    -m  include matching edges\n";
*/

/* Provide main with a prototype to eliminate compiler warnings. */
extern int main (
# ifdef ANSI_PROTOTYPES
    int		/* argc */,
    String []	/* argv */
# endif
);

char *node_type(int type)
{
    switch (type) {
    case (ACTION): return "action"; break;
    case (AGENT): return "agent"; break;
    case (BRANCH): return "branch"; break;
    case (ITERATION): return "iter"; break;
    case (SELECTION): return "select"; break;
    case (SEQUENCE): return "sequence"; break;
    case (PROCESS): return "process"; break;
    case (JOIN): return "join"; break;
    case (RENDEZVOUS): return "rend"; break;
    default: return "unknown"; break;

    }
}


char *node_shape(int type)
{
    switch (type) {
    case (ACTION): return "box, style=rounded"; break;
    case (AGENT): return "box, style=striped" ;break;
    case (ITERATION): return "diamond, style=filled, label=ITERATION"; break; /* XXX Never happens. */
    case (SELECTION): return "diamond, style=filled, label=SELECTION"; break;
    case (JOIN): return "diamond, style=filled, label=JOIN"; break;
    case (BRANCH): return "circle, fixedsize = true, style=filled, label=BRANCH"; break;
    case (RENDEZVOUS): return "circle, fixedsize = true, style=filled, label=RENDEZVOUS"; break;
    case (PROCESS): return "plain"; break;

    default: fprintf(stderr, "Help! %s is unknown!\n", node_type(type)); return "plaintext"; break;

    }
}

char *op_to_string(int op)
{
    switch(op) {
    case (OR): return "||"; break;
    case (AND): return "&&"; break;
    case (EQ): return "=="; break;
    case (NE): return "!="; break;
    case (LE): return "<="; break;
    case (GE): return ">="; break;
    case (LT): return "<"; break;
    case (GT): return ">"; break;
    case (NOT): return "!"; break;
    case (DOT): return "."; break;
    case (QUALIFIER): return "(qual)"; break;
    case (ID): return "ID"; break;
    }
    return "I don't know";
}

void insert_iteration_links(Node from, Node to)
{
    Node p;
    int i;

    fprintf(stderr, "LOOP: %s (%ld) -> %s (%ld)\n", from->name, (long)from,
	   to->name, (long) to);

    /* Look for an unseen node to skip to. */
    for (i = 0; (p = (Node) ListIndex(from->successors, i)); i++) {
	if ((node_color_t)p->data == WHITE) {
	    printf("%ld -> %ld [label=\"skip\", weight=0]\n", (long)to, (long)p);
	}
    }

}

void print_resources(Tree t)
{
    
    if (t) {
	if (IS_ID_TREE(t)) {
	    if (TREE_ID(t)[0] == '"') {
		int i;
		for (i = 1; i < strlen(TREE_ID(t)); i++) {
		    if (TREE_ID(t)[i] == '"') break;
		    putchar(TREE_ID(t)[i]);
		}
	    } else {
		printf("%s", TREE_ID(t));
	    }
	} else if (IS_OP_TREE(t)) {
	    print_resources(t->left);
	    if (TREE_OP(t) == DOT) {
		printf("%s", op_to_string(TREE_OP(t)));
	    } else {
		printf(" %s ", op_to_string(TREE_OP(t)));
	    }
	    print_resources(t->right);
	} else {
	    print_resources(t->right);
	    print_resources(t->right);
	}
    } else {
	printf("[]");
    }
}

void print_agents(Tree t)
{
    
    if (t) {
	if (IS_ID_TREE(t)) {
	    if (TREE_ID(t)[0] == '"') {
		int i;
		for (i = 1; i < strlen(TREE_ID(t)); i++) {
		    if (TREE_ID(t)[i] == '"') break;
		    putchar(TREE_ID(t)[i]);
		}
	    } else {
		printf("%s", TREE_ID(t));
	    }
	} else if (IS_OP_TREE(t)) {
	    print_agents(t->left);
	    if (TREE_OP(t) == DOT) {
		printf("%s", op_to_string(TREE_OP(t)));
	    } else {
		printf(" %s ", op_to_string(TREE_OP(t)));
	    }
	    print_agents(t->right);
	} else {
	    print_agents(t->left);
	    print_agents(t->right);
	}
    } else {
	printf("[No Agent]");
    }
}

int find_agent(char *name){
    int i;
    for(i=0; i<num_of_agents; i++){
        if(strcmp(agents[i],name)==0){
            break;
        }
    }
    if(i < num_of_agents){
        return i;
    }
    agents[num_of_agents] = strdup(name);

    return num_of_agents++;
}

void getagents(Tree t)
{
	if (t) {
    	if(TREE_ID(t)){
      		char *agent = strdup(TREE_ID(t));
      		int idx = find_agent(agent);
      		char *color = colors[idx%MAX_COLORS];

      		if(more){
       			printf(",style=filled, fillcolor=\"seagreen1:%s\"",color);
       			//printf(",style=striped  ,fillcolor= %s ", color);
       			more = FALSE;
       		}
      		else{
      			printf(",style=filled ,color= %s ", color);
    		}

    	}else{
    		more = TRUE;
     		getagents(t->left);
     		getagents(t->right);
     	}
    }else {
    	//to avoid segmentation error
    	//printf("[No Agent]");
    }
}


void print_link(Node from, Node to, int weight)
{

    if (weight != 0) {
	printf("%ld -> %ld [weight=%d, style=%s",
	       (long)from, (long)to, weight, weight == 0 ? "invis" : "solid");


	if (label_type == LINKS) {
	    if (!(graph_type & ANON)) {
		if (from->type == ACTION) {
		    printf(", labelfloat=\"true\", labelfontcolor=\"black\", taillabel=\"p:");
		    print_resources((from->provides));
		    printf("\"");
		}
	    }
	    if (!(graph_type & ANON)) {
		if (to->type == ACTION) {
		    printf(", labelfloat=\"true\", fontcolor=\"BLACK\", label=\"r:");
		    print_resources((to->requires));
		    printf("\"") ;
		}
	    }
	}
	printf("] ;\n") ;

    } else {
/*	printf("%ld -> %ld [label=\"again\", weight=%d, style=%s, headport=\"ne\", tailport=\"se\"] ;\n", */
	printf("%ld -> %ld [weight=%d] ;\n",
	       (long)from, (long)to, weight);
    }
}

void name_node(Node n)
{
    char buf[512];

    if (strcmp(n->name, "(anonymous)") == 0) {
	/*XXX free(n->name);*/
	sprintf(buf, "%s_%d", node_type(n->type), node_num++);
	n->name = strdup(buf);
    }

    if (n->type == PROCESS) {
	/*XXX free(n->name);*/
	n->name = strdup("start");
    }
    /* This hack detects sink. */
    if (n->next == NULL) {
	/*XXX free(n->name);*/
	n->name = strdup("end");
    }
    if (graph_type != XML) {
	printf("%ld [shape=%s, ", (long)n, node_shape(n->type));
	if (n->type == PROCESS) {
	    printf("label=\"%s\"]\n", n->name);
	} else 	if (!(graph_type & ANON) && (n->type == ACTION)) {

	    if (label_type == NODES) {
		printf("label=");
		printf("\"");
		print_resources(n->requires);
		printf(" ->\\n%s\\n-> ", n->name);
		print_resources(n->provides);
		printf("\"];\n");
	    } else {
	        printf("label=");
	    	printf("\"");
	    	print_resources(n->requires);
            printf(" ->\\n%s\\n-> ", n->name);
            print_resources(n->provides);
            printf("\\nAgent(s)\\n");
            print_agents(n->agent);
            printf("\"");
            getagents(n->agent);
	    	printf("];\n");

	    }
	} else {
	    //printf("label=\"\"];\n");
	    printf("];\n");
	}
    }
}

void has_cycle(Node n, int name)
{
    int i;
    Node child;

    n->data = (void *)GRAY;
    if (graph_type == XML) {
	printf("<%s name=\"%s\">\n", node_type(n->type), n->name);
    }
    if (name) {
	if (n->type == SELECTION || n->type == BRANCH) {
	    printf("{ rank = same;\n");
	}
	for (i = 0; (child = (Node) ListIndex(n->successors, i)); i++) {
	    name_node(child);
	}
	if (n->type == SELECTION || n->type == BRANCH) {
	    printf("}\n");
	}
    }

    for (i = 0; (child = (Node) ListIndex(n->successors, i)); i++) {
	if (graph_type != XML) {
	    if (!name) {
		print_link(n, child,
			  (node_color_t)child->data == GRAY ? 0 : 1);
	    }
	}
	if ((node_color_t)child->data == WHITE) {
	    has_cycle(child, name);
	}
    }

    if (graph_type == XML) {
	printf("</%s>\n", node_type(n->type));
    }
    n->data = (void *)BLACK;
}



void traverse(Node n, int name)
{
    Node p = n;
    /* Mark all nodes WHITE to begin. */
    while (p) {
	p->data = (void *) WHITE;
	p = p->next;
    }
    /* Look for cycles. */
    has_cycle(n, name);
}

void name_nodes(Node n)
{
    name_node(n);
    traverse(n, 1);
}


int main(int argc,String argv[]){
    //int argc;
    //String argv [ ];

    int c, status;

    filename = "-";
    status = EXIT_SUCCESS;

    while ((c = getopt (argc, argv, "adflnmxh?")) != EOF) {
	switch (c) {
	case 'a':
	    graph_type |= ANON;
	    break;

	case 'f':
	    graph_type |= FLOW;
	    break;

	case 'l':
	    label_type = LINKS;
	    break;

	case 'n':
	    label_type = NODES;
	    break;

	case 'x':
	    graph_type = XML;
	    break;

	case 'h':
	    printf (usage, argv[0]);
	    exit(EXIT_SUCCESS);
	    break;

	case '?':
	    exit(EXIT_FAILURE);
	    break;
	}
    }

    if (graph_type == 0) {
	graph_type = FLOW;
    }
    do {
	if (optind < argc) {
	    filename = argv [optind];
	    lineno = 1;
	}

	if (strcmp (filename, "-") == 0) {
	    filename = "stdin";
	    yyin = stdin;

	    if (yyparse ( ))
		status = EXIT_FAILURE;

	} else if ((yyin = fopen (filename, "r")) != NULL) {
	    if (yyparse ( ))
		status = EXIT_FAILURE;

	    fclose (yyin);

	} else {
	    fprintf (stderr, "%s: ", argv [0]);
	    perror (filename);
	    status = EXIT_FAILURE;
	}

    } while (++ optind < argc);

    if (status != EXIT_FAILURE) {
	if (program) {
	    char *p, *name = basename(filename);
	    name = strtok(name, ".");
	    for (p = name; *p; p++) {
		if (*p == '-') *p = '_';
	    }
	    if (graph_type != XML) {
	    String fname = " ";
		printf("digraph %s {\n", name);
		printf("process [shape=plaintext, label=\"%s\"];\n",fname );
	    }

	    name_nodes(program->source);
	    traverse(program->source, 0);
	    if (graph_type != XML) {
		printf("}\n");
	    }
	}
    }
    exit (status);
}
