/*---------------------------------------------------------------------*/
/* builtin.h                                                           */
/* Name: Tiantian Zha                                                  */
/* Assignment: 7                                                       */
/*---------------------------------------------------------------------*/

#ifndef BUILTIN_INCLUDED
#define BUILTIN_INCLUDED


/* Implement cd. Check if the number of arguments in command AO is 
   correct and change directory accordingly. */

void builtin_callCD(void);


/* Implement setenv. Check if number of arguments is correct. Call
   setenv() using the array of arguments in command AO. */

void builtin_callSETENV(void);


/* Implement unsetenv. Check that there is only one command line 
   argument, and call unsetenv() using that argument. */

void builtin_callUNSETENV(void);


/* Call exit(0). Do not call if exit has command-line arguments. */

void builtin_callEXIT(void);


#endif
