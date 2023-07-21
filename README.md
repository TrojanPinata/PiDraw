# PiDraw

![drawing robot built by me](https://i.imgur.com/l32Rj4b.jpg)
![result](https://i.imgur.com/Ef2MCmU.jpg)

This is a drawing robot I built similar to my Prusa Mini+, which I designed and coded myself using off the shelf components and 3D printed structural supports. My goal was to write code which could take in an image and reproduce a copy of it (in binary color) onto a page. The goal was slightly extended to drawing an outline as well, but that is secondary to its functionality  as a pseudo-dot-matrix printer.

[Video of robot running with v/o](https://youtu.be/3Vgg1YUDOpk)

The original design used a [Adafruit stepper driver](https://www.adafruit.com/product/2348), which was not up to the task of driving two 1.2A motors, and quietly died. The driver.py script is the remnant of that, and utilizes the adafruit_motor and motorkit packages to work. As I switched to the L298Ns, I designed a driver from scratch (motor.py) which interfaces with dot.py. If you are attempting to reuse this code with that adafruit stepper driver, modifying the picture.py file should be easy, but be aware that driver.py is several iterations behind.

This robot uses opencv and potrace to print and is based around a Pi 4, three L298N motor drivers, two Nema 17 1.2A motors, and a 12V solenoid. The axis are belt driven and utilize a plate based y-axis in order to reduce moving parts.

![Schematic](https://i.imgur.com/D4MiPwX.png)

Note: L298Ns are rated for ~2A which is below the inrush current from the inductive load. They will get hot and burn out after extended use. I have gone through four boards/chips just testing this process. I understand the risks of doing this, but it is much cheaper than getting a more expensive motor driver for a project like this.

Do not touch the motor drivers or motors during use, they will burn you. I used active cooling to slow this process.

![oops](https://i.imgur.com/qz85ows.jpg)