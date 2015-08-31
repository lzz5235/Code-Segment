#define _GNU_SOURCE
#include<sys/types.h>
#include<sys/wait.h>
#include<stdio.h>
#include<sched.h>
#include<signal.h>
#include<unistd.h>


#define STACK_SIZE (1024*1024)
static char container_stack[STACK_SIZE];

char *const container_args[]={
	"/bin/bash",
	NULL
};


int container_main(void *arg){

	printf("Container - inside the container! pid [%d]\n",getpid());
	sethostname("container",10);
	system("mount -t proc proc /proc");
	execv(container_args[0],container_args);
	printf("Something's wrong\n");
	return 1;
}

int main(){
	printf("Parent pid [%d]\n",getpid());
	int container_pid = clone(container_main,container_stack+STACK_SIZE,//stack from top to bottom
		CLONE_NEWNS | CLONE_NEWPID | CLONE_NEWUTS |SIGCHLD,NULL);
	printf("container pid is %d\n",container_pid);
	waitpid(container_pid,NULL,0);
	printf("Parent - container stopped!\n");
	return 0;
}
