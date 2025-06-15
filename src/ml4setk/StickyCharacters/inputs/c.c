#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define IN 1
#define OUT 0

int main() {
    FILE *file;
    char *filename = "example.txt";
    char c;
    int lines = 0, words = 0, chars = 0;
    int state = OUT;

    file = fopen(filename, "w");
    if (file == NULL) {
        printf("Failed to create file.\n");
        return 1;
    }
    fprintf(file, "Hello World,\nthis is a test file.\nLet's count the words.\n");
    fclose(file);

    file = fopen(filename, "r");
    if (file == NULL) {
        printf("Failed to open file %s\n", filename);
        return 1;
    }

    printf("Processing file: %s\n\n", filename);

    while ((c = fgetc(file)) != EOF) {
        chars++;
        if (c == '\n') {
            lines++;
        }
        if (isspace(c)) {
            state = OUT;
        } else if (state == OUT) {
            state = IN;
            words++;
        }
    }

    fclose(file);

    if (chars > 0 && lines == 0) {
        lines = 1;
    }

    printf("--- File Statistics ---\n");
    printf("Characters: %d\n", chars);
    printf("Words: %d\n", words);
    printf("Lines: %d\n", lines);

    return 0;
}