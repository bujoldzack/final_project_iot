import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import threading

DATA_Pin = 17
CLK_Pin  = 4

# Set up GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Red Button
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Blue Button
GPIO.setup(18, GPIO.OUT) # Buzzer
GPIO.setup(21, GPIO.OUT) # Red LED
GPIO.setup(20, GPIO.OUT) # Green LED
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Open Container Button
GPIO.output(21, GPIO.LOW)
GPIO.output(20, GPIO.HIGH)
GPIO.setup(DATA_Pin, GPIO.OUT)
GPIO.setup(CLK_Pin,  GPIO.OUT)
GPIO.output(DATA_Pin, GPIO.LOW)
GPIO.output(CLK_Pin,  GPIO.LOW)


# Initialize the sensor with trigger and echo pins
sensor = DistanceSensor(echo=22, trigger=27)

# Function to handle button presses
def button_pressed(channel):
    global button_presses
    button_presses.append(channel)
    if len(button_presses) == 1:
        global sequence_timer
        sequence_timer = threading.Timer(3, check_sequence)  # 3 seconds timeout
        sequence_timer.start()

# Function to check button sequence
def check_sequence():
    global button_presses
    if button_presses == [12, 16, 12]:
        status_label.config(text="Status: Unlocked")
        GPIO.output(20, GPIO.LOW) # Green LED
        GPIO.output(21, GPIO.HIGH)  # Red LED
    else:
        status_label.config(text="Status: Locked")
        GPIO.output(20, GPIO.HIGH)  # Green LED
        GPIO.output(21, GPIO.LOW) # Red LED
    button_presses = []

# Function to handle opening the container
def open_container():
    if "Locked" in status_label.cget("text"):
        alert_label.config(text="Alert: Container opened without authorization")
        # Activate passive buzzer for alert sound
        buzzer_thread = threading.Thread(target=activate_buzzer)
        buzzer_thread.start()
    else:
        alert_label.config(text="Alert: Container opened with authorization")

# Function to activate buzzer
def activate_buzzer():
    buzzer_frequency = 1000  # Set the buzzer frequency (in Hz)
    buzzer_duration = 0.1  # Set the duration of each beep (in seconds)
    num_beeps = 3  # Set the number of beeps
    buzzer_pwm = GPIO.PWM(18, buzzer_frequency)
    buzzer_pwm.start(50)  # Start PWM with a duty cycle of 50% (default)
    for _ in range(num_beeps):
        buzzer_pwm.ChangeFrequency(buzzer_frequency)  # Set the buzzer frequency
        time.sleep(buzzer_duration)  # Wait for the duration of the beep
        buzzer_pwm.stop()  # Turn off the buzzer
        time.sleep(buzzer_duration)  # Wait for the same duration before the next beep

# Function to update threshold label
def update_threshold_label(value):
    rounded_value = round(float(value))
    threshold_label.config(text=f"{rounded_value}%")

# Function to update waste level and LED bar
def update_waste_level():
    # Get average distance measured by the sensor (in meters)
    distance = get_distance()

    # Convert distance to percentage for waste level
    waste_percentage = (1 - distance) * 100

    # Get the threshold value set by the user
    threshold_value = threshold.get()

    # Adjust the waste percentage based on the threshold
    if waste_percentage > threshold_value:
        adjusted_percentage = threshold_value
    else:
        adjusted_percentage = waste_percentage

    # Update the waste level progress bar
    waste_level["value"] = adjusted_percentage
    # Update the waste level label
    waste_label.config(text=f"{adjusted_percentage:.1f}%")
    global hex_level
    hex_level = 0x0000

    if adjusted_percentage < 20:
        hex_level = 0x0003
        send16bitData(CmdMode)
        sendLED(hex_level)
        latchData()
    if adjusted_percentage > 20 and adjusted_percentage < 40:
        hex_level = 0x000f
        send16bitData(CmdMode)
        sendLED(hex_level)
        latchData()
    if adjusted_percentage > 40 and adjusted_percentage < 60:
        hex_level = 0x003f
        send16bitData(CmdMode)
        sendLED(hex_level)
        latchData()
    if adjusted_percentage > 60 and adjusted_percentage < 80:
        hex_level = 0x00ff
        send16bitData(CmdMode)
        sendLED(hex_level)
        latchData()
    if adjusted_percentage > 80 and adjusted_percentage < 100:
        hex_level = 0x03ff
        send16bitData(CmdMode)
        sendLED(hex_level)
        latchData()
    # Schedule the next update
    root.after(100, update_waste_level)

