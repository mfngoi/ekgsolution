int counter = 1;

void setup() { }

void loop() {
    Particle.publish("PublishTest", String(counter));
    counter++;
    delay(5000);

}