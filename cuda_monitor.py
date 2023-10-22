import argparse
import time
from collections import deque
import pynvml
import shutil
import asciichartpy
import os

pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)


def get_gpu_memory():
    """Retrieve the current GPU memory usage and total available GPU memory in GB."""
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    used_mem = meminfo.used / (1024**3)  # Convert to GB
    total_mem = meminfo.total / (1024**3)  # Convert to GB
    return used_mem, total_mem


def get_gpu_utilization():
    """Retrieve the current GPU utilization percentage."""
    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
    return utilization.gpu


def console_size():
    """Retrieve the width and height of the console."""
    width, height = shutil.get_terminal_size((20, 50))
    return width, height


def monitor_memory(interval=1):
    """Monitor and plot GPU memory usage and utilization in real-time."""
    width, height = console_size()
    data_points = deque(maxlen=width - 20)
    utilization_points = deque(maxlen=width - 20)

    try:
        while True:
            used_mem, total_mem = get_gpu_memory()
            gpu_utilization = get_gpu_utilization()
            data_points.append((used_mem / total_mem) * 100)
            utilization_points.append(gpu_utilization)

            _, height = console_size()  # Update height in case terminal is resized
            os.system("cls" if os.name == "nt" else "clear")

            # Plot GPU usage in GB
            print(asciichartpy.plot(list(data_points), {"height": (height - 5) // 2}))

            # Plot GPU utilization as a percentage
            print(
                asciichartpy.plot(
                    list(utilization_points), {"height": (height - 5) // 2}
                )
            )

            print(
                f"\nUsed Memory: {used_mem:.2f} GB | Free Memory: {total_mem - used_mem:.2f} GB | Total Memory: {total_mem:.2f} GB | GPU Utilization: {gpu_utilization}%"
            )

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monitor GPU memory usage and utilization in real-time."
    )
    parser.add_argument(
        "--interval_seconds",
        "-s",
        type=float,
        default=1,
        help="Interval in seconds between memory checks and utilization checks.",
    )
    args = parser.parse_args()

    monitor_memory(args.interval_seconds)

pynvml.nvmlShutdown()
