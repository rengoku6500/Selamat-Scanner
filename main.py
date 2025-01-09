import subprocess
import sys
import os
from colorama import Fore, Back, Style, init
import shutil  # New import to check for executable presence

# Initialize colorama
init(autoreset=True)

# Function to check and install required Python packages
def check_and_install(package):
    """Check if a Python package is installed and install it if missing."""
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Function to check Waybackurls installation
def check_waybackurls():
    """Check if Waybackurls is installed."""
    if shutil.which("waybackurls") is None:
        print("waybackurls is not installed. Please install it manually.")
        print("Follow these steps to install Go and waybackurls:\n")
        print("1. Install Go from https://golang.org/dl/ and add it to your PATH.")
        print("2. Run: go install github.com/tomnomnom/waybackurls@latest")
        print("After installing, please rerun this script.")
        sys.exit(1)
    else:
        print("waybackurls is already installed.")

# Function to run individual script
def run_script(script_name, description):
    """Run a Python script with a description."""
    print("\n" + "-" * 50)
    print(f"Running {description} ({script_name})...")
    print("-" * 50)
    try:
        subprocess.run([sys.executable, script_name], check=True)
        print(f"\n{description} completed successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")
        sys.exit(1)

# Function to clear terminal screen
def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Main Menu
def main_menu():
    # Check requirements
    print("Checking requirements...")
    check_and_install("colorama")
    check_and_install("requests")
    check_waybackurls()
    print("All requirements are fulfilled.")

    # Clear the screen after requirements check
    clear_screen()

    # Main script execution menu with colored options
    while True:
        print("""
      ⠀⢻⣿⣿⣿⣦⠘⢶⣄⣀⡀⠘⣷⡐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠺⠥⢄⣀⠀⠀⠀⣀⣠⣤⣶⣾⣿⣿⣿⣟⣁⣀⣤
⠙⠿⣿⣿⣿⣛⠛⠳⢤⣈⣂⠈⠑⠞⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣍⡹⠶⢤⡀⠈⠙⡒⠆⠀⠀⠈⣉⠛⠛⢿⣿⣿⣿⣿⡿
⣶⣿⣿⡿⠟⠋⠁⠀⠐⠒⢬⣭⠵⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠔⠋⠁⠀⠀⠀⠘⢷⡀⠈⠳⠦⣄⠀⠽⣿⣿⣿⣿⡿⠟⠋⠀
⢿⣿⣿⣿⣿⣯⠄⠐⣺⣽⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⠀⠀⠀⠀⠀⠀⠀⠙⣄⠀⡄⠤⣵⣦⠀⠉⣙⠛⠒⠀⠀⠀
⠀⠈⣩⣿⣿⡵⢒⣽⢶⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠇⠀⠀⠀⠀⠀⣀⠔⠀⠘⢦⠘⡆⠈⠛⠷⡄⠹⣯⡓⠤⣀⠀
⣴⣾⣿⣿⣿⣿⠟⠡⡿⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣤⣶⣶⣶⡶⠞⠁⠀⠀⠀⠀⢣⡄⠀⠀⠀⡈⠂⠈⠻⣦⡀⠀
⠀⠀⠀⠀⣠⣧⠄⢀⡇⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⠿⠿⠛⠛⠉⠀⠀⠀⠀⢀⠄⠀⢸⠃⠀⠀⠀⠙⣦⣤⣤⣬⣽⡦
⠀⠀⠀⠈⠉⠀⣼⢨⣇⣀⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⣾⡿⠋⠁⣀⣤⣶⠶⠶⠶⠶⠶⡶⠊⠁⠀⠀⠸⠀⠀⡆⠀⠘⡎⢙⡋⡁⠰⣄
⠀⠀⠀⠀⠀⠀⣿⢸⡏⠻⠿⣿⣿⢿⣆⠀⠀⠀⠀⠀⡸⢋⣠⢃⣾⡿⠓⠒⠦⣄⠀⠀⢸⠃⠀⠀⠀⢠⠃⠀⢠⡇⠀⠀⡷⠋⠙⠢⡀⠈
⠀⠈⠀⠀⠀⠀⣿⠀⣿⣄⡴⠛⠿⣶⣿⣧⡀⠀⠀⠀⠁⣾⠃⡾⠛⣰⣿⣿⡆⡎⡆⢀⠎⠀⠀⢀⡴⠃⠀⠀⣾⡇⠀⠀⡇⡀⠀⠀⢹⠀
⠀⠀⠀⠀⠀⡴⠃⣠⣿⣿⡆⠠⣶⣦⠸⣿⣧⠀⠀⠀⠀⠀⠈⡇⠈⢮⡻⠛⠃⢁⡠⠋⠀⢀⡤⠊⠀⠀⢀⣼⣿⡇⠀⠀⡇⠉⣀⠀⢸⠀
⠀⠀⠠⠀⠈⠀⠰⡟⢸⣿⠱⡀⠻⠟⠀⢸⣿⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠉⠉⠡⠤⣤⡚⠁⠀⠀⠀⣠⠞⠁⡇⣼⠀⠀⢹⠀⠘⠀⣸⠀
⠄⠀⠀⠀⠀⠀⠀⠀⢻⣯⡆⠈⠉⠀⠀⡸⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⢉⠏⠀⣸⠃⣹⠀⠀⣏⠄⠀⠀⠅⠀
⠁⠀⠀⠀⠀⠀⠀⠀⢠⡏⡇⠀⠀⠀⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⣰⠋⠀⣿⠀⠀⡟⢆⢀⠞⠀⠀
⠀⠀⠀⠀⠀⣰⠒⣠⡞⠁⣿⠀⠀⠀⠀⢻⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠁⣰⠃⢀⠀⡏⠀⢸⢃⡼⢳⡀⠀⠀
⠸⠗⠀⠀⢘⣥⣾⣫⠔⡸⢻⣇⠀⠀⠀⠀⣈⠤⠀⠀⠀⠀⠀⠀⠀⠀⣰⠀⠀⠀⠀⠀⠀⢀⣼⢇⣾⠇⠀⣼⠀⡇⣄⣼⠀⠀⠘⣇⠀⠀
⠀⠀⠀⠠⠿⣿⣿⢋⠀⠃⡼⠙⣄⠀⠀⠀⢳⣤⣴⣶⣶⣶⣾⣿⣿⡿⠁⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⢀⢰⣿⡄⣧⣿⡿⠀⠀⠀⢻⠀⠀
⠀⠀⠀⢀⣴⣿⣷⡟⠀⣼⠁⡕⢹⣦⠀⠀⠀⠙⣟⠉⠉⠉⢉⡽⠋⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣵⣏⣸⣿⣿⡇⣿⣿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⢀⣾⣿⣿⣿⠁⣾⣿⡆⢃⣼⣌⠳⣄⠀⠀⠈⠑⠒⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡟⠁⠈⣿⣿⣿⣿⣿⣿⡟⢿⣿⣷⣄⠀⠀⠀
⠀⠀⢸⣿⠿⢻⣿⣰⣿⣿⣇⣾⣿⣿⡇⠈⢳⣄⠀⠀⠀⠈⠑⠀⠀⠀⠀⠀⣀⡤⠞⠉⢿⢀⠀⢀⣿⣿⡁⢸⣿⣿⠀⢀⢷⠀⠈⠀⠀⠀
⠴⠶⠿⠷⠄⢼⣿⡿⢿⣿⣿⣿⣿⢿⡇⣠⢸⡏⡱⢄⡀⠀⠀⢀⣀⣤⡶⠟⠉⠀⣀⣀⣠⠏⢀⡼⠋⢺⠁⢸⡟⢿⠀⠆⠈⣇⠀⠀⠀⠰
⡀⠀⠀⠀⡐⠸⡿⠗⠋⣿⣿⡿⠀⣿⣿⠇⢸⡏⣧⠤⠭⠿⠟⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⠀⡆⠁⠈⠱⣇⠀⠸⡆⠀⠀⠀
⠀⠀⠀⠀⠙⢦⣁⠀⣸⢟⣽⠁⣰⢻⡇⢠⠏⠀⣿⣤⠀⠀⠀⠀⠀⣤⡤⣤⣶⣶⣴⣶⣾⣿⣿⣿⣿⣇⣼⡇⠀⣸⢀⣿⡄⠀⣿⠀⠀⠀
⠀⠀⠀⠀⠐⣋⣭⣿⣿⣿⠏⣴⡇⢀⡇⣎⣠⠞⢻⣿⠄⠀⠀⠀⠀⠹⣶⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣿⣾⣿⣇⣰⢹⠀⡄⠀
⠀⠀⠀⣠⣿⡿⢿⣿⣿⣏⣼⣿⡇⢸⡷⠋⠀⢀⣤⣿⡄⠀⠀⠀⠀⣿⣏⣹⣿⢛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⠀⠙⠆

         """)
        print(Fore.YELLOW + "\n" + "-" * 50)
        print(Fore.CYAN + "    made by rengoku6500!")
        print("""[!] legal disclaimer: Usage of this script for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program
        """)
        print(Fore.YELLOW + "-" * 50)
        print(Fore.MAGENTA + "\nMain Menu:")
        print(Fore.CYAN + "1. Crawl Wayback URLs")
        print(Fore.CYAN + "2. Find XSS Vulnerabilities")
        print(Fore.CYAN + "3. Find SQL Injection Vulnerabilities")
        print(Fore.RED + "4. Exit")

        choice = input(Fore.GREEN + "Enter your choice (1-4): ").strip()

        if choice == "1":
            run_script("crawlUrl.py", "Crawl Wayback URLs")
        elif choice == "2":
            run_script("detectXss.py", "Find XSS Vulnerabilities")
        elif choice == "3":
            run_script("detectSqli.py", "Find SQL Injection Vulnerabilities")
        elif choice == "4":
            print(Fore.RED + "Exiting the program. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter a valid option (1-4).")

if __name__ == "__main__":
    main_menu()
