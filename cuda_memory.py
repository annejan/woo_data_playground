import time
from collections import deque
import pynvml
import shutil
import asciichartpy
import os

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

def get_gpu_memory():
    """Retrieve the current GPU memory usage in GB."""
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return meminfo.used / (1024**3)  # Convert to GB

def console_size():
    """Retrieve the width and height of the console."""
    width, height = shutil.get_terminal_size((20, 50))
    return width, height

def monitor_memory(interval=1):
    """Monitor and plot GPU memory usage in real-time."""
    width, height = console_size()
    # Number of points to keep is based on console width
    data_points = deque(maxlen=width - 20)

    try:
        while True:
            mem_used = get_gpu_memory()
            data_points.append(mem_used)

            _, height = console_size()  # Update height in case terminal is resized
            os.system('cls' if os.name == 'nt' else 'clear')
            print(asciichartpy.plot(list(data_points), {'height': height - 5}))  # Leaving some margin for plot labels

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_memory()

pynvml.nvmlShutdown()

