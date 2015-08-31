#include "csapp.h"

int main()
{
	char c;
	printf("STDIN_FILENO = %d\n",STDIN_FILENO);
	printf("STDOUT_FILENO = %d\n",STDOUT_FILENO);

	while(Read(0,&c,1)!=0)
		Write(1,&c,1);

	exit(0);
}
