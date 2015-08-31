/*------------------------------- mutex_01.c --------------------------------*
On Linux, compile with: 
cc -std=c99 -pthread mutex_01.c -o mutex_01 
 
Check your system documentation how to enable C99 and POSIX threads on 
other Un*x systems.

Copyright Loic Domaigne. 
Licensed under the Apache License, Version 2.0.
*--------------------------------------------------------------------------*/

#define _POSIX_C_SOURCE 200112L // use IEEE 1003.1-2004

#include <unistd.h>  // sleep()
#include <pthread.h> 
#include <stdio.h>   
#include <stdlib.h>  // EXIT_SUCCESS
#include <string.h>  // strerror() 
#include <errno.h>

/***************************************************************************/
/* our macro for errors checking                                           */
/***************************************************************************/
#define COND_CHECK(func, cond, retv, errv) \
if ( (cond) ) \
{ \
   fprintf(stderr, "\n[CHECK FAILED at %s:%d]\n| %s(...)=%d (%s)\n\n",\
              __FILE__,__LINE__,func,retv,strerror(errv)); \
   exit(EXIT_FAILURE); \
}
 
#define ErrnoCheck(func,cond,retv)  COND_CHECK(func, cond, retv, errno)
#define PthreadCheck(func,rc) COND_CHECK(func,(rc!=0), rc, rc)


/*****************************************************************************/
/* real work starts here                                                     */
/*****************************************************************************/
/*
 * Accordingly to the Intel Spec, the following situation
 *
 *    thread A:         thread B:
 *    mov [_x],1        mov [_y],1
 *    mov r1,[_y]       mov r2,[_x]
 *
 * can lead to r1==r2==0. 
 *
 * We use this fact to illustrate what bad surprise can happen, if we don't
 * use mutex to ensure appropriate memory visibility. 
 *
 */
volatile int Arun=0; // to mark if thread A runs
volatile int Brun=0; // dito for thread B

pthread_barrier_t barrier; // to synchronize start of thread A and B.

/*****************************************************************************/
/* threadA- wait at the barrier, set Arun to 1 and return Brun                */
/*****************************************************************************/
void*
threadA(void* arg)
{
    pthread_barrier_wait(&barrier);
    Arun=1;
    return (void*) Brun;
}

/*****************************************************************************/
/* threadB- wait at the barrier, set Brun to 1 and return Arun                */
/*****************************************************************************/
void*
threadB(void* arg)
{
    pthread_barrier_wait(&barrier);
    Brun=1;
    return (void*) Arun;
}

/*****************************************************************************/
/* main- main thread                                                         */
/*****************************************************************************/
/*
 * Note: we don't check the pthread_* function, because this program is very
 * timing sensitive. Doing so remove the effect we want to show
 */
int
main()
{
   pthread_t thrA, thrB;
   void *Aval, *Bval;
   int Astate, Bstate;

   for (int count=0; ; count++) 
   {
      // init 
      //
      Arun = Brun = 0;
      pthread_barrier_init(&barrier, NULL, 2);

      // create thread A and B
      //
      pthread_create(&thrA, NULL, threadA, NULL);
      pthread_create(&thrB, NULL, threadB, NULL);

      // fetch returned value 
      //
      pthread_join(thrA, &Aval);
      pthread_join(thrB, &Bval);

      // check result 
      //
      Astate = (int) Aval; Bstate = (int) Bval;
      if ( (Astate == 0) && (Bstate == 0) )  // should never happen 
      {
         printf("%7u> Astate=%d, Bstate=%d (Arun=%d, Brun=%d)\n",
                count, Astate, Bstate, Arun, Brun );
      } 

   } // forever

   // never reached
   //
   return EXIT_SUCCESS;
}
