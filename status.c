#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

#define RETIC_1 26
#define RETIC_2 19
#define RETIC_3 13
#define RETIC_4 11
#define RETIC_5 9
#define RETIC_6 10

int main(int argc, char** argv) {
	if (argc != 1) {
		printf("Usage: status\n");
		return 0;
	}

	int pins[] = {RETIC_1, RETIC_2, RETIC_3, RETIC_4, RETIC_5, RETIC_6};
	wiringPiSetupGpio();
	
	for (int i = 0; i < 6; i++) {
		if (digitalRead(pins[i]) == LOW) {
			fprintf(stdout, "%d\n", i + 1);
			return 0;
		}
	}
	printf("0\n");

	return 0;
}


