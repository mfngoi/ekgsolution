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

// Declare function
int doSomething(String cmd);

void setup() {

    // Connect function to particle API
    Particle.function("doSomething", doSomething);

    // initialize the serial communication:
    Serial.begin(9600);

}

void loop() {

}

int doSomething(String cmd)
{
    int result = 1;
    Serial.println("Hello there!");

    return result; 
}