/*---------------------------------------------------------------------*/
/* ish.c                                                               */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#define _GNU_SOURCE

#include "command.h"
#include "builtin.h"
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <assert.h>
#include <sys/wait.h>
#include <fcntl.h>


enum {FALSE, TRUE};
enum {PERMISSIONS = 0600};
enum {MAX_LENGTH = 1024};

/* Name of this shell. */
char* pcShell;

/*---------------------------------------------------------------------*/

/* Read from given file into acLine. MAX_LINE is the size of array. 
   Stop reading at \n or EOF. Return TRUE if successful, FALSE if line
   is empty or if line exceeds specified length. */

static int ish_readLine(char acLine[], FILE *stream) {

   assert(acLine != NULL);
   assert(stream != NULL);

   acLine = fgets(acLine, MAX_LENGTH, stream);
   if (acLine == NULL) return FALSE;
   return TRUE;

}

/*---------------------------------------------------------------------*/

/* Input/Output redirection. Replace old stream (0 or 1 for stdin or
   stdout) with specified file. */

static int ish_dup(char* pcFilename, int iOldStream) {
   int iFd;
   int iRet;


   if (iOldStream == 0) iFd = open(pcFilename, PERMISSIONS);
   else iFd = creat(pcFilename, PERMISSIONS);

   if (iFd == -1) {
      fprintf(stderr, "%s: %s: %s\n", pcShell, pcFilename, 
              strerror(errno));
      return FALSE;
   }

   iRet = close(iOldStream);
   if (iRet == -1) {
      fprintf(stderr, "%s: %s: %s\n", pcShell, pcFilename, 
              strerror(errno));
      return FALSE;
   }

   iRet = dup(iFd);
   if (iRet == -1) {
      fprintf(stderr, "%s: %s: %s\n", pcShell, pcFilename, 
              strerror(errno));
      return FALSE;
   }

   iRet = close(iFd);
   if (iRet == -1) {
      fprintf(stderr, "%s: %s: %s\n", pcShell, pcFilename, 
              strerror(errno));
      return FALSE;
   }

   return TRUE;
}

/*---------------------------------------------------------------------*/

/* Execute the line that was just read. First analyze the line, then
   run appropriate commands. Redirect input/output if necessary. */

static void ish_executeLine(char* acLine) {

   int iRet;
   size_t iPid;
   char* pcCommand;
   char** acArgs;
   DynArray_T oTokens;
   void (*pfRet)(int);

   /* Lexically and syntactically analyze line. */
   oTokens = Token_newLine(acLine);
   if (oTokens == NULL) return;
   iRet = Command_readLine(oTokens);
   if (iRet == FALSE) {
      Command_reset();
      Token_freeLine(oTokens);
      return;
   }

   /* Stop execution if no command. */
   pcCommand = Command_getCommand();
   if (pcCommand == NULL) {
      Command_reset();
      Token_freeLine(oTokens);
      return;
   }

   /* Execute built-in commands if applicable.*/
   if (strcmp(pcCommand, "cd") == 0) builtin_callCD();
   else if (strcmp(pcCommand, "setenv") == 0) builtin_callSETENV();
   else if (strcmp(pcCommand, "unsetenv") == 0) builtin_callUNSETENV();
   else if (strcmp(pcCommand, "exit") == 0) {
      Token_freeLine(oTokens);
      builtin_callEXIT();
   }

   /* Fork off a child and run specified command. */
   else {
      acArgs = Command_getArgs();
      if (acArgs == NULL) {
         Command_reset();
         Token_freeLine(oTokens);
         return;
      }
     
      fflush(NULL);
      iPid = fork();

      if (iPid == (size_t) -1) {
         fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
         exit(EXIT_FAILURE);
      }

      /* Child process. */
      if (iPid == 0) {
         char* pcInputFile;
         char* pcOutputFile;

         pfRet = signal(SIGINT, SIG_DFL);
         if (pfRet == NULL) {
            fprintf(stderr, "%s: %s: %s\n", 
                    pcShell, pcCommand, strerror(errno));
            exit(EXIT_FAILURE);
         }

         /* Redirect input/output if applicable. */
         pcInputFile = Command_getInput();
         if (pcInputFile != NULL) {
            iRet = ish_dup(pcInputFile, 0);
            if (iRet == FALSE) {
               Command_reset();
               Token_freeLine(oTokens);
               exit(EXIT_FAILURE);
            }
         }
         pcOutputFile = Command_getOutput();
         if (pcOutputFile != NULL) {
            iRet = ish_dup(pcOutputFile, 1);
            if (iRet == FALSE) {
               Command_reset();
               Token_freeLine(oTokens);
               exit(EXIT_FAILURE);
            }
         }

         execvp(pcCommand, acArgs);
         /* Should never reach this point unless error occurs. */
         fprintf(stderr, "%s: %s: %s\n", pcShell, pcCommand, 
                 strerror(errno));
         exit(EXIT_FAILURE);
      }

      /* Parent process. */
      iPid = wait(NULL);
      if (iPid == (size_t)-1) {
         fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
         exit(EXIT_FAILURE);
      }

      Command_freeArgs(acArgs);
   }

   Command_reset();
   Token_freeLine(oTokens);

   return;
}

