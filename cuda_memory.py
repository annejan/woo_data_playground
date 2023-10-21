import time
from tqdm import tqdm
import asciichartpy
import pynvml

# Initialize NVIDIA GPU monitoring
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming you are monitoring GPU 0

def get_gpu_memory():
    """Retrieve the current GPU memory usage in MB"""
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    return meminfo.used / (1024**2)

def monitor_memory_usage(duration, interval):
    """
    Monitor memory usage over time.
    
    :param duration: Total time duration for monitoring (seconds)
    :param interval: Time interval for each data collection (seconds)
    :return: List of memory usage data points
    """
    data_points = []
    num_iterations = int(duration / interval)
    
    for _ in tqdm(range(num_iterations), desc="Monitoring GPU memory", ncols=100):
        mem_used = get_gpu_memory()
        data_points.append(mem_used)
        time.sleep(interval)

    return data_points

if __name__ == "__main__":
    # Collect memory usage data over 10 seconds with 1-second intervals
    data = monitor_memory_usage(10, 1)
    
    # Clear the screen
    print("\033[H\033[J")
    
    # Plot memory usage
    print("Memory usage over time (in MB):\n")
    print(asciichartpy.plot(data, {"height": 15}))

# Shutdown NVIDIA GPU monitoring
pynvml.nvmlShutdown()
