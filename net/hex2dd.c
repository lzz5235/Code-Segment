#include "../io/csapp.h"

int main(int argc,char **argv)
{
	struct in_addr inaddr;
	unsigned int addr;

	if(argc!=2)
	{
		fprintf(stderr, "usage: %s <hex number>\n",  argv[0]);
		exit(0);
	}
	sscanf(argv[1],"%x",&addr);

	inaddr.s_addr = htonl(addr);
	printf("%s\n",inet_ntoa(inaddr));
	exit(0);
}
