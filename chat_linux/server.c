/*
 *title:server.c
 *content:server part
 *start time: Mar.25.2011
 *end time:  Apr.8 2011
 */

#include "i.h"

int user_list_fd;

/* start:initialization */
int init()
{
	i_init();

	user_list_fd = i_open("./user_list", O_RDWR|O_CREAT);

	struct user usr;
	/* init the user list file's fist user to 0*/
	memset((struct user*)&usr, '\0', sizeof(struct user));
	i_lseek(user_list_fd, 0, SEEK_SET);
	i_write(user_list_fd, (char*)&usr, USR_LEN);

	/* bind the struct sockaddr_in server to the sockfd */
	i_bind(sockfd, (struct sockaddr*)&server, ADDR_LEN);	

	struct chat_history apple;	

	bzero(&apple, HSTR_LEN);
	i_lseek(mainfd, 0, SEEK_SET);
	i_write(mainfd, &apple, HSTR_LEN);
	i_lseek(mainfd, -HSTR_LEN, SEEK_END);
	i_read(mainfd, &apple, HSTR_LEN);
	count = apple.count;

	return(0);
}
/* end:initialization */

/* start:message control */
int send_msg(struct msg *msg_recv, struct sockaddr *addr)
{
	int i;
	struct user usr;

	/* a common message come */	
	printf("a ordinar message come !\n");
	
	i = msg_recv->id_to;
	i_lseek(user_list_fd, i*USR_LEN, SEEK_SET);
	i_read(user_list_fd, &usr, USR_LEN);
	strncpy(msg_recv->append, usr.name, 10);

	i_sendto(sockfd, msg_recv, MSG_LEN, 0,
		&(usr.user_addr), ADDR_LEN);
	
	printf("id%d send a message to id%d sucess!\n", msg_recv->id_from, msg_recv->id_to);

	return(0);
}
int check_login(struct msg *msg_recv, struct sockaddr *addr)
{
	int i = msg_recv->id_from;;
	struct user usr;

	/* a login requet */
	printf("a login request come!\n");
	
	/* get the id's information */
	i_lseek(user_list_fd, i*USR_LEN, SEEK_SET);
	i_read(user_list_fd, &usr, USR_LEN);

	int n;
	n = strcmp(usr.password, msg_recv->content);
	/* 如果验证成功，则发送成功信息 */
	if (n == 0)
	{
		/* save user new address */
		i_lseek(user_list_fd, -USR_LEN, SEEK_CUR);
		usr.user_addr = *addr;
		i_write(user_list_fd, &usr, USR_LEN);
		/* tell user pass */
		i_sendto(sockfd, (struct msg*)msg_recv, sizeof(struct msg), 0,
			&(usr.user_addr), ADDR_LEN);
		
	}
	else
	{
		/* 出错的话的respond */
		if (0 != n)
		{
			printf("id %d login error.\n", i);
			bzero(msg_recv->content, CNTNT_LEN);			
			msg_recv->flag = -1;
			i_sendto(sockfd, (struct msg*)msg_recv, sizeof(struct msg), 0,
				&(usr.user_addr), ADDR_LEN);
		
		}
		return(1);
	}
	printf("Id %d login sucess!\n", i);	
	
	return(0);
}
int reg_user(struct msg *msg_recv, struct sockaddr *addr)
{
	struct user usr;
	
	printf("a regit requet come:\n");

	/* find the last user and hava the please to add a new user */
	int n;
	i_lseek(user_list_fd, -USR_LEN, SEEK_END);
	i_read(user_list_fd, &usr, USR_LEN);
	/* 把新用户的信息赋值到usr然后填入到user list file中 */
	const char *name;
	const char *password;

	name = &(msg_recv->content[0]);
	password = &(msg_recv->content[10]);
	strcpy((usr.name), name);
	strcpy(usr.password, password);
	memcpy(&(usr.user_addr),addr, ADDR_LEN);

	usr.id = (usr.id + 1);
	i_lseek(user_list_fd, 0, SEEK_END);
	i_write(user_list_fd, &usr, USR_LEN);

	msg_recv->id_from = usr.id;
	/* regist to the user list then tell the user reg success */
	i_sendto(sockfd, (struct msg*)msg_recv, sizeof(struct msg), 0,
		addr, ADDR_LEN); 

	printf("Id %d regist sucess!\n", usr.id);

	return(0);
	
}
int msg_cntl()
{
	struct msg msg_recv;
	struct sockaddr addr_recv;

	printf("begin listen input...\n");
	int size = ADDR_LEN;

	for (;;)
	{
		bzero(&msg_recv, MSG_LEN);
		i_recvfrom(sockfd, &msg_recv, sizeof(struct msg), 0,
			&addr_recv, &size);
		printf("message received...\n");

		i_saveto_chat(&msg_recv);

		switch (msg_recv.flag)
		{
			case 1 :
				send_msg(&msg_recv,(struct sockaddr*)&addr_recv);/* send ordinary chat */
				break;
			case 2 :
				check_login(&msg_recv, (struct sockaddr*)&addr_recv);
				break;			
			case 3 :
				reg_user(&msg_recv, (struct sockaddr*)&addr_recv);
				break;
			default :
				break;
		}
	}
	return(0);
}
/* end:message control*/
/* start:exit_sys()*/
int exit_sys()
{
	close(sockfd);
	close(mainfd);
	close(user_list_fd);
	printf("exit system");
	kill(0, SIGABRT);

	exit(0);
}
/* end:exit_sys()*/

