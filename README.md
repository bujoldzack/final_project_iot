# Project Overview
The objective of the smart waste management system is to efficiently monitor and regulate waste levels within containers by employing a variety of IoT hardware and software. It utilizes ultrasonic sensors to measure the fullness of trash containers. The data collected by these sensors is then visually displayed through a user interface developed with Tkinter, allowing for real-time monitoring and management. Additionally, the system includes a security feature that uses a button-based locking mechanism and an alarm system to alert unauthorized access, and then ensures the security and integrity of the disposal process.

# Hardware Components
1. Raspberry Pi & Extension Board
2. Passive Buzzer: To alert when the container is accessed unauthorized.
3. LEDs Green and Red: For the status of the lock (correct and incorrect code).
4. LED Bar Graph: For visual indication of the waste levels outside the container.
5. HC-SR04 Ultrasonic Sensor: To measure the waste level inside the container.
6. Red and Blue Buttons: For entering the security code to unlock the trash container.
7. Connectors

# GPIO Pins Used
1.	HC-SR04 Ultrasonic Sensor: Trigger to GPIO27, Echo to GPIO22
2.	LED Bar: DI to GPIO17
3.	Red LED: GPIO21
4.	Green LED: GPIO20
5.	Red Button: GPIO16
6.	Blue Button: GPIO12
7.	Passive Buzzer: GPIO18

# Code Implemementation
The Python code handles sensor data acquisition, GUI development, and control logic for security and alert systems. It utilizes libraries such as Tkinter for the GUI, RPi.GPIO for GPIO pin manipulation, and gpiozero for sensor integration.

# User Manuel
Operating Instructions:
1. Waste Level Monitoring:
Launch the application on the Raspberry Pi.
The GUI will display the waste level in real-time, both numerically and visually through the LED bar graph.
2. Setting Thresholds:
Use the threshold scale provided in the GUI to set a threshold for waste level.
Adjust the threshold according to your preference (e.g., 80% full).
3. Security System:
To unlock the trash container, press the buttons in the sequence: Blue, Red, Blue within a 3-second interval.
Green LED indicates a correct sequence, while the Red LED indicates an incorrect sequence.
4. Alarm System:
If the container is opened without authorization, the passive buzzer will sound.