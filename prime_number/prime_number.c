#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<pthread.h>  
#include<errno.h>  
#include<unistd.h> 

#define NUM 10000000
typedef enum {false = 0, true = 1} bool;

struct myarg{
	unsigned int *a;
	unsigned int begin;
	unsigned int end;
};

bool check_prime_number(unsigned int N)
{
	if(N==1 || N==0)
		return false;
	if(N==2)
		return true;
	else if(N==3)
		return true;
	else if(N==5)
		return true;
	else if(N==7)
		return true;

	if(N%2==0)
		return false;
	unsigned int end = (unsigned int)sqrt((double)N);
	for(unsigned int i=3;i<=end;i+=2)
	{
		if(N%i==0)
			return false;
	}
	return true;
}

void* thread(void *arg)
{
	struct myarg *para;
	para = (struct myarg *)arg;
	unsigned int *a = para->a;
	unsigned int begin = para->begin;
	unsigned int end = para->end;

	for(int i = begin;i<end;i++)
	{
		if(check_prime_number(a[i])==1){
			printf("%ld\n",a[i]);
			sleep(0.5);
		}
	}
	return ((void *)0);
}

int main(int argc,char **argv)
{
	unsigned int *a = (int *)malloc(sizeof(unsigned int)*NUM);
	srand(time(NULL));
	pthread_t pth;
	for(int i=0;i<NUM;i++)
	{
		a[i]=rand()%NUM;
//		printf("%ld--%d\n",a[i],check_prime_number(a[i]));
	}
	struct myarg para1,para2;
	para1.a = a;	para2.a = a;
	para1.begin = 0;	para2.begin = NUM/2;
	para1.end = NUM/2;	para2.end = NUM;
	
	int p1=0,p2=0;
	
	p1 = pthread_create(&pth,NULL,thread,(void *)&para1);
	if(p1!=0)
	{
		printf("Create pthread Error!\n");
		exit(1);
	}
	p2 = pthread_create(&pth,NULL,thread,(void *)&para2);
	if(p1!=0)
	{
		printf("Create pthread Error!\n");
		exit(1);
	}

	pthread_join(pth,NULL);	
		
	return 0;
}
