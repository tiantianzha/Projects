/*---------------------------------------------------------------------*/
/* sighandling.c                                                       */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#include "sighandling.h"
#include "command.h"
#include <signal.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

enum {ALARM_TIME = 5};

/*---------------------------------------------------------------------*/

/* Upon receiving SIGQUIT signal, print and exit(0). */

void sighandling_quit2(int iSignal) {

   assert(iSignal == SIGQUIT);
   printf("quit\n");
   exit(0);
}

/*---------------------------------------------------------------------*/

/* Upon receiving SIGQUIT signal, change SIGQUIT handler to
   sighandling_quit2. Set SIGALRM handler to sighandling_alarm. 
   Print user message. */

void sighandling_quit1(int iSignal) {
   char cSlash = '\\';
   void (*pfRet)(int); 

   assert(iSignal == SIGQUIT);

   printf("Type Ctrl-%c again within 5 seconds to quit.\n", cSlash);
   alarm(ALARM_TIME);
   /*pfRet = signal(SIGALRM, sighandling_alarm);*/
   pfRet = signal(SIGQUIT, sighandling_quit2);
   return;

}

/*---------------------------------------------------------------------*/

/* Upon receiving SIGALRM signal, print % and set the SIGQUIT handler
   to sighandling_quit1. */

void sighandling_alarm(int iSignal) {
   char cPercent = '%';

   assert(iSignal == SIGALRM);

   printf("%c ", cPercent);
   fflush(NULL);
   signal(SIGQUIT, sighandling_quit1);

}
