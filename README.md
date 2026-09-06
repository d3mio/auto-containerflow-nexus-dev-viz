# ContainerFlow Nexus: Local Dev Mesh Visualizer GUI

![Python](https://img.shields.io/badge/Language-Python-blue.svg?style=for-the-badge&logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
![AI Generated](https://img.shields.io/badge/Content-AI_Generated-informational.svg?style=for-the-badge)

## Architecture Overview & Problem Statement

**Problem Statement:** In modern software development, local environments frequently leverage complex multi-service containerized applications managed via Docker or Docker Compose. The inherent challenge lies in effectively monitoring, managing, and debugging these intricate "dev mesh" setups. Relying solely on a disparate collection of CLI commands (`docker ps`, `docker stats`, `docker logs`) leads to fragmented visibility, inefficient troubleshooting, and a steep learning curve for developers, significantly impeding productivity and rapid iteration cycles. The absence of a unified, intuitive visual interface exacerbates these issues, turning complex diagnostics into a laborious process.

**Architecture Overview:** ContainerFlow Nexus directly addresses this critical pain point by providing an elite, unified graphical interface for local containerized environments. Engineered in Python with a robust Tkinter-based desktop GUI, the application establishes a direct, secure connection with the local Docker daemon via the `docker-py` SDK. Its architecture is designed for low-latency, real-time data acquisition: continuously polling Docker APIs to retrieve comprehensive metrics on container lifecycle states, granular resource utilization (CPU, memory, network I/O), intricate network configurations, and aggregated log streams. All acquired data is processed client-side and rendered into highly interactive, dynamic visualizations, including real-time resource graphs, intricate network topology diagrams, and consolidated log views. This client-centric, direct Docker interaction model ensures optimal performance, minimal overhead, and an immediate visual representation of your local container infrastructure.

## Features

*   **Real-time Resource Monitoring & Visualization:** Provides dynamic, per-container graphs for CPU utilization, memory consumption, and network I/O (transmit/receive). Offers instantaneous, granular insights into resource allocation and potential performance bottlenecks within your local dev mesh.
*   **Interactive Network Topology Diagrams:** Generates and visualizes the intricate network connections and relationships between containers, services, and Docker networks. Simplifies the understanding of complex multi-service architectures and identifies data flow paths.
*   **Aggregated & Filterable Log Streams:** Centralizes and displays live log output from multiple selected containers into a single, scrollable stream. Includes advanced filtering, search capabilities, and customizable severity highlighting to expedite debugging and event correlation.
*   **Comprehensive Container Lifecycle Management:** Enables interactive control over container states directly from the GUI. Perform essential operations such as start, stop, restart, pause, unpause, and remove containers, alongside the ability to attach to a container's shell (`docker exec`).
*   **Seamless Docker & Docker Compose Integration:** Automatically detects and intelligently manages both standalone Docker containers and complex multi-service applications defined by `docker-compose.yml` files, offering a unified, consistent management experience across all local container assets.
*   **Modern, Customizable User Interface:** Features a sophisticated dark-themed interface by default, designed for optimal readability and reduced eye strain. Provides options for visual customization to adapt to developer preferences and enhance overall user experience.

## Quick Start

### Prerequisites

Ensure the following prerequisites are met on your development machine:

*   **Docker Desktop** or **Docker Engine** installed and actively running.
*   **Python 3.8+**
*   **pip** (Python package installer)

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-org/containerflow-nexus.git
    cd containerflow-nexus
    ```

2.  **Install Required Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` typically includes packages like `docker`, `matplotlib`, `networkx`, `Pillow` for full functionality.)*

### Usage

1.  **Launch the GUI Application:**
    Ensure Docker is running, then execute the main application script:
    ```bash
    python gui_app.py
    ```

## Example Telemetry Output

Upon successful launch and initialization, ContainerFlow Nexus provides real-time feedback and visual insights:

```
Successfully launched ContainerFlow Nexus GUI.
[INFO] Initializing Docker client and API connection...
[INFO] Detecting active Docker containers and services across local daemon.
[INFO] Rendering real-time resource graphs for 3 discovered containers (e.g., 'backend-service', 'frontend-app', 'database').
[INFO] Building interactive network topology for 'my_app_default' bridge network.
[INFO] Aggregating log streams from all active services.

Launched visual GUI application window [Tkinter] with a high-contrast dark theme and real-time Docker container visualization. The interface dynamically displays:
- Dynamic CPU/Memory graphs for 'backend-service' (avg. CPU: 12%, Mem: 256MB)
- An interactive network map illustrating connections between 'frontend-app', 'backend-service', and 'database' over the 'my_app_default' network, including live network I/O.
- A consolidated log stream showcasing the latest events from all services, with filter options for service name, log level, or keyword.
- Active control buttons for the 'database' container (e.g., Stop, Restart, Exec Shell) indicating operational readiness.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.