/* start:chat_history*/
int get_page_size()
{
	struct chat_history page_size_reader;
	
	i_lseek(mainfd, -HSTR_LEN, SEEK_END);
	i_read(mainfd, &page_size_reader, HSTR_LEN);

	return(page_size_reader.count);
}

int read_chat_history()
{
	printf("****char*history***");
	printf("(n-nextpage; p-prepage; q-quit)\n");

	int page_num;/* */
	int remains;
	int berry = get_page_size();


	page_num = berry / 8;
	remains = berry % 8;

	if (remains != 0)
		page_num ++;
	else
		page_num = page_num;
		
	printf("there are %d page total %d items", 
		page_num, berry);

	int i = -1;

	while (1)
	{	
		char flag;	

		if ((berry + i*8) >= 0)
		{
			printf("(%d~%d)\n", (berry + i*8), (berry + (i+1)*8));

			i_print_history(PRT_LEN, i);

			printf("@@@\n");
			while ('\n' == (flag = getchar()))
			{
			}

			switch (flag)
			{
				case 'p' :
					i--;
					break;
				case 'n' :
					i++;
					break;
				case 'q' :
					return(0);
				default  :
					break;
			}	
			if (i >= 0)
			{
				printf("have at the end!\n");
				printf("return to menu!\n");
			}		
		}
		else 
		{
			printf("(1~%d)\n", remains);			
		
			i_print_history(remains, 0);
			
			printf("#########over##############\n");

			return(0);
		}	
	}
		
	return(0);
}
/* end:chat_history*/
/* start:menu*/
int menu()
{
	sleep(1);

	printf("----------help----menu---------\n");
	printf("\t r--report to user\n");
	printf("\t c--chat history\n");
	printf("\t h--help menu\n");
	printf("\t e--exit the system\n");
	printf("----------help_menu---------\n");

	int command = 0;

	printf("input command>");
	command = getchar();
	switch(command)
	{

		case 'c':
			read_chat_history();
			break;
		case 'e':
			exit_sys();
			break;
		case 'r':
			//report();
			//break;
		default :
			menu();
			break;
	}
	getchar();
	
	return(0);
}
/* end:menu*/
int main()
{
	init();
	pid_t pid;
	switch (pid = fork())
	{
		case -1 :
			perror("fork error\n");
			exit(1);
			break;
		case 0 :
			msg_cntl();
			break;
		default :
			menu();
			break;
	}

	return(0);
}
