#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <pthread.h>
#include <fcntl.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PROTOCOL_RESERVER   0
#define CONFIG_BUF          256
#define CONFIG              "./config.ini"
#define PORTFLAG            "listen="
#define RECVBUFSIZE         4096

void *portprocess(void *param);

int main(int argc, char **argv)
{
    FILE        *fd;
    char        *buf;
    ssize_t     read;
    size_t      len;
    int         thread_sum;

    fd = fopen(CONFIG, "r");
    if(NULL == fd){
        printf(strerror(errno));
        exit(-1);
    }

    len = 0;
    buf = malloc(CONFIG_BUF);
    memset(buf, 0, CONFIG_BUF);
    while((read = getline(&buf, &len, fd)) != -1){
        char *strport = buf;
        char *subsequce;
        if(subsequce = strstr(strport, PORTFLAG)){
            char *port;
            strport += strlen(PORTFLAG);
            for((port = strtok(strport, ",")); port != NULL; (port = strtok(NULL, ","))){
                printf("port %s \n", port);
                int iport = atoi(port);
                pthread_t thread;
                void *status;
                pthread_create(&thread, NULL, portprocess, (void*)&iport);
                pthread_join(thread, &status);// pthread_join problem
            }
        }
    }

}

void *portprocess(void *param)
{
    int     sock;
    int     clientsock;
    struct  sockaddr_in addr;
    struct  sockaddr_in remote;
    socklen_t   len;
    char    buf[RECVBUFSIZE];

    sock = socket(AF_INET, SOCK_STREAM, PROTOCOL_RESERVER);

    if(-1 == sock){
        printf(strerror(errno));
        exit(-1);
    }

    memset(&addr, 0, sizeof(struct sockaddr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons((*(unsigned short*)param));
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if((bind(sock, (struct sockaddr*)(&addr), sizeof(struct sockaddr_in))) < 0){
        printf(strerror(errno));
        exit(-1);
    }

    if(listen(sock, 50/*backlog size*/) < 0){
        printf(strerror(errno));
        exit(-1);
    }

    clientsock = accept(sock, (struct sockaddr*)&remote, &len);
    if(-1 == clientsock){
        printf(strerror(errno));
        exit(-1);
    }

    printf("remote addr is %s\n", inet_ntoa(remote.sin_addr));
    printf("port is ");

    while(1){
        memset(buf, 0, RECVBUFSIZE);
        if(-1 == recv(clientsock, buf, RECVBUFSIZE, MSG_WAITALL)){
            printf(strerror(errno));
        }

        printf("recv data is %s \n", buf);
    }

    return NULL;
}
