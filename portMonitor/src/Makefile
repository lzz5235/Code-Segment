SOURCE = $(wildcard *.c)
OBJS = $(patsubst %.c,%.o,$(SOURCE))

CC = gcc

CFLAGS += -Wall -O2
LDFLAGS += -lpthread

all:portmonitor
	cp portmonitor ../	
portmonitor:$(OBJS)
	$(CC) -Wall $(CFLAGS) -o $@ $^ $(LDFLAGS)

.PHONY:clean
clean:
	rm -f *.o portmonitor

cpexe:
	cp portmonitor ../
