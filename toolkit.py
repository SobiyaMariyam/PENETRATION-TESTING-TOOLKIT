from port_scanner import AsyncPortScanner  # Import the asynchronous port scanner module
from brute_forcer import SSHBruteForcer  # Import the SSH brute-forcing module
import asyncio  # Import asyncio for asynchronous programming

# Function to display the main menu and get user input
def main_menu():
    """
    Displays the main menu and prompts the user for a choice.
    Returns:
        str: The user's menu choice.
    """
    print("\nPenetration Testing Toolkit")  # Title of the toolkit
    print("1. Port Scanner")  # Option to use the port scanner module
    print("2. SSH Brute-Forcer")  # Option to use the SSH brute-forcer module
    print("3. Exit")  # Option to exit the program
    return input("\nChoose an option: ").strip()  # Return the user's choice

# Main entry point of the program
if __name__ == "__main__":
    # Infinite loop to keep the menu running until the user chooses to exit
    while True:
        # Show the main menu and get the user's choice
        choice = main_menu()

        # Handle Port Scanner option
        if choice == "1":
            # Prompt the user for target details
            target = input("Enter target IP/hostname: ").strip()  # Target IP or hostname
            port_range = input("Enter port range (e.g., 1-1000): ").strip()  # Port range to scan
            start_port, end_port = map(int, port_range.split('-'))  # Parse the port range into integers
            timeout = float(input("Enter timeout (default 2): ") or 2)  # Timeout for scanning (default is 2 seconds)

            # Create an instance of the port scanner with the given parameters
            scanner = AsyncPortScanner(target, port_range=(start_port, end_port), timeout=timeout)
            
            # Run the scan asynchronously
            asyncio.run(scanner.run_scan())
            
            # Print and save the scan results
            scanner.print_results()
            scanner.save_results()

        # Handle SSH Brute-Forcer option
        elif choice == "2":
            # Prompt the user for SSH brute-forcing details
            target = input("Enter target IP/hostname: ").strip()  # Target IP or hostname for SSH
            username = input("Enter username for SSH: ").strip()  # Username for SSH login
            password_file = input("Enter path to password list: ").strip()  # Path to the password list file
            
            # Read the password list from the specified file
            with open(password_file, 'r') as f:
                passwords = f.readlines()  # Read all passwords into a list
            
            # Create an instance of the SSH brute-forcer with the given parameters
            brute_forcer = SSHBruteForcer(target, username, passwords)
            
            # Run the brute-forcing process asynchronously
            asyncio.run(brute_forcer.run_bruteforce())

        # Handle Exit option
        elif choice == "3":
            print("Exiting toolkit.")  # Print exit message
            break  # Break the loop to exit the program

        # Handle invalid choices
        else:
            print("Invalid choice. Please try again.")  # Prompt the user to enter a valid option
