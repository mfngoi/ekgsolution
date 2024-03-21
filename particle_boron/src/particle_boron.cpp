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
  const int size = 500;
  size_t b_size = size*(3/2);

  // Store ecg signals raw then in 4 bits form
  unsigned short ekgSignals[size];
  uint8_t binarySignals[b_size];  // Used to store binary data 


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


  // Publish one half of the array
  // 1. encode half of the array to base64

  // Convert short array into uint8_t array
  // Track progress of byte array
  size_t index = 0;
  bool half_byte = false;

  // Iterate through short array
  for (int i=0; i<size; i++) {
    unsigned short number =  ekgSignals[i];
    // Extract (4 bits) x3 from short array
    for (int j=0; j<3; j++) {
      unsigned short n = number;
      unsigned short mask = ~(~0 << 4);
      uint8_t value = (n >> (2-j)*4) & mask; // Extract value of 4 bits from left to right

      // Insert value into the byte_array
      if (!half_byte) {
        binarySignals[index] = value << 4; // Store left half of 4 bits
        half_byte = !half_byte;
      } else {
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
  if (success) {
    Serial.println("==================");
    Serial.println(encodedLen);
    Serial.println(encoded);
    Particle.publish("Publish", encoded);
  } else {
    Serial.println("Something went wrong");
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