/* 
 * Project myProject
 * Author: Your Name
 * Date: 
 * For comprehensive documentation and examples, please visit:
 * https://docs.particle.io/firmware/best-practices/firmware-template/
 */

// Include Particle Device OS APIs
#include "Particle.h"

// Let Device OS manage the connection to the Particle Cloud
SYSTEM_MODE(AUTOMATIC);

// Run the application and system concurrently in separate threads
SYSTEM_THREAD(ENABLED);

// Show system, cloud connectivity, and application logs over USB
// View logs with CLI using 'particle serial monitor --follow'
SerialLogHandler logHandler(LOG_LEVEL_INFO); 

// Forward declarations (functions used before they're implemented)
int uploadEKGData(String cmd);

void setup() {

    // Particle functions
    Particle.function("uploadEKGData", uploadEKGData);

    // initialize the serial communication:
    Serial.begin(9600);
    pinMode(D0, INPUT); // Setup for leads off detection LO +
    pinMode(D1, INPUT); // Setup for leads off detection LO -

}

void loop() {

}

int uploadEKGData(String cmd) {

    int ekgCounter = 0;

    if (cmd == "3.3v") {
        Serial.println("Printing 3.3v list of readings: ");
    } else {
        Serial.println("Printing 5v list of readings: ");
    }

    while(ekgCounter < 10000) {
        if((digitalRead(D0) == 1)||(digitalRead(D1) == 1)){
            Serial.println('-1');
        }
        else{
            // send the value of analog input 0:
            int output = analogRead(A0);            // Particle Boron 3.3v / 4095 units

            if (cmd == "3.3v") {
                output = (1024*output)/4095;             // Arduino Pro Mini  5v / 1024 units
                Serial.println(output);
            } else {
                Serial.println(output);
            }
        }
        //Wait for a bit to keep serial data from saturating
        delay(1);
        ekgCounter += 1;
    }
    Serial.println("Amount of Readings: ");
    Serial.println(ekgCounter);
    return 1;
}