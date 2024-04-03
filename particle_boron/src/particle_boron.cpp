/*
 * Project myProject
 * Author: Your Name
 * Date:
 * For comprehensive documentation and examples, please visit:
 * https://docs.particle.io/firmware/best-practices/firmware-template/
 */

// Include Particle Device OS APIs
#include <stdlib.h>
#include <string>
#include "Particle.h"

using namespace std;

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
  const int size = 100;

  // Store ecg signals raw then in 4 bits form
  unsigned short ekgSignals[size];

  Serial.printf("Collecting %d signals\n", size);
  int ekgCounter = 0;
  while (ekgCounter < size)
  {
    unsigned short r = rand() % 4096; // Reading Sample
    Serial.println(r);
    Serial.println(r, BIN);
    Serial.println("======================");

    ekgSignals[ekgCounter] = r;

    delay(50); // Wait for a bit to keep serial data from saturating
    ekgCounter += 1;
  }
  Serial.printf("Finished collecting %d signals\n", size);

  string signals_data = "";
  for (int i=0; i<size; i++) {
    string num = to_string(ekgSignals[i]); // Convert to string
    signals_data += num + ",";
  }

  // Create JSON
  String uid = cmd;
  // String signals = signals_data;
  String data = String::format("{ \"data\": \"%s\", \"uid\": \"%s\" }", signals_data.c_str(), uid.c_str());
  // Submit data
  Particle.publish("PublishTest", data);  // Change to Publish or PublishTest

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