import argparse
import time
from collections import deque
import pynvml
import shutil
import asciichartpy
import os

pynvml.nvmlInit()
gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)


def fetch_gpu_memory():
    """Retrieve the current GPU memory usage and total available GPU memory in GB."""
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(gpu_handle)
    used = meminfo.used / (1024**3)
    total = meminfo.total / (1024**3)
    return used, total


def get_gpu_utilization():
    """Retrieve the current GPU utilization percentage."""
    utilization = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
    return utilization.gpu


def terminal_dimensions():
    """Retrieve the width and height of the console."""
    width, height = shutil.get_terminal_size((20, 50))
    return width, height


def monitor_gpu_stats(interval=1):
    """Monitor and plot GPU memory usage percentage and utilization in real-time."""
    width, height = terminal_dimensions()
    memory_points = deque(maxlen=width - 20)
    utilization_points = deque(maxlen=width - 20)

    try:
        while True:
            used_memory, total_memory = fetch_gpu_memory()
            gpu_usage = get_gpu_utilization()
            memory_points.append((used_memory / total_memory) * 100)
            utilization_points.append(gpu_usage)

            (
                _,
                height,
            ) = terminal_dimensions()  # Update height in case terminal is resized
            os.system("cls" if os.name == "nt" else "clear")

            print(
                asciichartpy.plot(
                    [list(memory_points), list(utilization_points)],
                    {"height": height - 5},
                )
            )

            print(
                f"\nUsed Memory: {used_memory:.2f} GB | Free Memory: {total_memory - used_memory:.2f} GB | Total Memory: {total_memory:.2f} GB | GPU Utilization: {gpu_usage}%"
            )

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monitor GPU memory usage percentage and utilization in real-time."
    )
    parser.add_argument(
        "--interval_seconds",
        "-s",
        type=float,
        default=1,
        help="Interval in seconds between memory percentage checks and GPU utilization checks.",
    )
    args = parser.parse_args()

    monitor_gpu_stats(args.interval_seconds)

pynvml.nvmlShutdown()
