import asyncio
import socket
import csv
import ipaddress
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Logging configuration
logging.basicConfig(
    filename="port_scanner.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

class AsyncPortScanner:
    def __init__(self, target, port_range=(1, 65535), timeout=2):
        self.target = target
        self.port_range = port_range
        self.timeout = timeout
        self.open_ports = []

    async def scan_port(self, port):
        """
        Scans a single port asynchronously.
        """
        try:
            reader, writer = await asyncio.open_connection(self.target, port)
            try:
                banner = await asyncio.wait_for(reader.read(1024), timeout=self.timeout)
                banner = banner.decode('utf-8').strip()
            except asyncio.TimeoutError:
                banner = "No banner"
            
            service = socket.getservbyport(port, "tcp") if port < 1024 else "Unknown"
            self.open_ports.append((port, service, banner))
            logging.info(f"Open port found: {port} ({service}) - {banner}")
            writer.close()
            await writer.wait_closed()
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            logging.warning(f"Failed to connect to port {port}")

    async def run_scan(self):
        """
        Scans the specified range of ports.
        """
        print(f"Scanning target: {self.target}")
        tasks = [
            self.scan_port(port)
            for port in range(self.port_range[0], self.port_range[1] + 1)
        ]
        await asyncio.gather(*tasks)
        self.open_ports.sort(key=lambda x: x[0])

    def save_results(self, filename="scan_results.csv"):
        """
        Saves scan results to a CSV file.
        """
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Port", "Service", "Banner"])
            writer.writerows(self.open_ports)
        print(f"Results saved to {filename}")
        logging.info(f"Results saved to {filename}")

    def print_results(self):
        """
        Displays scan results in the console.
        """
        print("\nOpen Ports:")
        for port, service, banner in self.open_ports:
            print(f"Port {port} ({service}): {banner}")

def get_ip_range(start_ip, end_ip):
    """
    Generates a list of IPs in the given range.
    """
    try:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        return [str(ip) for ip in ipaddress.summarize_address_range(start, end)]
    except ipaddress.AddressValueError as e:
        print(f"Invalid IP address: {e}")
        return []

# GUI
def start_scan():
    ip_range = target_entry.get().strip()
    port_range = port_entry.get().strip()
    timeout = float(timeout_entry.get() or 2)

    try:
        start_port, end_port = map(int, port_range.split('-'))
        if '-' in ip_range:
            start_ip, end_ip = ip_range.split('-')
            targets = get_ip_range(start_ip.strip(), end_ip.strip())
        else:
            targets = [ip_range]

        print(f"Targets to scan: {targets}")
        for target in targets:
            scanner = AsyncPortScanner(target, port_range=(start_port, end_port), timeout=timeout)
            asyncio.run(scanner.run_scan())
            scanner.print_results()
            scanner.save_results(filename=f"scan_results_{target}.csv")
        
        messagebox.showinfo("Scan Complete", "Scan finished successfully. Check the CSV file.")
    except Exception as e:
        logging.error(f"Error during scanning: {e}")
        messagebox.showerror("Error", str(e))

# Create GUI window
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
