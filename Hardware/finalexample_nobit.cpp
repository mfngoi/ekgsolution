/*
 * Project myProject
 * Author: Your Name
 * Date:
 * For comprehensive documentation and examples, please visit:
 * https://docs.particle.io/firmware/best-practices/firmware-template/
 */

// Include Particle Device OS APIs
#include <stdlib.h>
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
    ekgSignals[ekgCounter] = r;

    delay(20); // Wait for a bit to keep serial data from saturating
    ekgCounter += 1;
  }
  Serial.printf("Finished collecting %d signals\n", size);

  string data = "";
  for (int i=0; i<size; i++) {
    string num = to_string(ekgSignals[i]); // Convert to string
    data = data + num + ","
  }

  // Create JSON
  string uid = cmd;
  string signals = data;
  string data = String::format("{ \"data\": \"%s\", \"uid\": \"%s\" }", signals.c_str(), uid.c_str());
  // Submit data
  Particle.publish("PublishTest", data);  // Change to Publish or PublishTest

  return 1;
  }

  // int len = encodedLen/2;
  // char *str1 = (char*)malloc(len +1);
  // memcpy(str1, encoded, len);
  // str1[len] = '\0';

  // char *str2 = (char*)malloc(len +1);
  // memcpy(str2, encoded + len, len);
  // str2[len] = '\0';

  // Particle.publish("Publish", str1);
  // Particle.publish("Publish", str2);

  // free(str1);
  // free(str2);

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