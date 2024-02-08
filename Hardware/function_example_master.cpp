#include "Particle.h"
#include <list>
#include <string>

// The following line is optional, but it allows your code to run
// even when not cloud connected
SYSTEM_THREAD(ENABLED);

// This allows for USB serial debug logs
SerialLogHandler logHandler;

unsigned long colorSetTime = 0;
std::chrono::milliseconds colorExpirationTime = 10s;

// Forward declarations (functions used before they're implemented)
int setColor(String cmd);
int doSomething(String cmd);
int uploadEKGData(String cmd);

void setup()
{
    // Particle functions
    Particle.function("setColor", setColor);
    Particle.function("doSomething", doSomething);
    Particle.function("uploadEKGData", uploadEKGData);

    Serial.begin(9600); // Initialize Serial

    // Pins for Heart Sensor
    pinMode(D0, INPUT); // Setup for leads off detection LO +
    pinMode(D1, INPUT); // Setup for leads off detection LO -
}

void loop()
{
    if (colorSetTime != 0 && millis() - colorSetTime >= colorExpirationTime.count())
    {
        // Revert back to system color scheme
        RGB.control(false);
        colorSetTime = 0;
        Log.info("reverted to normal color scheme");
    }
}

void showlist(std::list<int> g)
{
    std::list<int>::iterator it;
    for (it = g.begin(); it != g.end(); ++it)
    {
        Serial.println(*it);
    }
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
            ekgList.push_back(analogRead(A0));
        }
        // Wait for a bit to keep serial data from saturating
        ekgCounter += 1;
        delay(20);
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

int setColor(String cmd)
{
    int result = 0;

    Log.info("setColor %s", cmd.c_str());

    int red, green, blue;
    if (sscanf(cmd, "%d,%d,%d", &red, &green, &blue) == 3)
    {
        // Override the status LED color temporarily
        RGB.control(true);
        RGB.color(red, green, blue);
        colorSetTime = millis();

        Log.info("red=%d green=%d blue=%d", red, green, blue);
        result = 1;
    }
    else
    {
        Log.info("not red,green,blue");
    }
    return result;
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