/* Document editing engine
 *
 * The document editing engine takes an input document and performs an editing
 * operation to produce an output document.  This engine could be used in a
 * text editor or diff tool.
 *
 * Only delete operations are defined in order to keep this exercise short.
 *
 * The delete operation works as follows:
 *
 *   char *doc_delete(const char *input,
 *                    const Location *start,
 *                    const Location *end,
 *                    char **errmsg);
 *
 * For example:
 *
 *   char *errmsg = NULL;
 *   char *output = doc_delete("Hello\nworld\n",
 *                             &(Location){ .lineno = 1, .charno = 4 },
 *                             &(Location){ .lineno = 2, .charno = 4 },
 *                             &errmsg);
 *   if (output) {
 *       printf("%s", output);
 *   } else {
 *       fprintf(stderr, "error: %s\n", errmsg ? errmsg : "unknown error");
 *   }
 *   free(output);
 *   free(errmsg);
 *
 * The output is:
 *
 *   Held
 *
 * Your task is to implement the delete operation.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>

/* TODO You may include C Standard Library headers and define additional
 * structs.
 */

/**
 * Location in a document
 *
 * For example:
 *
 *   hello
 *   world
 *      ^
 *
 * This location is { .lineno = 2, .charno = 4 }.  Note that both line and
 * character numbers start at 1.
 */
typedef struct {
    unsigned lineno;    /* Line number */
    unsigned charno;    /* Character number */
} Location;

/**
 * Delete characters from @start to @end (inclusive).
 *
 * For example:
 *
 *   Hello world
 *   This is a test
 *
 * To delete the 'H' use start={1, 1}, end={1, 1}.
 *
 * To delete " world" use start={1, 6}, end={1, 11}.
 *
 * To empty the second line use start={2, 1}, end={2, 14}.  This does not
 * delete the newline character at the end of the second line.
 *
 * To delete the second line use start={2, 1}, end={2, 15}.  This includes the
 * newline character at the end of the line.
 *
 * To join the lines to "Hello worldThis is a test" use start={1, 12},
 * end={1, 12}.
 *
 * @input: input document
 * @start: start of range (inclusive)
 * @end: end of range (inclusive)
 * @errmsg: filled in if there was an error (must be freed with free(3))
 *
 * Returns: a new output document or NULL on error, must be freed with free(3).
 */
char *doc_delete(const char *input,
                 const Location *start,
                 const Location *end,
                 char **errmsg)
{
    /* TODO
     * Your code here.  Feel free to write helper functions, too.
     *
     * Do not change this function's prototype, the arguments and return type
     * are fixed.
     */
	char *output =(char*)malloc(sizeof(input)/sizeof(input[0]));
	const char *tempchar = input;
	char line = 0;
	const char *index[2]={0};
	const char * sz = 0;
	const char * ez = 0;
	int size = 0;
	index[0] = input;
	while(*tempchar !='\0'){
		if(*tempchar =='\n')
		{
			index[line+1] = (tempchar+1);
			break;
		}
		tempchar++;
	}
//	std::cout << *index[0] << *index[1] << std::endl;
//	tempchar = input;

	if(start->lineno==1)
		sz = index[start->lineno-1] + start->charno-1;
	if(start->lineno==2)
		sz = index[start->lineno-1] + start->charno-1;
	if(end->lineno==1)
		ez = index[end->lineno-1] + end->charno-1;
	if(end->lineno==2)
		ez = index[end->lineno-1] + end->charno-1;
//	std::cout << *sz << " " <<*ez<< std::endl;
	for(size=0;size<sz-input;size++)
	    output[size] = input[size];
	for(;*ez!='\0';ez++)
	    output[size++] = input[ez-input+1];
	output[size] = '\0';
//	std::cout << output <<std::endl;
	return output;
}

/* Test harness */
int main(int argc, char **argv)
{
    struct {
        const char *input;
        const Location start;
        const Location end;
        const char *output;
    } test_cases[] = {
        /* These are the examples from the comments above */
        {"Hello\nworld\n", (Location){1, 4}, (Location){2, 4}, "Held\n"},
        {"Hello world\n", (Location){1, 1}, (Location){1, 1}, "ello world\n"},
        {"Hello world\n", (Location){1, 6}, (Location){1, 11}, "Hello\n"},
        {"Hello world\nThis is a test\n",
         (Location){2, 1}, (Location){2, 14},
         "Hello world\n\n"},
        {"Hello world\nThis is a test\n",
         (Location){2, 1}, (Location){2, 15},
         "Hello world\n"},
        {"Hello world\nThis is a test\n",
         (Location){1, 12}, (Location){1, 12},
         "Hello worldThis is a test\n"},

        /* Feel free to add your own test cases... (for example error cases) */
    };
    int ret = EXIT_SUCCESS;
    size_t i;

    for (i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); i++) {
        char *errmsg = NULL;
        char *output = doc_delete(test_cases[i].input,
                                  &test_cases[i].start,
                                  &test_cases[i].end,
                                  &errmsg);

        if (!output) {
            fprintf(stderr, "Test %zu failed: %s\n",
                    i, errmsg ? errmsg : "unknown error");
            ret = EXIT_FAILURE;
        } else if (strcmp(output, test_cases[i].output)) {
            fprintf(stderr, "Test %zu output mismatch: expected \"%s\", got \"%s\"\n",
                    i, test_cases[i].output, output);
            ret = EXIT_FAILURE;
        }

        free(output);
        free(errmsg);
    }
    return ret;
}