/*---------------------------------------------------------------------*/

/* Execute configuration file. If none provided, execute .ishrc in the
   HOME directory. If no configuration file found, proceed to 
   interactive mode. */

static void ish_handleConfig(char* argv) {
   char* pcHome;
   char* pcPath;
   char cPercent = '%';
   size_t uiLength;
   int iRet;
   FILE *fp;
   char acLine[MAX_LENGTH] = "";

   /* Get .ishrc if no argument provided. */
   if (argv == NULL) {
      pcHome = getenv("HOME");
      pcPath = (char*) malloc(strlen(pcHome) + 8);
      strcpy(pcPath, pcHome);
      strcat(pcPath, "/.ishrc");
   }
   /* Get specified file. */
   else {
      uiLength = strlen(argv);
      if (uiLength > (size_t)MAX_LENGTH - 1) {
         fprintf(stderr, "%s: Argument too long\n", pcShell);
         return;
      }
      pcPath = argv;
   }

   /* Open configuration file. Return if unopened. */
   fp = fopen((const char*)pcPath, "r");
   if (argv == NULL) free(pcPath);
   if (fp == NULL) return;

   /* Read and execute each line. Return to main if reading failed. */
   for (;;) {
      iRet = ish_readLine(acLine, fp);
      if (iRet == FALSE) break;
      printf("%c %s", cPercent, acLine);
      fflush(NULL);
      ish_executeLine(acLine);
   }

   iRet = fclose(fp);
   if (iRet == EOF) fprintf(stderr, "%s: %s\n", pcShell, 
                            strerror(errno));

}

/*---------------------------------------------------------------------*/

/* Signal handler: if program receives SIGQUIT, print quit and call
   exit(0). */

static void ish_handlequit2(int iSignal) {

   assert(iSignal == SIGQUIT);
   printf("quit\n");
   exit(0);
}

/*---------------------------------------------------------------------*/

/* Signal handler: if program receives SIGQUIT, print instruction
   message and set an alarm. Set SIGQUIT handler to ish_handlequit2. */

static void ish_handlequit1(int iSignal) {
   char cSlash = '\\';
   void (*pfRet)(int);

   assert(iSignal == SIGQUIT);

   printf("Type Ctrl-%c again within 5 seconds to quit.\n", cSlash);
   alarm(5);
   pfRet = signal(SIGQUIT, ish_handlequit2);
   if (pfRet == NULL) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }
}

/*---------------------------------------------------------------------*/

/* Signal handler: if program receives SIGALRM, print % and set the
   SIGQUIT handler to ish_handlequit1. */

static void ish_handlealarm(int iSignal) {
   char cPercent = '%';
   void (*pfRet)(int);

   assert(iSignal == SIGALRM);
   printf("%c ", cPercent);
   fflush(NULL);
   pfRet = signal(SIGQUIT, ish_handlequit1);
   if (pfRet == NULL) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }
}

/*---------------------------------------------------------------------*/

/* Set the name of the shell to the name of this executable, unblock 
   signals, handle configuration file, read and run each input line. */

int main(int argc, char* argv[]) {
   sigset_t sSigSet;
   int iRet;
   char cPercent = '%';
   char acLine[MAX_LENGTH];
   void (*pfRet)(int);

   pcShell = argv[0];

   /* Unblock SIGALRM, SIGINT, and SIGQUIT. */
   sigemptyset(&sSigSet);
   sigaddset(&sSigSet, SIGALRM);
   sigaddset(&sSigSet, SIGINT);
   sigaddset(&sSigSet, SIGQUIT);
   iRet = sigprocmask(SIG_UNBLOCK, &sSigSet, NULL);
   if (iRet != 0) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }

   /* Set handlers for SIGINT and SIGQUIT. */
   pfRet = signal(SIGINT, SIG_IGN);
   if (pfRet == SIG_ERR) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }
   pfRet = signal(SIGQUIT, ish_handlequit1);
   if (pfRet == SIG_ERR) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }

   /* Handle configuration files. */
   if (argc <= 2) ish_handleConfig(argv[1]);
   else fprintf(stderr, "%s: Too many arguments\n", pcShell);

   /* Read and run user input. */
   for (;;) {
      printf("%c ", cPercent);
      fflush(NULL);

      pfRet = signal(SIGALRM, ish_handlealarm);
      if (pfRet == SIG_ERR) {
         fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
         exit(EXIT_FAILURE);
      }
      iRet = ish_readLine(acLine, stdin);
      if (iRet == FALSE) break;
      ish_executeLine(acLine);
   }

   Command_uninit();
   return 0;
}

