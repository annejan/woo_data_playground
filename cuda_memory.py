import time
import torch
import os
from tqdm import tqdm
import asciichartpy

def display_cuda_memory_usage():
    """Return CUDA memory usage in GB."""
    t = torch.cuda.get_device_properties(0).total_memory
    r = torch.cuda.memory_reserved(0)
    a = torch.cuda.memory_allocated(0)

    used_memory = a / (1024 ** 3)
    return used_memory

def monitor_cuda_memory_and_time_graph(duration=10, interval=1):
    """Monitor CUDA memory and integrate with tqdm and asciichartpy."""

    memory_values = []
    progress_bar = tqdm(total=int(duration / interval), position=0, leave=True)

    for _ in range(int(duration / interval)):
        used_memory = display_cuda_memory_usage()
        memory_values.append(used_memory)

        _, console_width = os.get_terminal_size()
        # Limit the plot to console width by dropping old values
        while len(asciichartpy.plot(memory_values)) > console_width:
            memory_values.pop(0)
        
        # Print memory graph to console
        print("\033c")  # Clear the console
        print(asciichartpy.plot(memory_values))
        
        # Update the progress bar
        progress_bar.update(1)
        progress_bar.refresh()
        time.sleep(interval)

    progress_bar.close()

monitor_cuda_memory_and_time_graph(duration=30)

