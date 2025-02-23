/*---------------------------------------------------------------------*/
/* builtin.c                                                           */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#define _GNU_SOURCE

#include "dynarray.h"
#include "token.h"
#include "command.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <assert.h>

enum {MAX_PATH = 1024};
enum {DECIMAL = 10};

/* name of the shell that is running these commands */
extern char* pcShell;

/*---------------------------------------------------------------------*/

/* Implement cd. Check if the number of arguments in command AO is 
   correct and change directory accordingly. */

void builtin_callCD(void) {
   int iLength;
   int iRet;
   char** acArgs;
   char* pcDest;
   char* pcCommand;  

   iLength = Command_getArgsLength();
   pcCommand = Command_getCommand();
   if (iLength > 2) {
      fprintf(stderr, "%s: %s: Too many arguments.\n", 
              pcShell, pcCommand);
      return;
   }

   /* If cd had no command-line argument, go to home directory. */
   if (iLength == 1) {
      pcDest = getenv("HOME");
      if (pcDest == NULL) {
         fprintf(stderr, "%s: %s: No such file or directory. \n", 
                 pcShell, pcCommand); 
         return;
      }
      iRet = chdir(pcDest);
      if (iRet == -1) fprintf(stderr, "%s: %s: %s\n", 
                              pcShell, pcCommand, strerror(errno));
      return;
   }

   /* If cd has an argument, go to specified directory. */
   acArgs = Command_getArgs();
   assert(strcmp(acArgs[0], "cd") == 0);
   pcDest = acArgs[1];
   Command_freeArgs(acArgs);

   iRet = chdir(pcDest);
   if (iRet == -1) {
      fprintf(stderr, "%s: %s: No such file or directory.\n", 
              pcShell, pcCommand);
   }
}

/*---------------------------------------------------------------------*/

/* Implement setenv. Check if number of arguments is correct. Call
   setenv() using the array of arguments in command AO. */

void builtin_callSETENV(void) {
   int iRet;
   char** acArgs;
   int iLength;
   char* pcCommand;

   iLength = Command_getArgsLength();
   pcCommand = Command_getCommand();
   assert(strcmp(pcCommand, "setenv") == 0);

   /* Check that there are exactly 4 arguments. */
   if (iLength > 3) {
      fprintf(stderr, "%s: %s: Too many arguments.\n", 
              pcShell, pcCommand);
      return;
   }

   if (iLength < 3) {
      fprintf(stderr, "%s: %s: Too few arguments.\n", 
              pcShell, pcCommand);
      return;
   }

   acArgs = Command_getArgs();
  

   /* Call setenv(). */
   iRet = setenv(acArgs[1], acArgs[2], 1);
   if (iRet == -1) fprintf(stderr, "%s: %s: %s\n", 
                           pcShell, pcCommand, strerror(errno));
   Command_freeArgs(acArgs);
   return;
}

/*---------------------------------------------------------------------*/

/* Implement unsetenv. Check that there is only one command line 
   argument, and call unsetenv() using that argument. */

void builtin_callUNSETENV(void) {
   int iRet;
   char** acArgs;
   char* pcCommand;
   int iLength;

   pcCommand = Command_getCommand();
   iLength = Command_getArgsLength();

   /* Check that there are exactly 2 arguments. */
   if (iLength > 2) {
      fprintf(stderr, "%s: %s: Too many arguments.\n", 
              pcShell, pcCommand);
      return;
   }
   
   if (iLength < 2) {
      fprintf(stderr, "%s: %s: Too few arguments.\n", 
              pcShell, pcCommand);
      return;
   }

   /* Call unsetenv(). */
   acArgs = Command_getArgs();
   iRet = unsetenv(acArgs[1]);
   if (iRet == -1) fprintf(stderr, "%s: %s: %s\n", 
                           pcShell, pcCommand, strerror(errno));
   Command_freeArgs(acArgs);
   return;
}

/*---------------------------------------------------------------------*/

/* Call exit(0). Do not call if exit has command-line arguments. */

void builtin_callEXIT(void) {
   int iLength;
   char* pcCommand;

   pcCommand = Command_getCommand();
   iLength = Command_getArgsLength();

   /* Check that exit has no arguments. */
   if (iLength > 1) { 
      fprintf(stderr, "%s: %s: Too many arguments.\n", 
              pcShell, pcCommand); 
      return;
   }

   /* Free the command AO, then call exit(0). */
   Command_uninit();
   exit(0);
}
