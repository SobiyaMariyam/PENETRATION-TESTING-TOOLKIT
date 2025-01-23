import asyncio  # Asynchronous programming library
import socket  # Low-level networking interface
import csv  # Library for handling CSV files
import ipaddress  # Library for IP address manipulation
import logging  # Library for logging events
from datetime import datetime  # Library for handling dates and times
import tkinter as tk  # Library for GUI development
from tkinter import ttk, messagebox  # Additional GUI widgets and dialog boxes

# Configure logging to record scan activities and errors
logging.basicConfig(
    filename="port_scanner.log",  # Log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO  # Log level
)

class AsyncPortScanner:
    """
    A class to perform asynchronous port scanning.
    """
    def __init__(self, target, port_range=(1, 65535), timeout=2):
        """
        Initializes the port scanner with target details.

        Args:
            target (str): Target IP or hostname.
            port_range (tuple): Range of ports to scan (default 1-65535).
            timeout (float): Timeout for each connection attempt (default 2 seconds).
        """
        self.target = target
        self.port_range = port_range
        self.timeout = timeout
        self.open_ports = []  # List to store information about open ports

    async def scan_port(self, port):
        """
        Scans a single port asynchronously.

        Args:
            port (int): The port number to scan.
        """
        try:
            # Attempt to establish a connection to the port
            reader, writer = await asyncio.open_connection(self.target, port)

            # Try to retrieve the banner from the service
            try:
                banner = await asyncio.wait_for(reader.read(1024), timeout=self.timeout)
                banner = banner.decode('utf-8').strip()
            except asyncio.TimeoutError:
                banner = "No banner"  # Default message if no banner is retrieved
            
            # Determine the service name if the port is a well-known port
            service = socket.getservbyport(port, "tcp") if port < 1024 else "Unknown"
            
            # Save the open port details
            self.open_ports.append((port, service, banner))
            logging.info(f"Open port found: {port} ({service}) - {banner}")
            
            # Close the connection
            writer.close()
            await writer.wait_closed()
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            logging.warning(f"Failed to connect to port {port}")

    async def run_scan(self):
        """
        Scans the specified range of ports asynchronously.
        """
        print(f"Scanning target: {self.target}")
        # Create tasks for each port in the range
        tasks = [
            self.scan_port(port)
            for port in range(self.port_range[0], self.port_range[1] + 1)
        ]
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
        # Sort the open ports by port number
        self.open_ports.sort(key=lambda x: x[0])

    def save_results(self, filename="scan_results.csv"):
        """
        Saves scan results to a CSV file.

        Args:
            filename (str): Name of the file to save results (default "scan_results.csv").
        """
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow(["Port", "Service", "Banner"])
            # Write port details
            writer.writerows(self.open_ports)
        print(f"Results saved to {filename}")
        logging.info(f"Results saved to {filename}")

    def print_results(self):
        """
        Displays the scan results in the console.
        """
        print("\nOpen Ports:")
        for port, service, banner in self.open_ports:
            print(f"Port {port} ({service}): {banner}")

def get_ip_range(start_ip, end_ip):
    """
    Generates a list of IP addresses in the specified range.

    Args:
        start_ip (str): Starting IP address.
        end_ip (str): Ending IP address.

    Returns:
        list: List of IP addresses in the range.
    """
    try:
        # Parse and validate the IP range
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        # Generate and return the IP addresses
        return [str(ip) for ip in ipaddress.summarize_address_range(start, end)]
    except ipaddress.AddressValueError as e:
        print(f"Invalid IP address: {e}")
        return []

# GUI
def start_scan():
    """
    Starts the scan based on user input from the GUI.
    """
    # Get input from the user
    ip_range = target_entry.get().strip()
    port_range = port_entry.get().strip()
    timeout = float(timeout_entry.get() or 2)

    try:
        # Parse the port range
        start_port, end_port = map(int, port_range.split('-'))
        
        # Determine whether to scan a range of IPs or a single IP
        if '-' in ip_range:
            start_ip, end_ip = ip_range.split('-')
            targets = get_ip_range(start_ip.strip(), end_ip.strip())
        else:
            targets = [ip_range]

        print(f"Targets to scan: {targets}")
        # Scan each target
        for target in targets:
            scanner = AsyncPortScanner(target, port_range=(start_port, end_port), timeout=timeout)
            asyncio.run(scanner.run_scan())
            scanner.print_results()
            scanner.save_results(filename=f"scan_results_{target}.csv")
        
        # Notify user of completion
        messagebox.showinfo("Scan Complete", "Scan finished successfully. Check the CSV file.")
    except Exception as e:
        logging.error(f"Error during scanning: {e}")
        messagebox.showerror("Error", str(e))

# Create the GUI window
root = tk.Tk()
root.title("Async Port Scanner")

# Target input
tk.Label(root, text="Target IP/Hostname (or IP range):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
target_entry = tk.Entry(root)
target_entry.grid(row=0, column=1, padx=10, pady=5)

# Port range input
tk.Label(root, text="Port Range (e.g., 1-1000):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=10, pady=5)

# Timeout input
tk.Label(root, text="Timeout (seconds):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
timeout_entry = tk.Entry(root)
timeout_entry.grid(row=2, column=1, padx=10, pady=5)

# Start button
start_button = tk.Button(root, text="Start Scan", command=start_scan)
start_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
