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

char* pcShell;

static int loop_readLine(char acLine[], FILE *stream) {

   assert(acLine != NULL);
   assert(stream != NULL);

   acLine = fgets(acLine, MAX_LENGTH, stream);
   if (acLine == NULL) return FALSE;
   return TRUE;

}

static void loop_dup(char* cFilename, int iOldStream) {
   int iFd;
   int iRet;

   if (iOldStream == 0) iFd = open(cFilename, PERMISSIONS);
   else iFd = creat(cFilename, PERMISSIONS);

   if (iFd == -1) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }
   iRet = close(iOldStream);
   iRet = dup(iFd);
   iRet = close(iFd);


}


static void my_handler2(int iSignal) {
   printf("quit\n");
   exit(0);
}

static void my_handler(int iSignal) {
   char cSlash = '\\';
   printf("Press Ctrl-%c again in 5 seconds\n", cSlash);
   alarm(5);
   signal(SIGQUIT, my_handler2);

   return;
}

static void my_handler3(int iSignal) {
   char cPercent = '%';
   alarm(0);
   printf("%c ", cPercent);
   fflush(NULL);
   signal(SIGQUIT, my_handler);

}

static void loop_executeLine(char* acLine) {

   int iRet;
   int iPid;
   char* pcCommand;
   char** acArgs;
   DynArray_T oTokens;

   oTokens = Token_newLine(acLine);
   if (oTokens == NULL) return;
   iRet = Command_readLine(oTokens);
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

   if (strcmp(pcCommand, "cd") == 0) builtin_callCD();
   else if (strcmp(pcCommand, "setenv") == 0) builtin_callSETENV();
   else if (strcmp(pcCommand, "unsetenv") == 0) builtin_callUNSETENV();
   else if (strcmp(pcCommand, "exit") == 0) {
      Token_freeLine(oTokens);
      builtin_callEXIT();
   }

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
         fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
         exit(EXIT_FAILURE);
      }

      /* Child process. */
      if (iPid == 0) {
         char* pcInputFile;
         char* pcOutputFile;

         signal(SIGINT, SIG_DFL);

         pcInputFile = Command_getInput();
         if (pcInputFile != NULL) {
            loop_dup(pcInputFile, 0);
         }
         pcOutputFile = Command_getOutput();
         if (pcOutputFile != NULL) {
            loop_dup(pcOutputFile, 1);
         }

         execvp(pcCommand, acArgs);
         fprintf(stderr, "%s: %s: %s\n", pcShell, pcCommand, strerror(errno));
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

   return;
}


static void loop_handleConfig(char* argv) {
   char* pcHome;
   char* pcPath;
   char cPercent = '%';
   int iLength;
   int iRet;
   FILE *fp;
   char acLine[MAX_LENGTH];

   if (argv == NULL) {
      pcHome = getenv("HOME");
      pcPath = (char*) malloc(strlen(pcHome) + 8);
      strcpy(pcPath, pcHome);
      strcat(pcPath, "/.ishrc");
   }
   else {
      iLength = strlen(argv);
      if (iLength > MAX_LENGTH - 1) {
         fprintf(stderr, "%s: Argument too long\n", pcShell);
         return;
      }
      pcPath = argv;
   }

   fp = fopen((const char*)pcPath, "r");
   if (argv == NULL) free(pcPath);
   if (fp == NULL) return;

   for (;;) {
      iRet = loop_readLine(acLine, fp);
      if (iRet == FALSE) break;
      printf("%c %s", cPercent, acLine);
      fflush(NULL);
      loop_executeLine(acLine);
   }
   iRet = fclose(fp);
   if (iRet == EOF) fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));

}



int main(int argc, char* argv[]) {
   sigset_t sSigSet;
   int iRet;
   char cPercent = '%';
   char acLine[MAX_LENGTH];

   pcShell = argv[0];

   sigemptyset(&sSigSet);
   sigaddset(&sSigSet, SIGALRM);
   sigaddset(&sSigSet, SIGINT);
   sigaddset(&sSigSet, SIGQUIT);
   iRet = sigprocmask(SIG_UNBLOCK, &sSigSet, NULL);
   if (iRet != 0) {
      fprintf(stderr, "%s: %s\n", pcShell, strerror(errno));
      exit(EXIT_FAILURE);
   }

   signal(SIGINT, SIG_IGN);
   signal(SIGQUIT, my_handler);

   if (argc <= 2) {
      loop_handleConfig(argv[1]);
   }
   else fprintf(stderr, "%s: Too many arguments\n", pcShell);

   for (;;) {
      signal(SIGALRM, my_handler3);
      printf("%c ", cPercent);
      fflush(NULL);

      iRet = loop_readLine(acLine, stdin);
      if (iRet == FALSE) break;
      loop_executeLine(acLine);
   }
   return 0;
}

