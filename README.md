## FetchMe
<p align="center">
  <img width="400" height="300" src="http://tinyimg.io/i/H6cgMyd.png"><br>
  <strong>Autonomous Campus delivery for The University of Texas at Austin</strong>
</p>

## Inspiration

FetchMe is a senior design capstone project for The University of Texas ECE department. 
Driver-less cars are an emerging technology which has the potential to impact many different industries. However, many people are afraid of the technology and its effect on the future of driving. Our group hopes to shed light, and potentially lunch, on the benefits of autonomous technology! We aim to develop a retrofitted RC car that will display the safety and usefulness of autonomous vehicles in the real world. The RC car will do so by performing simple tasks on the UT campus, such as delivering mail or food to requesting students or faculty.<br>

With the help of our industry sponsor, Texas Instruments, and our faculty mentor, Dr. David Pan, we hope to make UT Austin the first university in the world to have autonomous delivery for its students!

## Design Overview and GPIO Ports
<p align="center">
  <img width="600" height="400" src="http://tinyimg.io/i/FkfJGkR.PNG"><br>
  <strong>Top Level Block Diagram</strong>
</p><br><br>

<strong><u>GPIO (BeagleBone) to Motor Control</u></strong><br>
<b>P8_8</b>: Rear Motor (Forward)<br>
<b>P8_9</b>: Rear Motor (Reverse)<br>
<b>P8_11</b>: Front Motor (Turns Left)<br>
<b>P8_14</b>: Front Motor (Turns Right)<br>

<strong><u>GPIO (MSP430) to Ulstrasonic Sensor Control (BeagleBone)</u></strong><br>
<i>BeagleBone Input</i><br>
<b>AIN2 (P9_37)</b>: Front Sensor<br>
<b>AIN3 (P9_38)</b>: Right Sensor<br>
<b>AIN0 (P9_39)</b>: Left Sensor<br>
<b>AIN1 (P9_40)</b>: Back Sensor<br>

<b><u>MSP430 Output</u></b><br>
<b>P1.1</b>: Obstruction Flag (High when F/R/L/B Sensor Echo returns High)<br>

<i>MSP430 Input from 'ECHO' Sensor Pin</i><br>
<b>P1.0</b>: Front Sensor<br>
<b>P1.6</b>: Right Sensor<br>
<b>P2.1</b>: Left Sensor<br>
<b>P2.2</b>: Back Sensor<br>

<strong><u>GPIO for Heartbeats</u></strong><br>
<b>P8_44</b><br>
<b>USR2</b><br>
<b>USR3</b><br>
<br>

## Contributers
<p>
<b>Erik Gill</b> - Communication Networks and Integrated Circuits <br>
  <a href="https://www.linkedin.com/in/john-nam-a8a629116/" style="text-decoration: none">
  <b>John Nam</b></a> - Energy Systems and Renewable Energy<br>
  <a href="https://www.linkedin.com/in/joshmarasigan/" style="text-decoration: none">
  <b>Josh Marasigan</b></a> - Software Engineering and Design<br>
  <a href="https://www.linkedin.com/in/ross-han-30567489/" style="text-decoration: none">
  <b>Ross Han</b></a> - Energy Systems and Renewable Energy<br>
  <a href="https://www.linkedin.com/in/yueheng-zhang/" style="text-decoration: none">
  <b>Yueheng (Henry) Zhang</b></a> - Software Engineering and Design<br>
</p>

## Faculty Mentors
<p>
  <a href="http://www.ece.utexas.edu/people/faculty/david-z-pan" style="text-decoration: none"><b>Dr. David Z. Pan</b></a> – Faculty Mentor
</p>

## Follow Our Blog!
https://autonomousdesignproject.wordpress.com/
