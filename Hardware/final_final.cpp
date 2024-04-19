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
#include "Base64RK.h"

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
  pinMode(D0, INPUT); // Setup for leads off detection LO +
  pinMode(D1, INPUT); // Setup for leads off detection LO -
}

void loop()
{
}

int uploadEKGData(String cmd)
{

  // Split argument values
  char user_id[50], report_id[50];
  sscanf(cmd, "%[^,],%[^,]", &user_id, &report_id);

  const int size = 400;
  size_t b_size = size * 1.5;

  // Store ecg signals raw then in 4 bits form
  unsigned short ekgSignals[size];
  uint8_t binarySignals[b_size]; // Used to store binary data

  Serial.printf("Collecting %d signals\n", size);
  int ekgCounter = 0;
  while (ekgCounter < size)
  {

    if ((digitalRead(D0) == 1) || (digitalRead(D1) == 1))
    {
      ekgSignals[ekgCounter] = 0;
      Serial.println(0);
    }
    else
    {
      unsigned short output = analogRead(A0);
      ekgSignals[ekgCounter] = output;
      Serial.println(output);
    }

    delay(25); // Wait for a bit to keep serial data from saturating
    ekgCounter += 1;
  }
  Serial.printf("Finished collecting %d signals\n", size);

  // Convert short array into uint8_t array
  // Track progress of byte array
  size_t index = 0;
  bool half_byte = false;

  // Iterate through short array
  for (int i = 0; i < size; i++)
  {
    unsigned short number = ekgSignals[i];
    // Extract (4 bits) x3 from short array
    for (int j = 0; j < 3; j++)
    {
      unsigned short n = number;
      unsigned short mask = ~(~0 << 4);
      uint8_t value = (n >> (2 - j) * 4) & mask; // Extract value of 4 bits from left to right

      // Insert value into the byte_array
      if (!half_byte)
      {
        binarySignals[index] = value << 4; // Store left half of 4 bits
        half_byte = !half_byte;
      }
      else
      {
        binarySignals[index] = binarySignals[index] | value; // Store right half of 4 bits
        half_byte = !half_byte;
        index++;
      }
    }
  }
  Serial.println("=======================================");
  Serial.println(index);

  // Encode binarySignals to base64
  size_t encodedLen = Base64::getEncodedSize(b_size, true);
  char *encoded = new char[encodedLen]; // Destination variable
  bool success = Base64::encode(binarySignals, b_size, encoded, encodedLen, true);
  if (success)
  {
    Serial.println("==================");
    Serial.println(encodedLen);
    Serial.println(encoded);

    String signals = encoded;

    String data = String::format("{ \"data\": \"%s\", \"uid\": \"%s\", \"report_id\": \"%s\" }", signals.c_str(), user_id, report_id);

    Particle.publish("PublishTest", data);
  }
  else
  {
    Serial.println("Something went wrong");
    return 0;
  }

  return 1;
}

int doSomething(String cmd)
{
  int result = 1;
  Serial.println("doSomething triggered (version 4)...");
  Serial.println(cmd);

  char user_id[50], report_id[50];
  sscanf(cmd, "%[^,],%[^,]", &user_id, &report_id);
  Serial.println(user_id);
  Serial.println("==============");
  Serial.println(report_id);
  Serial.println("==============");

  String data = String::format("{ \"data\": \"%s\", \"uid\": \"%s\" }", user_id, report_id);

  Particle.publish("PublishTest", data);

  if (cmd == "red")
    Serial.println("Welcome to the matrix");
  else if (cmd == "blue")
    Serial.println("Turn away from the truths");

  return result;
}