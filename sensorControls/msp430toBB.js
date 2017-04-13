
var b = require('bonescript');

b.pinMode("USR0", b.OUTPUT);
b.pinMode("USR1", b.OUTPUT);
b.pinMode("USR2", b.OUTPUT);
b.pinMode("USR3", b.OUTPUT);

b.digitalWrite("USR0", b.LOW);
b.digitalWrite("USR1", b.LOW);
b.digitalWrite('USR2', b.LOW);
b.digitalWrite('USR3', b.LOW);
b.pinMode("P8_8", b.OUTPUT);
b.digitalWrite("P8_8", b.HIGH);
b.pinMode("P8_9", b.OUTPUT);
b.digitalWrite("P8_9", b.HIGH)
b.pinMode("P8_11", b.OUTPUT);
b.digitalWrite("P8_11", b.HIGH);
b.pinMode("P8_14", b.OUTPUT);
b.digitalWrite("P8_14", b.HIGH);

b.analogRead("P9_36",stop);

/* Get information every 1000ms */
setInterval(isObstruction, 200);
var state = b.LOW;
var interrupt = false;
var interrupt_count = 0;
    
clearDirection = [];

// Filling
for (n = 0; n < 4; ++n) {
    clearDirection[n] = false;
}

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
    
  //  if(interrupt === false) {
    
        if(x.value > .95) {
            b.digitalWrite("USR3", b.HIGH);
           b.digitalWrite("P8_8", b.HIGH);
             b.digitalWrite("P8_9", b.HIGH);
             interrupt = true;
         //   b.digitalWrite("P8_11", b.HIGH);
         //    b.digitalWrite("P8_14", b.HIGH);
        }
        else {
            b.digitalWrite("USR3", b.LOW);
            
           //motorControl();
            
        //   b.digitalWrite("P8_8", b.HIGH);
        //   b.digitalWrite("P8_9", b.HIGH);
         //   b.digitalWrite("P8_11", b.HIGH);
         //   b.digitalWrite("P8_14", b.HIGH);
        }
    }
    // Wait 3 seconds. 15 cycles
    else {
        
       b.digitalWrite("P8_9", b.LOW);
        b.digitalWrite("P8_8", b.HIGH);
        
        if(interrupt_count < 15) {
            
//            // Deal with this shit
            console.log(interrupt_count);
            
        }
        var p = 0;
        for(var i = 0; i < 4; i++) {
            if(clearDirection[n] == true) {
                p++;
            }
        }
        
        if(p > 0) {
            interrupt = true;
        }
        else {
            interrupt = false;
        }
//        interrupt_count++;
//    }
}

//function motorControl(x) {
//    console.log("Test");
    
    
//}
