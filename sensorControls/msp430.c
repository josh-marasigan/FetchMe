//#include <msp430g2553.h>
#include <msp430.h>

int miliseconds;
int miliseconds2;
int miliseconds3;
int distance1;
int distance2;
int distance3;
long sensor1;
long sensor2;
long sensor3;

void main(void)
{
  BCSCTL1 = CALBC1_1MHZ;
  DCOCTL = CALDCO_1MHZ;                     // submainclock 1mhz
  WDTCTL = WDTPW + WDTHOLD;                 // Stop WDT

  CCTL0 = CCIE;                             // CCR0 interrupt enabled
  CCR0 = 1000;                              // 1ms at 1mhz
  TACTL = TASSEL_2 + MC_1;                  // SMCLK, upmode

  P1IFG  = 0x00;                            //clear all interrupt flags
  P1DIR |= 0x41;                            // P1.0 and P1.6 as output for LED
  P1OUT &= ~0x41;                           // turn LED off
  P2IFG  = 0x00;                            //clear all interrupt flags
  P2DIR |= 0x04;                            // P2.2  as output for LED
  P2OUT &= ~0x04;                           // turn LED off


  _BIS_SR(GIE);                             // global interrupt enable

 while(1){
    P1IE &= ~0x01;          // disable interrupt
    P1DIR |= 0x02;          // P1.1 trigger pin as output for all ultrasonic sensors
    P1OUT |= 0x02;          // generate pulse
    __delay_cycles(10);     // for 10us
    P1OUT &= ~0x02;         // stop pulse
    P1DIR &= ~0x94;         // make pin P1.2, 1.4 and p1.7 input (ECHO)
    P1IFG = 0x00;           // clear flag just in case anything happened before
    P1IE |= 0x94;           // enable interrupt on ECHO pin
    P1IES &= ~0x94;         // rising edge on ECHO pin
//    P2IE &= ~0x01;          // disable interrupt
//    P2DIR &= ~0x01;         // make pin P2.0 input (ECHO)
//    P2IFG = 0x00;           // clear flag just in case anything happened before
//    P2IE |= 0x01;           // enable interrupt on ECHO pin
//    P2IES &= ~0x01;         // rising edge on ECHO pin
    __delay_cycles(30000);          // delay for 0.5s (after this time echo times out if there is no object detected)
    distance1 = sensor1/58;           // converting ECHO length into cm
    distance2 = sensor2/58;           // converting ECHO length into cm
    distance3 = sensor3/58;           // converting ECHO length into cm
   if(distance1 < 100 && distance1 != 0) P1OUT |= 0x01;  //turning LED on if distance is less than 20cm and if distance isn't 0.
       else P1OUT &= ~0x01;
   if(distance2 < 100 && distance2 != 0) P1OUT |= 0x40;  //turning LED on if distance is less than 20cm and if distance isn't 0.
     else P1OUT &= ~0x40;
   if(distance3 < 100 && distance3 != 0) P2OUT |= 0x04;  //turning LED on if distance is less than 20cm and if distance isn't 0.
        else P2OUT &= ~0x04;
 }
}

#pragma vector=PORT1_VECTOR
__interrupt void Port_1(void)
{
    if(P1IFG&0x04)  //is there interrupt pending?
        {
          if(!(P1IES&0x04)) // is this the rising edge?
          {
            TACTL|=TACLR;   // clears timer A
            miliseconds = 0;
            P1IES |= 0x04;  //falling edge
          }
          else
          {
            sensor1 = (long)miliseconds*1000 + (long)TAR;    //calculating ECHO length
          }
          P1IFG &= ~0x04;             //clear flag
    }

    if(P1IFG&0x10)  //is there interrupt pending?
    {
          if(!(P1IES&0x10)) // is this the rising edge?
          {
            TACTL|=TACLR;   // clears timer A
            miliseconds2 = 0;
            P1IES |= 0x10;  //falling edge
          }
          else
          {
            sensor2 = (long)miliseconds2*1000 + (long)TAR;    //calculating ECHO length
          }
          P1IFG &= ~0x10;             //clear flag
     }
    if(P1IFG&0x80)  //is there interrupt pending?
        {
          if(!(P1IES&0x80)) // is this the rising edge?
          {
            TACTL|=TACLR;   // clears timer A
            miliseconds3 = 0;
            P1IES |= 0x80;  //falling edge
          }
          else
          {
            sensor3 = (long)miliseconds3*1000 + (long)TAR;    //calculating ECHO length
          }
          P1IFG &= ~0x80;             //clear flag
    }

}

#pragma vector=TIMER0_A0_VECTOR
__interrupt void Timer_A (void)
{
  miliseconds++;
  miliseconds2++;
  miliseconds3++;
}

