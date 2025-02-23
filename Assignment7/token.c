/*---------------------------------------------------------------------*/
/* token.c                                                             */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#include "token.h"
#include <assert.h>
#include "dynarray.h"
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>

enum {MIN_LENGTH = 0}; /* Dynarray length. */
enum {MAX_LINE_LENGTH = 1024};
enum Statetype {NOT_IN_TOKEN, IN_TOKEN, RE_DIR, IN_QUOTES};

struct Token{
      char* pcWord;
      int iType;
};

extern char* pcShell;

/*---------------------------------------------------------------------*/

/* Copy n characters of src into dest. dest is one larger than n, to
   allow room for the nullbyte. If a src character is a ", do not 
   copy it (but count it as part of the n characters. */

static char* Token_strncpy(char pcDest[], const char pcSrc[], 
                           size_t uiLength) {
   size_t i; /* source index */
   size_t j = 0; /* destination index */

   assert(pcSrc != NULL);
   assert(pcDest != NULL);

   for (i = 0U; i < uiLength; i++) {
      if (pcSrc[i] != '\"') {
         pcDest[j] = pcSrc[i];
         j++;
      }
   }
   for (; j <= uiLength; j++) pcDest[j] = '\0';
   return pcDest;
}

/*---------------------------------------------------------------------*/

/* This copies char* tokenStart till length into a new string. 
 Not null-terminated. */

Token_T Token_newToken(char* tokenStart, size_t length) {
   Token_T oToken;
   char* tokenCopy;

   assert(tokenStart != NULL);

   oToken = (Token_T) malloc(sizeof(struct Token));
   if (oToken == NULL) return NULL;

   /* Determine the type of the token. */
   if ((length == 1) && (*tokenStart == '<')) 
      oToken->iType = INPUT_TOKEN;
   else if ((length == 1) && (*tokenStart == '>')) 
      oToken->iType = OUTPUT_TOKEN;
   else oToken->iType = REGULAR_TOKEN;

   tokenCopy = (char*) malloc(length + 1);
   if (tokenCopy == NULL) return NULL; 
   /* Strncpy will pad the last bit with nullbyte*/
   tokenCopy = Token_strncpy(tokenCopy, tokenStart, length);

   oToken->pcWord = tokenCopy;
 
/*   fprintf(stderr, "%d\n", oToken->type);*/

   return oToken;
}

/*---------------------------------------------------------------------*/

/* Reads an array of chars and identifies separate tokens. Insert in 
   FIFO order into a Dynarray. Return NULL if unable to create a new
   dynarray, or if line a unmatched quote is present. */

