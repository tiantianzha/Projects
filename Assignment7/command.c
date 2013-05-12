/*---------------------------------------------------------------------*/
/* command.c                                                           */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#include "command.h"
#include "token.h"
#include "dynarray.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

enum {UNSEEN = -2};
enum {FALSE, TRUE};

/* States of the object. */

static char* cCommand = NULL;
static DynArray_T acArguments; 
static char* cInput = NULL;
static char* cOutput = NULL;

static int iInput = UNSEEN;
static int iOutput = UNSEEN;

static int iRead = FALSE;
static int iInit = FALSE;

extern char* pcShell;

/*---------------------------------------------------------------------*/

/* Read tokens and sort them into command, arguments, or input/output. 
   Identify syntactical errors. Return TRUE if reading was successful,
   FALSE if line is empty or contains errors. Modifies all global 
   variables in this AO if appropriate tokens are read. */

int Command_readLine(DynArray_T oTokens) {
   int iLength;
   int i;
   int iType;
   Token_T oCurrent;

   assert(oTokens != NULL);

   /* Initialize the array of arguments. */
   if (!iInit) {
      acArguments = DynArray_new(0);
      iInit = TRUE;
   }

   /* Return FALSE if oTokens is empty. */
   iLength = DynArray_getLength(oTokens);
   if (iLength == 0) return FALSE;

   iRead = TRUE;

   /* Identify command name. */
   oCurrent = DynArray_get(oTokens, 0);
   if (Token_getType(oCurrent) != REGULAR_TOKEN) {
      fprintf(stderr, "%s: Missing command name\n", pcShell);
      return FALSE;
   }
   /* Add the command name as the first element of acArguments */
   cCommand = Token_getToken(oCurrent);
   DynArray_add(acArguments, cCommand);

   /* Read each token and classify as appropriate. Do not store > or < */
   for (i = 1; i < iLength; i++) {
      oCurrent = DynArray_get(oTokens, i);
      iType = Token_getType(oCurrent);

      /* If oCurrent is an input token, mark it as seen. If an input
         token has already been seen, return FALSE. If it follows an 
         output token, return FALSE. */
      if (iType == INPUT_TOKEN) {
         if (iInput != UNSEEN) {
            fprintf(stderr, "%s: Multiple input tokens\n", pcShell);
            return FALSE;
         }
         else if (iOutput == i - 1) {
            fprintf(stderr, 
                    "%s: Standard output redirection with no file name\n",
                    pcShell);
            return FALSE;
         }
         iInput = i;
      }

      /* If oCurrent is an output token, mark it as seen. If an output
         token has already been seen, return FALSE. If it follows an
         input token, return FALSE. */
      else if (iType == OUTPUT_TOKEN) {
         if (iOutput != UNSEEN) { 
            fprintf(stderr, "%s: Multiple output tokens\n", pcShell);
            return FALSE;
         }
         else if (iInput == i - 1) {
            fprintf(stderr, 
                    "%s: Standard input redirection with no file name\n",
                    pcShell);
            return FALSE;
         }
         iOutput = i;
      }

      /* If it is a regular token, classify as appropriate. */
      else {
         if (iInput == i - 1) cInput = Token_getToken(oCurrent);    
         else if (iOutput == i - 1) cOutput = Token_getToken(oCurrent);
         else DynArray_add(acArguments, Token_getToken(oCurrent));
      }
   }

   /* If an input or output token is not followed by a regular token, 
      return FALSE. */
   if ((iInput != UNSEEN) && (cInput == NULL)) {
      fprintf(stderr, 
              "%s: Standard input redirection without file name\n", 
              pcShell);
      return FALSE; 
   }
   if ((iOutput != UNSEEN) && (cOutput == NULL)) {
      fprintf(stderr,
              "%s: Standard output redirection without file name\n",
              pcShell);
      return FALSE;
   }

   return TRUE;
}

/*---------------------------------------------------------------------*/

/* Return all variables modified during Command_readLine to their 
   default state. Do not uninitialize the acArguments array. */

