# PENETRATION-TESTING-TOOLKIT
***COMPANY***: CDETECH IT SOLUTION

***NAME***: Sobiya vhora

***INTERN ID***: CT08GRD

***DOMAIN***: Cyber Security & Ethical Hacking

***BATCH DURATION***: December 25th, 2024 to January 25th, 2025

***MENTOR NAME***: Neela Santhosh

***DESCRIPTION OF TASK-3***

# Async Port Scanner

## Objective
The Async Port Scanner is an efficient, user-friendly tool designed for scanning open ports on target hosts. It uses asynchronous programming to maximize performance, identifies services running on open ports, and provides the ability to scan a range of IP addresses or ports. Additionally, it offers a GUI for ease of use and generates detailed reports in CSV format.

---

## Features

1. **Asynchronous Scanning**:
   - Utilizes Python's `asyncio` library for efficient and concurrent port scanning.

2. **Service Identification**:
   - Detects services using `socket.getservbyport` for common port-to-service mappings.

3. **IP Range Support**:
   - Scans a single IP or a range of IPs using the `ipaddress` library.

4. **Logging**:
   - Logs errors, warnings, and results to a log file (`port_scanner.log`) for debugging and audit purposes.

5. **Results Export**:
   - Saves results (port, service, banner) to a CSV file for detailed documentation.

6. **Graphical User Interface (GUI)**:
   - A simple interface built using `tkinter` for inputting scan parameters and displaying results.

7. **Banner Grabbing**:
   - Attempts to fetch banners from open ports for additional insights about running services.

---

## Code Description

### Imports
- **`asyncio`**: Handles asynchronous I/O operations.
- **`socket`**: Provides low-level networking support.
- **`csv`**: Used to save scan results.
- **`ipaddress`**: Processes IP ranges for scanning.
- **`logging`**: Logs events, errors, and scan results.
- **`datetime`**: Tracks scan duration.
- **`tkinter`**: Creates the graphical user interface (GUI).

### Main Components

1. **`AsyncPortScanner` Class**:
   - Handles the core scanning logic.
   - **Methods**:
     - `scan_port(port)`: Scans a single port and fetches its banner.
     - `run_scan()`: Scans all ports in the specified range concurrently.
     - `save_results(filename)`: Saves scan results to a CSV file.
     - `print_results()`: Displays results in the console.

2. **`get_ip_range(start_ip, end_ip)` Function**:
   - Generates a list of IPs from the given start and end IPs.

3. **Graphical User Interface (GUI)**:
   - Built with `tkinter`.
   - Inputs:
     - Target IP or range.
     - Port range (e.g., `1-1000`).
     - Timeout (in seconds).
   - A "Start Scan" button triggers the scanning process.

---

## How to Execute

### Prerequisites
1. Install Python (>=3.8).
2. Install required libraries:
   ```bash
   pip install asyncio ipaddress
   ```

### Steps
1. Save the code to a file, e.g., `Port_Scanner.py`.
2. Run the script:
   ```bash
   python Port_Scanner.py
   ```
3. The GUI will open, allowing you to:
   - Enter the target IP or range (e.g., `192.168.1.1-192.168.1.10`).
   - Specify the port range (e.g., `1-65535`).
   - Set a timeout (default: 2 seconds).
4. Click "Start Scan" to initiate the scan.
5. Results will:
   - Be displayed in the terminal.
   - Be saved to a CSV file (e.g., `scan_results_<target>.csv`).
   - Include details on open ports, services, and banners.

---

## Example
### Input
- **Target**: `192.168.1.1`
- **Port Range**: `1-1000`
- **Timeout**: `2 seconds`

### Output
- Terminal:
  ```
  Open Ports:
  Port 22 (ssh): OpenSSH 8.2p1 Ubuntu
  Port 80 (http): Apache HTTP Server
  ```
- CSV File:
  ```csv
  Port,Service,Banner
  22,ssh,OpenSSH 8.2p1 Ubuntu
  80,http,Apache HTTP Server
  ```

---

## Log File (`port_scanner.log`)
Example log output:
```
2025-01-22 12:34:56 - INFO - Open port found: 22 (ssh) - OpenSSH 8.2p1 Ubuntu
2025-01-22 12:34:56 - WARNING - Failed to connect to port 23
2025-01-22 12:34:56 - INFO - Results saved to scan_results_192.168.1.1.csv
```

---


