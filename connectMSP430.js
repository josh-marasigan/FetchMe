/* Killswitch.js
	Author: Josh Marasigan
 */
var b = require('bonescript');

/* Keep system on until HIGH signal */
var kill = b.LOW;

b.pinMode("GPIO_30", b.INPUT);
b.pinMode("GPIO_31", b.INPUT);
b.pinMode("GPIO_48", b.INPUT);
b.pinMode("GPIO_04", b.INPUT);

/* Kill all systems except processors */
b.pinMode("USR0", b.OUTPUT);
b.pinMode("USR1", b.OUTPUT);
b.pinMode("USR2", b.OUTPUT);

/* All systems die except main for debugging purposes */
b.pinMode("USR3", b.OUTPUT);

/* Get information every 100ms */
setInterval(getKillStatus,100);

function getKillStatus() {
	b.digitalRead('GPIO_30',killSystem);

	function killSystem(x) {
		if(x == b.HIGH) {
			kill = b.HIGH;
			b.digitalWrite('USR0', b.HIGH);
		}
	}
}