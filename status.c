#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include "retic.h"

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


