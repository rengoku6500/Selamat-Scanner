import subprocess
import os
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_domains():
    """Ask for domain names from the user."""
    domains = input(Fore.YELLOW + "Enter domain names (comma-separated, e.g., domain1.com, domain2.com): ")
    domain_list = [domain.strip() for domain in domains.split(',')]
    return domain_list

def create_results_directory():
    """Create the 'results' directory if it doesn't exist."""
    if not os.path.exists('results'):
        os.makedirs('results')

def save_domains_to_file(domains):
    """Save domains to a file in the 'results' directory."""
    create_results_directory()
    with open("results/domains.txt", "w") as file:
        for domain in domains:
            file.write(domain + "\n")
    print(Fore.GREEN + "Domains saved to results/domains.txt.")

def run_commands():
    """Run WaybackURLs extraction and process the results."""
    print(Fore.CYAN + "Running Wayback URLs extraction and processing...")

    with open("results/domains.txt", "r") as file:
        domains = file.readlines()

    result = subprocess.run(["waybackurls"] + [domain.strip() for domain in domains],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    urls = result.stdout.decode().splitlines()

    unique_urls = sorted(set(urls))
    url_with_param = [url for url in unique_urls if '?' in url or '=' in url]

    create_results_directory()
    with open("results/urlWithParam.txt", "w") as file:
        for url in url_with_param:
            file.write(url + "\n")

    if os.path.exists("results/domains.txt"):
        os.remove("results/domains.txt")

    if os.path.exists("results/urlWithParam.txt"):
        print(Fore.GREEN + f"Total {len(url_with_param)} URLs with parameters found.")
    else:
        print(Fore.RED + "No output saved to results/urlWithParam.txt.")

def modify_url(url, word_to_add):
    """Modify the URL by appending 'RENGOKU' to each parameter's value."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    for key in query_params:
        query_params[key] = [value + word_to_add for value in query_params[key]]
    
    modified_query = urlencode(query_params, doseq=True)
    modified_url = parsed_url._replace(query=modified_query)
    return urlunparse(modified_url)

def check_reflected_word(url, word_to_check):
    """Send the GET request and check if the word is reflected in the response."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if word_to_check in response.text:
            return True
    except requests.RequestException as e:
        print(Fore.RED + f"Error requesting URL: {url}, {e}")
    return False

def main():
    """Main function to run the script."""
    clear_terminal()  # Clear terminal before starting
    reflected_urls = []

    try:
        # Ask user if they want to use a custom file
        use_custom_file = input(Fore.YELLOW + "Do you want to use your own custom file for URLs? (yes/no): ").strip().lower()
        
        if use_custom_file == 'yes':
            # If yes, prompt for the custom file
            custom_file = input(Fore.YELLOW + "Enter the path to your custom file: ").strip()
            if os.path.exists(custom_file):
                with open(custom_file, 'r') as file:
                    urls = file.readlines()
            else:
                print(Fore.RED + "File does not exist.")
                return
        else:
            # Otherwise, proceed with the domain names
            domains = get_domains()
            save_domains_to_file(domains)
            run_commands()

            with open('results/urlWithParam.txt', 'r') as infile:
                urls = infile.readlines()

        total_urls = len(urls)
        print(Fore.YELLOW + f"Total URLs with parameters to process: {total_urls}")
        
        word_to_add = "RENGOKU"
        word_to_check = "RENGOKU"

        for idx, url in enumerate(urls, start=1):
            url = url.strip()
            modified_url = modify_url(url, word_to_add)

            # Show progress
            progress = (idx / total_urls) * 100
            print(Fore.BLUE + f"Processing URL {idx}/{total_urls} - Progress: {progress:.2f}%")

            if check_reflected_word(modified_url, word_to_check):
                reflected_urls.append(modified_url)
                print(Fore.GREEN + f"Reflected URL: {modified_url}")

    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted by user!")
        save_partial_results(reflected_urls)
        return

    # Save the reflected URLs
    if reflected_urls:
        create_results_directory()
        with open('results/reflectedUrl.txt', 'w') as outfile:
            for reflected_url in reflected_urls:
                clean_url = reflected_url.replace(word_to_add, '')
                outfile.write(clean_url + '\n')
        print(Fore.GREEN + "There are URLs reflected. Check the 'results/reflectedUrl.txt' file.")
    else:
        print(Fore.RED + "No URLs were reflected.")

    # Cleanup
    if os.path.exists('results/urlWithParam.txt'):
        os.remove('results/urlWithParam.txt')

    input(Fore.CYAN + "\nPress Enter to exit...")
    clear_terminal()  # Clear terminal after finishing

def save_partial_results(reflected_urls):
    """Save partially analyzed results if interrupted."""
    save = input(Fore.YELLOW + "Do you want to save partially analyzed results? (yes/no): ").strip().lower()
    if save == 'yes' and reflected_urls:
        create_results_directory()
        with open('results/partial_reflectedUrl.txt', 'w') as file:
            for url in reflected_urls:
                file.write(url + '\n')
        print(Fore.GREEN + "Partial results saved to 'results/partial_reflectedUrl.txt'.")
    else:
        print(Fore.YELLOW + "No results saved.")

if __name__ == "__main__":
    main()
