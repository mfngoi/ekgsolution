/*
 * Project myProject
 * Author: Your Name
 * Date:
 * For comprehensive documentation and examples, please visit:
 * https://docs.particle.io/firmware/best-practices/firmware-template/
 */

// Include Particle Device OS APIs
#include <list>
#include <stdlib.h>
#include "Particle.h"
#include "Base64RK.h"

// Let Device OS manage the connection to the Particle Cloud
SYSTEM_MODE(AUTOMATIC);

// Run the application and system concurrently in separate threads
SYSTEM_THREAD(ENABLED);

// Show system, cloud connectivity, and application logs over USB
// View logs with CLI using 'particle serial monitor --follow'
SerialLogHandler logHandler(LOG_LEVEL_INFO);

// Forward declarations (functions used before they're implemented)
int doSomething(String cmd);
int uploadEKGData(String cmd);

void setup()
{

  // Particle functions
  Particle.function("doSomething", doSomething);
  Particle.function("uploadEKGData", uploadEKGData);

  // initialize the serial communication:
  Serial.begin(9600);
}

void loop()
{
}

int uploadEKGData(String cmd)
{
  const int size = 1000;
  short ekgCounter = 0;
  short ekgSignals[size];

  Serial.println("Collecting 1000 signals");
  while (ekgCounter < size)
  {

    short r = rand() % 4096;
    // Serial.println(r);
    ekgSignals[ekgCounter] = r;

    delay(1); // Wait for a bit to keep serial data from saturating
    ekgCounter += 1;
  }
  Serial.println("Finished collecting 1000 signals");


  // Publish one half of the array
  // 1. encode half of the array to base64
  size_t encodedLen = Base64::getEncodedSize(3, true);
  char *encoded = new char[encodedLen];
  uint8_t data[] = {50, 224, 208};
  bool success = Base64::encode(data, 3, encoded, encodedLen, true);

  if(success) {
    Serial.println(encoded);
    Serial.println(data[1], BIN);
    Serial.println(3734, BIN);
  } else {
    Serial.println("Something went wrong");
  }
  
  // for (int i = 0; i < ekgCounter; i++)
  // {
  //   Serial.println(ekgSignals[i]);
  // }

  // Serial.println("Amount of Readings: ");
  // Serial.println(ekgCounter);
  return 1;
}

int doSomething(String cmd)
{
  int result = 1;
  Serial.println("doSomething triggered...");
  if (cmd == "red")
    Serial.println("Welcome to the matrix");
  else if (cmd == "blue")
    Serial.println("Turn away from the truths");

  return result;
}