void Command_reset(void) {
   char* pcToken;
   int i;
   int iLength;

   if (!iRead) return;

   iInput = UNSEEN;
   iOutput = UNSEEN;
   iRead = FALSE;

   cInput = NULL;
   cOutput = NULL;
   cCommand = NULL;

   /* Empty the acArguments array. */
   iLength = DynArray_getLength(acArguments);
   if (iLength == 0) return;
   for (i = iLength - 1; i >= 0; i--) {
      pcToken = DynArray_removeAt(acArguments, i);
      assert(pcToken != NULL);
   }
   
   assert(DynArray_getLength(acArguments) == 0);
   
   iRead = FALSE;
}

/*---------------------------------------------------------------------*/

/* Returns the name of the command as a string. */

char* Command_getCommand() {

   if (iRead == FALSE) {
      fprintf(stderr, "%s: No command read\n", pcShell);
      return NULL;
   }
   return cCommand;
}

/*---------------------------------------------------------------------*/

/* Returns the name of the input file as a string. */

char* Command_getInput() {

   assert(iInit);

   if (iRead == FALSE) {
      fprintf(stderr, "%s: No line read\n", pcShell);
      return NULL;
   }
   return cInput;

}

/*---------------------------------------------------------------------*/

/* Returns the name of the output file as a string. */

char* Command_getOutput() {

   assert(iInit);

   if (iRead == FALSE) {
      fprintf(stderr, "%s: No line read\n", pcShell);
      return NULL;
   }
   return cOutput;

}

/*---------------------------------------------------------------------*/

/* Return all of the arguments as an array of char*.  */

char** Command_getArgs() {
   int iLength;
   char** acArgsArray;

   assert(iInit);

   if (iRead == FALSE) {
      fprintf(stderr, "%s: no command read\n", pcShell);
      return NULL;
   }

   /* Create an array in which to copy the elements of acArguments. 
      Null-terminate the array. */
   iLength = DynArray_getLength(acArguments);
   acArgsArray =  malloc((iLength +1) * sizeof(char*));
   if (acArgsArray == NULL) return NULL;
   DynArray_toArray(acArguments, (void**)acArgsArray);
   acArgsArray[iLength] = NULL;
   return (char**) acArgsArray;

}

/*---------------------------------------------------------------------*/

/* Return the number of elements in acArguments. */

int Command_getArgsLength() {

   assert(iInit);
   return DynArray_getLength(acArguments);

}

/*---------------------------------------------------------------------*/

/* Free the array of char* created in getArgs(). */

void Command_freeArgs(char* acArgs[]) {

   assert(acArgs != NULL);
   free(acArgs);

}

/*---------------------------------------------------------------------*/

/* Free acArguments. */

void Command_uninit(void) {

   assert(iInit == TRUE);
   DynArray_free(acArguments);
   iInit = FALSE;

}

/*---------------------------------------------------------------------*/
/*int main(void) {
   int i, iLength;
   DynArray_T oTokens;
   char commandline[] = "command < input1 > output1";
   char* toPrint;
   char** cNewArgsArray;

   oTokens = Token_newLine(commandline);

   Command_readLine(oTokens);
   iLength = DynArray_getLength(cArguments);

   fprintf(stderr, "Command is: %s\n", cCommand);
   fprintf(stderr, "Input is: %s\n", cInput);
   fprintf(stderr, "Output is: %s\n", cOutput);
   fprintf(stderr, "Arguments are: \n");
   
   for (i = 0; i < iLength; i++) {
      toPrint = (char*) DynArray_get(cArguments, i);
      fprintf(stderr, "%s\n", toPrint);
   }

   cNewArgsArray = Command_getArgs();
   for (i = 0; i < iLength; i++) {
      fprintf(stderr, "%s\n", cNewArgsArray[i]);
   }

   for (i = 0; i < iLength; i++) {
   }

   fprintf(stderr, "Args array length is: %d\n", iLength);
   fprintf(stderr, "iInput is: %d\n", iInput);
   fprintf(stderr, "iOutput is: %d\n", iOutput);

   Command_reset();

   fprintf(stderr, "Command is: %s\n", cCommand);
   fprintf(stderr, "Input is: %s\n", cInput);
   fprintf(stderr, "Output is: %s\n", cOutput);
   fprintf(stderr, "Arguments are: \n");
   
   fprintf(stderr, "Args array length is: %d\n", DynArray_getLength(cArguments));

   fprintf(stderr, "iInput is: %d\n", iInput);
   fprintf(stderr, "iOutput is: %d\n", iOutput);


   return 0;
}
*/
