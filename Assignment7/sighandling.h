/*---------------------------------------------------------------------*/
/* sighandling.h                                                       */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#ifndef SIGHANDLING_INCLUDED
#define SIGHANDLING_INCLUDED

/* Upon receiving SIGQUIT signal, print and exit(0). */

void sighandling_quit1(int iSignal);


/* Upon receiving SIGQUIT signal, change SIGQUIT handler to
   sighandling_quit2. Set SIGALRM handler to sighandling_alarm. 
   Print user message. */

void sighandling_quit2(int iSignal);


/* Upon receiving SIGALRM signal, print % and set the SIGQUIT handler
   to sighandling_quit1. */

void sighandling_alarm(int iSignal);


#endif
