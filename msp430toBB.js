
var b = require('bonescript');
 
b.pinMode("USR0", b.OUTPUT);
b.pinMode("USR1", b.OUTPUT);
b.pinMode("USR2", b.OUTPUT);
b.pinMode("USR3", b.OUTPUT);

b.digitalWrite("USR0", b.LOW);
b.digitalWrite("USR1", b.LOW);
b.digitalWrite('USR2', b.LOW);
b.digitalWrite('USR3', b.LOW);
b.pinMode("P8_7", b.OUTPUT);
b.digitalWrite("P8_7", b.HIGH);

b.analogRead("P9_36",stop);

/* Get information every 1000ms */
setInterval(isObstruction, 200);
var state = b.LOW;
    
function isObstruction() {
    
    if(state == b.LOW) state = b.HIGH;
    else state = b.LOW;
    b.digitalWrite("USR0", state);
    
    console.log("poll")
    b.analogRead("P9_36",stop);

}

function stop(x) {
    
    console.log('x.value = ' + x.value);
    console.log('x.err = ' + x.err);
    
    if(x.value >= .99) {
        b.digitalWrite("USR3", b.HIGH);
         b.digitalWrite("P8_7", b.LOW);
    }
    else {
        b.digitalWrite("USR3", b.LOW);
         b.digitalWrite("P8_7", b.HIGH);
    }
}
