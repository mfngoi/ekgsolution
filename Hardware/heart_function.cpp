/* 
 * Project myProject
 * Author: Your Name
 * Date: 
 * For comprehensive documentation and examples, please visit:
 * https://docs.particle.io/firmware/best-practices/firmware-template/
 */

#include <list>

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
int uploadEKGData(String cmd);

void setup() {
  // initialize the serial communication:
  Serial.begin(9600);

  Particle.function("uploadEKGData", uploadEKGData);

  pinMode(D0, INPUT); // Setup for leads off detection LO +
  pinMode(D1, INPUT); // Setup for leads off detection LO -

}

void loop() 
{

}


int uploadEKGData(String cmd)
{
    Serial.println("Running ekg function...");

    std::list<int> ekgList = {};
    unsigned long ekgStartTime = millis();
    std::chrono::milliseconds ekgExpirationTime = 10s;
    int ekgCounter = 0;

    Serial.println("Running heart sensor for 10 seconds... ");
    while ((millis() - ekgStartTime) < ekgExpirationTime.count())
    {
        if ((digitalRead(D0) == 1) || (digitalRead(D1) == 1))
        {
            // Serial.println('!');
            ekgList.push_back(-1);
        }
        else
        {
            // send the value of analog input 0:
            // Serial.println(analogRead(A0));
            int output = analogRead(A0);            // Particle Boron 3.3v / 4095 units
            output = (1024*output)/4095;             // Arduino Pro Mini  5v / 1024 units
            ekgList.push_back(output);
        }
        // Wait for a bit to keep serial data from saturating
        ekgCounter += 1;
        delay(1);
    }
    Serial.println("Heart sensor finished reading...");
    Serial.println(ekgCounter);

    Serial.println("Printing list...");
    std::string ekgString = "";
    for (int number : ekgList)
    {
        // Serial.println(number);
        ekgString += std::to_string(number) + ",";
    }

    Log.info(ekgString.c_str());
    Particle.publish("PublishTest", ekgString.c_str());
    Serial.println("Published ekg data...");

    return 1;
}

