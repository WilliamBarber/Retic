all: retic status

retic: controller.c
	gcc -Wall -Werror -o retic controller.c -l wiringPi

status: status.c
	gcc -Wall -Werror -o status status.c -l wiringPi

clean:
	rm -rf *.o retic status
