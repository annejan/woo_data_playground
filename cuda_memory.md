# GPU Memory Monitor

Monitor your GPU memory usage in real-time with an ASCII-based console graph.

## Overview

This script provides a real-time plot of your GPU's memory usage right in the terminal. It leverages NVIDIA's Management Library (NVML) to fetch memory usage statistics and presents them with a dynamic ASCII chart. It also displays used, free, and total memory statistics below the chart.

## Prerequisites

- An NVIDIA GPU and the corresponding drivers installed.
- Python 3.x
- The required Python libraries: `pynvml`, `shutil`, and `asciichartpy`. You can install them using:

  ```bash
  pip install pynvml asciichartpy
  ```

## Usage

1. Clone the repository or download the script.
2. Run the script:

    ```bash
    python cuda_memory.py
    ```

3. The GPU memory usage will be plotted in real-time in your terminal. Below the chart, you will find the statistics for used, free, and total GPU memory.
4. To stop the monitoring, press `CTRL+C`.

## Features

- Real-time GPU memory monitoring
- Dynamic chart that adapts to console width and height
- Displays used, free, and total GPU memory statistics

## Acknowledgements

This script utilizes:

- [pynvml](https://pypi.org/project/pynvml/) for accessing NVIDIA GPU stats.
- [asciichartpy](https://pypi.org/project/asciichartpy/) for plotting in the console.

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