# Function to get distance from HC-SR04 sensor
def get_distance():
    return sensor.distance

# Function to handle open container button press
def open_button_pressed(channel):
    open_container()

CmdMode  = 0x0000  # Work on 8-bit mode
ON       = 0x00ff  # 8-byte 1 data
SHUT     = 0x0000  # 8-byte 0 data
global s_clk_flag
s_clk_flag = 0

def send16bitData(data):
        global s_clk_flag
        for i in range(0, 16):
                if data & 0x8000:
                        GPIO.output(DATA_Pin, GPIO.HIGH)
                else:
                        GPIO.output(DATA_Pin, GPIO.LOW)

                if s_clk_flag == True:
                        GPIO.output(CLK_Pin, GPIO.LOW)
                        s_clk_flag = 0
                else:
                        GPIO.output(CLK_Pin, GPIO.HIGH)
                        s_clk_flag = 1
                time.sleep(0.001)
                data = data << 1

def latchData():
        latch_flag = 0
        GPIO.output(DATA_Pin, GPIO.LOW)

        time.sleep(0.05)
        for i in range(0, 8):
                if latch_flag == True:
                        GPIO.output(DATA_Pin, GPIO.LOW)
                        latch_flag = 0
                else:
                        GPIO.output(DATA_Pin, GPIO.HIGH)
                        latch_flag = 1
        time.sleep(0.05)

def sendLED(LEDstate):
        for i in range(0, 12):
                if (LEDstate & 0x0001) == True:
                        send16bitData(ON)
                else:
                        send16bitData(SHUT)
                LEDstate = LEDstate >> 1

def loop():
        while True:
                global hex_level
                hex_level = 0x000
                while hex_level <= 0x03ff:
                        send16bitData(CmdMode)
                        sendLED(hex_level)
                        latchData()

def destroy():
        GPIO.cleanup()

# Initialize button_presses list
button_presses = []

# Add event detection for button presses
GPIO.add_event_detect(16, GPIO.FALLING, callback=button_pressed, bouncetime=200)
GPIO.add_event_detect(12, GPIO.FALLING, callback=button_pressed, bouncetime=200)
GPIO.add_event_detect(26, GPIO.FALLING, callback=open_button_pressed, bouncetime=200)

root = tk.Tk()
root.title("Waste Management")
root.geometry("320x300")

frame_waste_level = ttk.Frame(root, padding=10)
frame_waste_level.grid(row=0, column=0, sticky=(tk.W, tk.E))
ttk.Label(frame_waste_level, text="Waste Level").grid(row=0, column=0, sticky=tk.W)
waste_level = ttk.Progressbar(frame_waste_level, length=200, maximum=100, value=60)
waste_level.grid(row=1, column=0, sticky=tk.W)
waste_label = ttk.Label(frame_waste_level, text="60.0%")
waste_label.grid(row=1, column=1, sticky=tk.W)

frame_threshold = ttk.Frame(root, padding=10)
frame_threshold.grid(row=1, column=0, sticky=(tk.W, tk.E))
ttk.Label(frame_threshold, text="Set Threshold:").grid(row=0, column=0, sticky=tk.W)
threshold = ttk.Scale(frame_threshold, from_=0, to=100, orient=tk.HORIZONTAL, value=80, command=update_threshold_label)
threshold.grid(row=0, column=1, sticky=tk.W)
threshold_label = ttk.Label(frame_threshold, text="")
threshold_label.grid(row=0, column=2, sticky=tk.W)

frame_status = ttk.Frame(root, padding=10)
frame_status.grid(row=2, column=0, sticky=(tk.W, tk.E))
status_label = ttk.Label(frame_status, text="Status: Locked")
status_label.grid(row=0, column=0, sticky=tk.W)

frame_buttons = ttk.Frame(root, padding=10)
frame_buttons.grid(row=3, column=0, sticky=(tk.W, tk.E))
open_button = ttk.Button(frame_buttons, text="Open Container", command=open_container)
open_button.grid(row=0, column=0, padx=5)
alert_label = ttk.Label(frame_buttons, text="Alert: No unauthorized access detected")
alert_label.grid(row=1, column=0, padx=5)

root.grid_columnconfigure(0, weight=1)

# Start the periodic update of the waste level
update_waste_level()

root.mainloop()
