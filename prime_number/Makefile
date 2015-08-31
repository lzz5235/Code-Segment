main:prime_number.o
	gcc prime_number.o -o prime_number -lm -lpthread
prime_number.o:prime_number.c
	gcc -c prime_number.c -o prime_number.o -std=c99
clean:
	rm prime_number.o prime_number
