/* Sensor.js
	Author: Josh Marasigan, John Nam
 */
 
var b = require('bonescript');
 
// Pin
var trigPin = "P8_8";
var echoPin = "p8_10";

var duration, cm, inches = 0;

b.pinMode(trigPin, b.OUTPUT);
b.pinMode(echoPint, b.INPUT);

// Interval for trig iterate
setInterval(burst, 200)

// Burst signal in increments, anticipate echo
function burst() {
    
    b.digitalWrite(trigPin, b.LOW);
    delay(5);
    b.digitalWrite(trigPin, b.HIGH);
    delay(10);
    b.digitalWrite(trigPin, b.LOW);
    
    // Read from echo pin
    b.analogRead(echoPin, printStatus);
    
    delay(250);
}

// Print distance
function printStatus() {
    console.log('x.value = ' + x.value);
    console.log('x.err = ' + x.err);
}
