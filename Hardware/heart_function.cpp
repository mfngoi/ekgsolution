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

// Time controllers
unsigned long ekgStartTime = 0;
std::chrono::milliseconds ekgExpirationTime = 10s;

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

void showlist(std::list<int> g)
{
    std::list<int>::iterator it;
    for(it = g.begin(); it != g.end(); ++it) {
        Serial.println(*it);
    }
}

int uploadEKGData(String cmd)
{
  Serial.println("Running ekg function...");

  std::list<int> ekgList = {};
  ekgStartTime = millis();

  while((millis() - ekgStartTime) < ekgExpirationTime.count()) {
      if((digitalRead(D0) == 1)||(digitalRead(D1) == 1)){
          Serial.println('!');
          ekgList.push_back(-1);
      }
      else{
          // send the value of analog input 0:
          Serial.println(analogRead(A0));
          ekgList.push_back(analogRead(A0));
      }
      //Wait for a bit to keep serial data from saturating
      delay(20);
  }

  Serial.println("Printing list...");
  for(int number: ekgList) {
    Serial.println(number);
  }

  // Particle.publish("PublishTest", String(ekgList));

  return 1;
}
