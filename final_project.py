import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
import time

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(16, GPIO.FALLING, callback=button1_pressed)
    GPIO.add_event_detect(12, GPIO.FALLING, callback=button2_pressed)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.IN)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    while True:
        measure_distance()
        time.sleep(1)

active1 = False
active2 = False

def toggle_green(pin):
    global active1
    if active1:
        GPIO.output(pin, GPIO.LOW)
        active = False
    else:
        GPIO.output(pin, GPIO.HIGH)
        active = True

def toggle_red(pin):
    global active2
    if active2:
        GPIO.output(pin, GPIO.LOW)
        active = False
    else:
        GPIO.output(pin, GPIO.HIGH)
        active = True


def button1_pressed(channel):
    print("Button 1 pressed")
    toggle_green(5)

def button2_pressed(channel):
    print("Button 2 pressed")
    toggle_red(6)

def measure_distance():
    global start_time, end_time

    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(27, GPIO.LOW)

    start_time = time.time()
    while GPIO.input(22) == 0:
        start_time = time.time()

    end_time = time.time()
    while GPIO.input(22) == 1:
        end_time = time.time()

    duration = end_time - start_time
    distance = duration * 17000
    distance = round(distance, 2)
    print("Distance:", distance, "cm")
    if distance < 10:
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)
    num_leds = int(min(max(distance / 100, 0), 10))
    for i in range(10):
        if i < num_leds:
            GPIO.output(17, GPIO.HIGH)
        else:
            GPIO.output(17, GPIO.LOW)
        time.sleep(0.05)

def clear_gpio():
    GPIO.cleanup()
    print("GPIO settings cleared")


def main():

    root = tk.Tk()
    root.title("Waste Management")
    root.geometry("250x250")

    frame_waste_level = ttk.Frame(root, padding=10)
    frame_waste_level.grid(row=0, column=0, sticky=(tk.W, tk.E))
    ttk.Label(frame_waste_level, text="Waste Level").grid(row=0, column=0, sticky=tk.W)

    waste_level = ttk.Progressbar(frame_waste_level, length=200, maximum=100, value=60)
    waste_level.grid(row=1, column=0, sticky=tk.W)
    ttk.Label(frame_waste_level, text="60%").grid(row=1, column=1, sticky=tk.W)

    frame_threshold = ttk.Frame(root, padding=10)
    frame_threshold.grid(row=1, column=0, sticky=(tk.W, tk.E))
    ttk.Label(frame_threshold, text="Set Threshold:").grid(row=0, column=0, sticky=tk.W)

    threshold = ttk.Scale(frame_threshold, from_=0, to=100, orient=tk.HORIZONTAL, value=80)
    threshold.grid(row=0, column=1, sticky=tk.W)
    ttk.Label(frame_threshold, text="80%").grid(row=0, column=2, sticky=tk.W)

    frame_status = ttk.Frame(root, padding=10)
    frame_status.grid(row=2, column=0, sticky=(tk.W, tk.E))
    ttk.Label(frame_status, text="Status: Locked").grid(row=0, column=0, sticky=tk.W)
    ttk.Label(frame_status, text="Unlock Sequence:").grid(row=0, column=1, sticky=tk.W)

    frame_alert = ttk.Frame(root, padding=10)
    frame_alert.grid(row=3, column=0, sticky=(tk.W, tk.E))
    ttk.Label(frame_alert, text="Alert: No unauthorized access detected").grid(row=0, column=0, sticky=tk.W)

    setup_gpio()

    root.grid_columnconfigure(0, weight=1)
    root.mainloop()

if __name__ == "__main__":
    main()
