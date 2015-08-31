/*
 *i.h is a used for creating a library
 *for server client
 *Mar 18 2010	
 *
 */
#ifndef _I_H

#define _I_H

#include <math.h>
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <inttypes.h>
#include <time.h>
#include <sys/ioctl.h> 
#include <net/if.h>
#include <signal.h>
#include <ncurses.h>
#include <math.h>

#define SEVR_IP     "127.0.0.1"
#define SEVR_PORT   8081
#define CNTNT_LEN   150
#define MSG_LEN     sizeof(struct msg)
#define ADDR_LEN    sizeof(struct sockaddr)
#define USR_LEN     sizeof(struct user)
#define PRT_LEN     8
#define HSTR_LEN    sizeof(struct chat_history)

/* declare Global variables */
int mainfd;/* used as chat histroy file handle*/
int sockfd;/* used as socket local handle */
int count;
struct sockaddr_in server;

/* msg is used for communicating message */
struct msg
{
	int flag; /* flag meaning:1,ordinary; 2,log msg; 3,reg msg, other,file*/
	int id_from;
	int id_to;
	char content[CNTNT_LEN];
	char append[10]; 
};

/* user is used information list */
struct user
{
	int id;
	char name[10];
	char password[10];
	char *p_chatlog;
	struct sockaddr user_addr;	
};
/* chat_history used for reading chat history */
struct chat_history
{
	char content[CNTNT_LEN];
	char time[25];
	int to;
	int from;
	int count;
};

/* i_functions below is funtions needed by both client and sever */
extern int i_saveto_chat(struct msg *pmsg);

int i_clean_stdin ()
{
	while ('\n' == getchar())
	{
		continue;
	}

	return(0);
}

int i_print(char *pmsg, int size)
{
	int i = 1;

	for (i; i<= size; i++)
	{
		if (*pmsg != '\n')
		{
			printf("%c", *pmsg);
			pmsg ++;
		}
		else 
		{
			return(0);
		}
	}

	return(0);
}
int i_input(char *p_input)
{
	char c = '\0';
	int i;	

	for (i = 0; i < CNTNT_LEN; i++)
	{
		p_input[i] = getchar();
		if (p_input[i] =='\n')
		{
			return(0);		
		}		
	}

	printf("you have input long enough!\n");
	return(0);
}
int i_socket(int domain, int type, int protocol)
{
	int fd;	

	if ((fd = socket(domain, type, protocol)) == -1)
	{
		perror("creat socket error:");
		exit(1);
	}
	
	return(fd);	
}

int i_bind(int fd, const struct sockaddr *addr, int namelen)
{
	if (-1 == bind(fd, addr, namelen))
	{
		perror("i_bind error:");
		exit(1);
	}
	
	return (0);
}

int i_recvfrom(int fd, void *buf, size_t len, int flags, 
		struct sockaddr *addr, int *size)
{	
	if (-1 == recvfrom(fd, buf, len, flags, addr, size))
	{
		perror("i_recvfrom error:");
		exit(1);	
	}
	
	return(0);
}

int i_sendto(int fd, void *buf, size_t len, int flags,
		struct sockaddr *addr, int size)
{
	if (-1 == sendto(fd, buf, len, flags, addr, size))
	{
		perror("i_sendto error");
		exit(1);	
	}
	
	return (0);
}

int i_open(const char *pathname, int flags)
{
	int fd;
	if ((fd = open(pathname, flags)) == -1)
	{
		perror("open_failed");
		exit(1);
	}
	
	return (fd);
}
int i_read(int fd, void *msg, int len)
{
	if(-1 == read(fd, msg, len))
	{
		perror("i_read error");
		exit(1);
	}
	return(0);
}
int i_write(int fd, void *msg, int len)
{
	if (-1 == write(fd, msg, len))
	{
		perror("i_write error");
		exit(0);
	}
	return(0);
}

/* init a socket,file and server addr */
int i_init()
{
	mainfd = i_open("./chat_log", O_RDWR|O_CREAT);
	sockfd = i_socket(AF_INET, SOCK_DGRAM, 0);

	/* initialize server address */
	bzero(&server, sizeof(server));
	server.sin_family = AF_INET;
	inet_pton(AF_INET, "127.0.0.1", &server.sin_addr);
	server.sin_port = htons(SEVR_PORT);

	perror("init");
	
	return (0);
}

char *i_get_time()
{
	time_t time_now;
	time(&time_now);

	return(ctime(&time_now));
}
int i_lseek(int fd, off_t size, int position)
{
	if (-1 == lseek(fd, size, position))
	{
		perror("seek error");
		exit(1);
	}
	return(0);
}
int i_saveto_chat(struct msg *pmsg)
{	
	struct chat_history hstr;


	bzero(&hstr, HSTR_LEN);
	count = count + 1;
	hstr.count =count;
	hstr.from = pmsg->id_from;
	hstr.to = pmsg->id_to;
	strncpy(hstr.content, pmsg->content, CNTNT_LEN);
	strncpy(hstr.time, i_get_time(), 25);

	i_lseek(mainfd, 0, SEEK_END);

	i_write(mainfd, &hstr, HSTR_LEN);

	return(0);
}

int i_print_history(int len, int i)
{
	struct chat_history chat_reader;
	int j;
	int position;
	
	bzero(&chat_reader, HSTR_LEN);
	if (i != 0)
	{
		position = len*i*HSTR_LEN;
		i_lseek(mainfd, position, SEEK_END);
	}
	else
	{
		position = len*i*HSTR_LEN;

		i_lseek(mainfd, HSTR_LEN, SEEK_SET);
	}
		
	for (j = 1; j <= len; j++)
	{
		
		i_read(mainfd, &chat_reader, HSTR_LEN);
		printf("\n#item%d:id%dto id%d \n", j,
			chat_reader.from, chat_reader.to);
		i_print(chat_reader.content, CNTNT_LEN);
		printf("\n  Time:%s\n", chat_reader.time);
	}

	return(0);
}

#endif
