#include "csapp.h"

int main(int argc,char **argv)
{
	int n;
	rio_t rio;
	char BUF[MAXLINE];
//	int fd = Open("log.txt",O_RDONLY,0);

	Rio_readinitb(&rio,STDIN_FILENO);
	while((n = Rio_readlineb(&rio,BUF,MAXLINE))!=0)
	{
		Rio_writen(STDOUT_FILENO,BUF,n);
	}
}
