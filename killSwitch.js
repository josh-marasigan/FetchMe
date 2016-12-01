/* Killswitch.js
	Author: Josh Marasigan
 */
var b = require('bonescript');

/* Keep system on until HIGH signal */
var kill = 0;
var toggle = b.LOW;

/* I/O Pins */
var GPIO = [
	"P9_11", 
	"P9_13", 
	"P9_15", 
	"P9_17",
	"P9_21",
	"P9_23"
];

/* LED Out */
var USR = [
	"USR0", 
	"USR1", 
	"USR2", 
	"USR3"
];

b.pinMode(GPIO[0], b.INPUT);
b.pinMode("P9_11", b.OUTPUT);
b.pinMode("P9_13", b.OUTPUT);
b.pinMode("P9_15", b.OUTPUT);

/* All 'systems' killed except main (USR4) for debugging purposes */
b.pinMode(GPIO[4], b.OUTPUT);
b.pinMode(GPIO[5], b.OUTPUT);
b.pinMode(USR[0], b.OUTPUT);
b.pinMode(USR[1], b.OUTPUT);
b.pinMode(USR[2], b.OUTPUT);
b.pinMode(USR[3], b.OUTPUT);

/* Initialize */
b.digitalWrite("P9_11", b.HIGH);
b.digitalWrite("P9_13", b.HIGH);
b.digitalWrite("P9_15", b.HIGH);
b.digitalWrite(GPIO[4], b.LOW);
b.digitalWrite(GPIO[5], b.LOW);

b.digitalWrite("USR0", b.LOW);
b.digitalWrite(USR[1], b.LOW);
b.digitalWrite(USR[2], b.LOW);
b.digitalWrite(USR[3], b.LOW);

/* Get information every 100ms */
setInterval(getKillStatus,100);

/* Flash when kill state */
setInterval(killed, 2000);

function killed() {
	if(kill == 1) {
		if(toggle == b.LOW) toggle = b.HIGH;
    	else toggle = b.LOW;
    	b.digitalWrite(GPIO[4], toggle);
    	b.digitalWrite(GPIO[5], toggle);
	}
}

function getKillStatus() {
	b.digitalRead(GPIO[0],killSystem);

	function killSystem(x) {
		if(x == b.HIGH) {
			kill = 1;
			b.digitalWrite("USR0", b.HIGH);
			b.digitalWrite("USR1", b.HIGH);
			b.digitalWrite('USR2', b.HIGH);
			b.digitalWrite('USR4', b.HIGH);
			b.digitalWrite(GPIO[4], b.HIGH);
			b.digitalWrite(GPIO[5], b.HIGH);
			
			b.digitalWrite(GPIO[1], b.LOW);
            b.digitalWrite(GPIO[2], b.LOW);
            b.digitalWrite(GPIO[3], b.LOW);
		}
	}
}
