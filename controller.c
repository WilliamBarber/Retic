#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>

#define RETIC_1 26
#define RETIC_2 19
#define RETIC_3 13
#define RETIC_4 11
#define RETIC_5 9
#define RETIC_6 10

void initializePins(int* pins);
void zeroAllPins(int* pins);
void setPin(int pinNumber, int* pins);

int main(int argc, char** argv) {
	if (argc != 2) {
		fprintf(stderr, "Usage: retic station_number (1-6, or 0 for all off)\n");
		return 0;
	}
	int stationNumber = atoi(argv[1]);
	if (stationNumber < 0 || stationNumber > 6) {
		fprintf(stderr, "Invalid station number. Valid: 1-6 or 0 for all off.\n");
		return 0;
	}

	int pins[] = {RETIC_1, RETIC_2, RETIC_3, RETIC_4, RETIC_5, RETIC_6};

	wiringPiSetupGpio();
	initializePins(pins);

	if (stationNumber == 0) {
		zeroAllPins(pins);
	}
	else {
		setPin(pins[stationNumber - 1], pins);
	}

	return 0;
}

void initializePins(int* pins) {
	for (int i = 0; i < 6; i++) {
		pinMode(pins[i], OUTPUT);
	}	
}

void zeroAllPins(int* pins) {
	for (int i = 0; i < 6; i++) {
		digitalWrite(pins[i], HIGH);
	}
}

void setPin(int pinNumber, int* pins) {
	zeroAllPins(pins);
	digitalWrite(pinNumber, LOW);
}
