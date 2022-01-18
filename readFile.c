#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>

//prototype
char *getWord(FILE *f);
void writeErrorLog(const char* url2);

int main (){
    FILE *f;
    char url[256] = { "keine Ahnung was ich schreiben soll" };
    f = fopen("/var/log/s0Power2vzError.log","r");    
    if (f == NULL){
        printf("File couldn't be opend\n");
        return EXIT_FAILURE;
    }
    writeErrorLog(url);
    char *word;
    do {        
        word = getWord(f);
        if (word != NULL) {
       // writeErrorLog(word);
        printf("%s ", word);
        free(word);
        } else {
            printf("--Finished--\n");
            break;//leave endless loop
        }
    }while (true);
    writeErrorLog(url);
    free (word);
    return EXIT_SUCCESS;
}

/**
 * @brief Get the Word object, without semicolons and linebreaks
 * 
 * @param f 
 * @return char* 
 */
char *getWord(FILE *f){
    int i=0, c=1 ;
    char *word = NULL;
    char character;
    const int maxLen = 100;
    if (c> 1) printf ("-->next run\n");
    word = malloc (sizeof(char) * maxLen);
       
    do {
        character = getc(f);
        if (character == EOF ){
            free(word);
            word = NULL;
            break;
        } 
        if (i > (maxLen*c-1)){
            printf ("word is too long, expand 'memory'\n");
            c++;
            word= realloc(word, sizeof(char) * maxLen * c );
        } 
        if (character != '\n'){
            word[i++] = character;
        } else {
                break;
        }    
    } while (true);
    return word;
}

void writeErrorLog(const char* command) {
  FILE* fptr;
  // opening file in writing mode
  fptr = fopen("/var/tmp/s0Power2vzError.log", "a");//append text
  // exiting program 
  if (fptr == NULL) {
    perror("Couldn't open File");
    exit(1);
  }
  fprintf(fptr, "%s\n", command);
  fclose(fptr);
}