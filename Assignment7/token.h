/*---------------------------------------------------------------------*/
/* token.h                                                             */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#ifndef TOKEN_INCLUDED
#define TOKEN_INCLUDED 

#include <stddef.h>
#include "dynarray.h"

enum {INPUT_TOKEN, OUTPUT_TOKEN, REGULAR_TOKEN};

typedef struct Token *Token_T;

extern char* pcShell;

/* This copies char* tokenStart till length into a new string. 
 Not null-terminated. */

Token_T Token_newToken(char* tokenStart, size_t length);

/* Reads an array of chars and identifies separate tokens. Insert in 
   FIFO order into a Dynarray. Return NULL if unable to create a new
   dynarray, or if line a unmatched quote is present. */

DynArray_T Token_newLine(char tokens[]);


/* Return a string token. */

char* Token_getToken(Token_T oToken);


/* Returns the type of the token: input, output, regular. */

int Token_getType(Token_T oToken);


/* Free a token. Do nothing if oToken is NULL. */

void Token_freeToken(Token_T oToken);


/* Free a dynarray of tokens. */

void Token_freeLine(DynArray_T oTokens);

#endif
