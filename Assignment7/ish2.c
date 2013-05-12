/*---------------------------------------------------------------------*/
/* ish.c                                                               */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/


#include "dynarray.h"
#include "token.h"
#include "command.h"
#include "builtin.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <errno.h>
#include <assert.h>


enum {MAX_LINE = 1024};
enum {FALSE, TRUE};
enum {PERMISSIONS = 0600};

char* pcShell;

/*---------------------------------------------------------------------*/

/* Read from StdIn. MAX_LINE is the size of array into which input must
   fit. It includes '\n' which indicates end of input, and '\0'. If 
   input exceeds specified length, print error message and discard 
   line. */

static int ish_readline(char acLine[], FILE *stream) {

   assert(acLine != NULL);
   assert(stream != NULL);   
   
   acLine = fgets(acLine, MAX_LINE, stream);
   if (acLine == NULL) return FALSE;
   return TRUE;
   
}

/*---------------------------------------------------------------------*/

/* Output redirection: replace oldstream (typically 0 or 1 for StdIn or
   StdOut) with the specified filename. */

static void ish_dup(char* cFilename, int iOldstream) {
   int iFd;
   int iRet;

   if (iOldstream == 0) iFd = open(cFilename, PERMISSIONS);
   else iFd = creat(cFilename, PERMISSIONS);
   
   if (iFd == -1) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }
   
   iRet = close(iOldstream);
   if (iRet == -1) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }

   iRet = dup(iFd);
   if (iRet == -1) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }
   
   iRet = close(iFd);
   if (iRet == -1) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }

   
}


/*---------------------------------------------------------------------*/

static void ish_executeLine(char* acLine) {
   
   int iRet;
   int iPid;
   char* pcCommand;
   char** acArgs;
   DynArray_T oTokens;
   
   oTokens = Token_newLine(acLine); /* Lexical analysis */
   if (oTokens == NULL) return;
   iRet = Command_readLine(oTokens); /* Syntactical analysis */
   if (iRet == FALSE) {
      Token_freeLine(oTokens);
      return;
   }
   pcCommand = Command_getCommand();
   if (pcCommand == NULL) {
      Command_reset();
      Token_freeLine(oTokens);
      return;
   }
   /* execute built-in commands if applicable */
   if (strcmp(pcCommand, "cd") == 0) builtin_callCD();
   else if (strcmp(pcCommand, "setenv") == 0) builtin_callSETENV();
   else if (strcmp(pcCommand, "unsetenv") == 0) builtin_callUNSETENV();
   else if (strcmp(pcCommand, "exit") == 0) {
      Token_freeLine(oTokens);
      builtin_callEXIT();
   }
   /* else, run the specified executable */
   else {
      acArgs = Command_getArgs();
      if (acArgs == NULL) {
         Command_reset();
         Token_freeLine(oTokens);
         return;
      }
      fflush(NULL);
      iPid = fork();
      if (iPid == -1) {
         /*perror(argv[o])*/;
         exit(EXIT_FAILURE);
      }
      
      /* Child process. */
      if (iPid == 0) {
         char* pcInputFile;
         char* pcOutputFile;
         
         signal(SIGINT, SIG_DFL);
         signal(SIGQUIT, ish_quithandler3);         

         /* I/O redirection */
         pcInputFile = Command_getInput();
         if (pcInputFile != NULL) {
            fprintf(stderr, "input file: %s\n", pcInputFile);
            ish_dup(pcInputFile, 0);
         }
         pcOutputFile = Command_getOutput();
         if (pcOutputFile != NULL) {
            fprintf(stderr, "output file: %s\n", pcOutputFile);
            ish_dup(pcOutputFile, 1);
         }
         execvp(pcCommand, acArgs);
         fprintf(stderr, "%s: %s: %s\n", pcShell, pcCommand, 
                 strerror(errno));
         exit(EXIT_FAILURE);
      }
      
      /* Parent process. */
      iPid = wait(NULL);
      if (iPid == -1) {
         fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
         exit(EXIT_FAILURE);
      }
      
      Command_freeArgs(acArgs);
   }
   
   Command_reset();
   Token_freeLine(oTokens);
   
}
/*---------------------------------------------------------------------*/

static void ish_handleconfig(char* argv) {
   char* pcHome;
   char* pcPath;
   char cPercent = '%';
   int iLength;
   int iRet;
   FILE *fp;
   char acLine[MAX_LINE];
   
   if (argv == NULL) {
      pcHome = getenv("HOME");
      pcPath = (char*) malloc(strlen(pcHome) + 8);
      
      strcpy(pcPath, pcHome);
      strcat(pcPath, "/.ishrc");
   }
   else {
      iLength = strlen(argv);
      if (iLength > MAX_LINE - 1) {
         fprintf(stderr, "%s: Argument too long\n", pcShell);
         return;
      }
      pcPath = argv;
   }

   fp = fopen((const char*)pcPath, "r");
   if (fp == NULL) {
      /*fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));*/
      if (argv == NULL) free(pcPath);
      return;
   }
   
   if (argv == NULL) free(pcPath);
   
   for (;;) {
      iRet = ish_readline(acLine, fp);
      if (iRet == FALSE) break;
      
      printf("%c %s", cPercent, acLine);
      fflush(NULL);
      ish_executeLine(acLine);
      
   }

   iRet = fclose(fp);
   if (iRet == EOF) fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
}

/*---------------------------------------------------------------------*/


int main(int argc, char* argv[]) {
   char cLine[MAX_LINE];
   char* cPercent = "%";
   int iRet;
   /* sigset_t sSigSet;
    */
   pcShell = argv[1];

/*   sigemptyset(&sSigSet);
 */
   signal(SIGINT, SIG_IGN);
   signal(SIGQUIT, ish_quithandler1);
  
   if (argc <= 2) {
      ish_handleconfig(argv[1]);
   }
   
   else fprintf(stderr, "%s: Too many arguments\n", pcShell); 
   
   for (;;) {
      signal(SIGALRM, ish_alarmhandler);
      printf("%s ", cPercent);
      fflush(NULL);
      
      iRet = ish_readline(cLine, stdin);
      if (iRet == FALSE) continue;
      
      ish_executeLine(cLine);
      
   }
   return 0;
}
