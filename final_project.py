import tkinter as tk
from tkinter import ttk

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

    root.grid_columnconfigure(0, weight=1)
    root.mainloop()

if __name__ == "__main__":
    main()
