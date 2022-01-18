#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>

void readCurlFailure2Log();
char *getMyLine(FILE *f);

int main () {

//readCurlFailure2Log();
//return EXIT_SUCCESS;
/*********************/





	FILE *fptr;
	char * line = NULL;
	size_t len = 0;
	ssize_t read;
	char line2[255]={0};


	// opening file in append mode
	fptr = fopen("/var/log/s0Power2vzError.log", "r+");
	if (fptr == NULL) {
		perror("Couldn't open File");
		exit(EXIT_FAILURE);
	}
	printf("read Filedata via curl - ");
    char *word = NULL;
    do {        
        word = getMyLine(fptr);
        printf(" -before-- ");
        if (word != NULL) {
            printf("%s\n", word);
            free(word);
            word=NULL;
            printf("-after-- ");            
        } else {
            printf("--Finished--\n");
            break;//leave endless loop
        }
    }while (true);
    return EXIT_SUCCESS;
/********************/



    //char *word = NULL;
    char character;
    const int maxLen = 100;    
    word = malloc (sizeof(char) * maxLen);
    int i=0, c=1;

    do {
        character = getc(fptr);
        printf ("%c",character);
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
        i++;
        if (character ='\n'){

        }
    } while (character != EOF);

return 1;
/*
    while ((read = getline(&line, &len, fptr)) != -1) {
		syslog(LOG_INFO, "send data %s", line);  		
		if(res != CURLE_OK) {
			fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
		} else {
			syslog(LOG_INFO, "curl sucessfully %s", line);  
		}		
		usleep(1000);		
    }
*/    
    fclose(fptr);

    if (line) free(line);
    return 0;
}




/*
	read from errorlog and send data 
*/
void readCurlFailure2Log() {
	FILE *fptr;
	char * line = NULL;
	size_t len = 0;
	ssize_t read;



	// opening file in append mode
	fptr = fopen("/var/log/s0Power2vzError.log", "r+");
	if (fptr == NULL) {
		perror("Couldn't open File");
		exit(EXIT_FAILURE);
	}
	printf("send missing data via curl");
    while ((read = getline(&line, &len, fptr)) != -1) {
		printf("send data %s", line);  		
    }
    fclose(fptr);
    if (line) free(line);
}


/**
 * @brief Get the line object, without semicolons and linebreaks
 * 
 * @param f 
 * @return char* 
 */
char *getMyLine(FILE *f){
    int i=0, c=1 ;
    char *word = NULL;
    char character;
    const int maxLen = 255;
    if (c> 1) printf ("-->next run\n");
    word = malloc (sizeof(char) * maxLen);
    do {
        character = getc(f);
        if (character == EOF || (int)character > 128) {
           if (word) free(word);
            word = NULL;
            break;
        } 
        if (i > (maxLen*c)){
            printf ("word is too long, expand 'memory'\n");
            c++;
            word= realloc(word, sizeof(char) * maxLen * c );
        } 
        if (character != '\n'){
            word[i++] = character;
        } else {
            word[i++]='\0';
            break;
       }        
    } while (true);
    return word;
}