DynArray_T Token_newLine(char pcTokens[]) {

   DynArray_T oNewArray;
   Token_T oNewToken;
   int i; /* this counts the ith character read */
   int iTokenStart = 0;
   size_t uiTokenSize;
   size_t uiLineSize;
   enum Statetype state = NOT_IN_TOKEN;

   assert(pcTokens != NULL);
   uiLineSize = strlen(pcTokens);
   assert(uiLineSize <= MAX_LINE_LENGTH);

   oNewArray = DynArray_new(MIN_LENGTH);
   if (oNewArray == NULL) return NULL;

   /* Read each character in pcTokens */
   for (i = 0; (size_t)i < uiLineSize; i++) {
      switch(state) {

         /* If the previous character was not in a token, update the
            state based on this character. */
         case NOT_IN_TOKEN:
            if (isspace(pcTokens[i])) state = NOT_IN_TOKEN;
            else if ((pcTokens[i] == '<') || (pcTokens[i] == '>')) {
               state = RE_DIR;
               iTokenStart = i;
            }
            else if (pcTokens[i] == '\"') {
               state = IN_QUOTES;
               iTokenStart = i;
            }
            else {
               state = IN_TOKEN;
               iTokenStart = i;
            }
            break;

         /* If the previous character was in token, update state and
            create new token as needed based on this character.  */
         case IN_TOKEN:
            if ((pcTokens[i] == '<') || (pcTokens[i] == '>')) {
               uiTokenSize = (size_t)i - (size_t)iTokenStart;
               oNewToken = Token_newToken
                  (pcTokens + iTokenStart, uiTokenSize);
               iTokenStart = i;
               DynArray_add(oNewArray, oNewToken);
               state = RE_DIR;
            }
            else if (pcTokens[i] == '\"') state = IN_QUOTES;
            else if (isspace(pcTokens[i])) {
               uiTokenSize = (size_t)i - (size_t)iTokenStart;
               oNewToken = Token_newToken
                  (pcTokens + iTokenStart, uiTokenSize);
               DynArray_add(oNewArray, oNewToken);
               state = NOT_IN_TOKEN;
            }
            else state = IN_TOKEN;
            break;

         /* If the previous character was < or >, create a token for that
            character, and update the state based on this character. */
         case RE_DIR:
            uiTokenSize = (size_t)i - (size_t)iTokenStart;
            oNewToken = Token_newToken
               (pcTokens + iTokenStart, uiTokenSize);
            DynArray_add(oNewArray, oNewToken);
            if ((pcTokens[i] == '<') || (pcTokens[i] == '>')) {
               iTokenStart = i;
               state = RE_DIR;
            }
            else if (pcTokens[i] == '\"') {
               iTokenStart = i;
               state = IN_QUOTES;
            }
            else if (isspace(pcTokens[i])) state = NOT_IN_TOKEN;
            else {
               iTokenStart = i;
               state = IN_TOKEN;
            }
            break;

         /* If the previous character was in quotation marks, stay in 
            this state unless another quotation mark is read. */
         case IN_QUOTES:
            if (pcTokens[i] == '\"') state = IN_TOKEN;
            else state = IN_QUOTES;
            break;
      }

   }
   /* Check for unmatched quote. */
   if (state == IN_QUOTES) {
      fprintf(stderr, "%s: Unmached quote.\n", pcShell);
      Token_freeLine(oNewArray);
      return NULL;
   }
   /* Check for a last token. */
   else if (state == IN_TOKEN) {
      uiTokenSize = (size_t)i - (size_t)iTokenStart;
      oNewToken = Token_newToken(pcTokens + iTokenStart, uiTokenSize);
      DynArray_add(oNewArray, oNewToken);
   }
   /* Check for a last redirection token. */
   else if (state == RE_DIR) {
      uiTokenSize = (size_t)i - (size_t)iTokenStart;
      oNewToken = Token_newToken(pcTokens + iTokenStart, uiTokenSize);
      DynArray_add(oNewArray, oNewToken);
   }
   return oNewArray;
}

/*---------------------------------------------------------------------*/

/* Return a string token. */

char* Token_getToken(Token_T oToken) {

   assert(oToken != NULL);
   return oToken->pcWord;

}

/*---------------------------------------------------------------------*/

/* Returns the type of the token: input, output, regular. */

int Token_getType(Token_T oToken) {

   assert(oToken != NULL);
   return oToken->iType;

}

/*---------------------------------------------------------------------*/

/* Free a token. Do nothing if oToken is NULL. */

void Token_freeToken(Token_T oToken) {

   if (oToken == NULL) return;
   free(oToken->pcWord);
   free(oToken);

}

/*---------------------------------------------------------------------*/

/* Free a dynarray of tokens. */

void Token_freeLine(DynArray_T oTokens) {
   int iLength;
   int i;
   Token_T oToken;

   if (oTokens == NULL) return;

   /* Free each token in the dynarray. */
   iLength = DynArray_getLength(oTokens);
   for (i = iLength - 1; i >= 0; i--) {
      oToken = DynArray_get(oTokens, i);
      Token_freeToken(oToken);
   }
   DynArray_free(oTokens);

}

