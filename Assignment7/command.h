/*---------------------------------------------------------------------*/
/* command.h                                                           */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#ifndef COMMAND_INCLUDED
#define COMMAND_INCLUDED

#include "dynarray.h"
#include "token.h"

/* Read tokens and sort them into command, arguments, or input/output. 
   Identify syntactical errors. Return TRUE if reading was successful,
   FALSE if line is empty or contains errors. Modifies all global 
   variables in this AO if appropriate tokens are read. */

int Command_readLine(DynArray_T oTokens);

/* Return all variables modified during Command_readLine to their 
   default state. Do not uninitialize the acArguments array. */

void Command_reset(void);


/* Returns the name of the command as a string. */

char* Command_getCommand(void);


/* Returns the name of the input file as a string. */

char* Command_getInput(void);


/* Returns the name of the output file as a string. */

char* Command_getOutput(void);


/* Return all of the arguments as an array of char*.  */

char** Command_getArgs(void);


/* Return the number of elements in acArguments. */

int Command_getArgsLength(void);


/* Free the array of char* created in getArgs(). */

void Command_freeArgs(char* acArgs[]);


/* Free acArguments. */

void Command_uninit(void);


#endif
