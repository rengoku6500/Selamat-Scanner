import subprocess
import os
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import Fore, Style, init
import re

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

def normalize_url_keys(url):
    """
    Normalize URL by keeping only the path and parameter keys.
    Ignores parameter values to compare URLs based on structure.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    normalized_query = sorted(query_params.keys())
    return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{'&'.join(normalized_query)}"

def deduplicate_urls(urls):
    """
    Deduplicate URLs based on normalized form (path + sorted query parameter keys).
    """
    seen = set()
    deduplicated = []
    for url in urls:
        normalized = normalize_url_keys(url)
        if normalized not in seen:
            seen.add(normalized)
            deduplicated.append(url)
    return deduplicated

def run_commands():
    """Run WaybackURLs extraction and process the results with deduplication."""
    print(Fore.CYAN + "Running Wayback URLs extraction and processing...")

    with open("results/domains.txt", "r") as file:
        domains = file.readlines()

    result = subprocess.run(["waybackurls"] + [domain.strip() for domain in domains],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    urls = result.stdout.decode().splitlines()

    # Deduplicate URLs
    unique_urls = deduplicate_urls(sorted(set(urls)))
    url_with_param = [url for url in unique_urls if '?' in url or '=' in url]

    create_results_directory()
    with open("results/urlWithParam.txt", "w") as file:
        for url in url_with_param:
            file.write(url + "\n")

    if os.path.exists("results/domains.txt"):
        os.remove("results/domains.txt")

    if os.path.exists("results/urlWithParam.txt"):
        print(Fore.GREEN + f"Total {len(url_with_param)} unique URLs with parameters found.")
    else:
        print(Fore.RED + "No output saved to results/urlWithParam.txt.")

def modify_url(url, word_to_add):
    """Modify the URL by appending 'RENGOKU<>' to each parameter's value."""
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

def scan_complex(url, word_to_check):
    """Check if the word is inside <script> tags in the HTML content, without worrying about filtering."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        # Look for the word inside <script> tags (even if filtered or not)
        script_content = re.findall(r'<script.*?>(.*?)</script>', response.text, re.DOTALL)
        
        for script in script_content:
            if word_to_check in script:
                return True

    except requests.RequestException as e:
        print(Fore.RED + f"Error requesting URL: {url}, {e}")

    return False

def main():
    """Main function to run the script."""
    clear_terminal()  # Clear terminal before starting
    reflected_urls_word = []
    reflected_urls_symbol = []
    reflected_urls_complex = []

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
        
        word_to_add = "RENGOKU<>"
        word_to_check_word = "RENGOKU"
        word_to_check_symbol = "RENGOKU<>"

        for idx, url in enumerate(urls, start=1):
            url = url.strip()
            modified_url = modify_url(url, word_to_add)

            # Show progress
            progress = (idx / total_urls) * 100
            print(Fore.BLUE + f"Processing URL {idx}/{total_urls} - Progress: {progress:.2f}%")

            if check_reflected_word(modified_url, word_to_check_word):
                reflected_urls_word.append(modified_url)
                print(Fore.GREEN + f"Reflected URL (word): {modified_url}")

            if check_reflected_word(modified_url, word_to_check_symbol):
                reflected_urls_symbol.append(modified_url)
                print(Fore.RED + f"Reflected URL (symbol): {modified_url}")

            if scan_complex(modified_url, word_to_check_word):
                reflected_urls_complex.append(modified_url)
                print(Fore.YELLOW + f"Reflected URL (complex): {modified_url}")

    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted by user!")
        save_partial_results(reflected_urls_word, reflected_urls_symbol, reflected_urls_complex)
        return

    # Save the reflected URLs
    if reflected_urls_word:
        create_results_directory()
        with open('results/wordReflected.txt', 'w') as outfile:
            for reflected_url in reflected_urls_word:
                clean_url = reflected_url.replace(word_to_add, '')
                outfile.write(clean_url + '\n')
        print(Fore.GREEN + "There are URLs with the word reflected. Check the 'results/wordReflected.txt' file.")

    if reflected_urls_symbol:
        create_results_directory()
        with open('results/symbolReflected.txt', 'w') as outfile:
            for reflected_url in reflected_urls_symbol:
                clean_url = reflected_url.replace(word_to_add, '')
                outfile.write(clean_url + '\n')
        print(Fore.RED + "There are URLs with the symbol reflected. Check the 'results/symbolReflected.txt' file.")

    if reflected_urls_complex:
        create_results_directory()
        with open('results/complexReflected.txt', 'w') as outfile:
            for reflected_url in reflected_urls_complex:
                clean_url = reflected_url.replace(word_to_add, '')
                outfile.write(clean_url + '\n')
        print(Fore.YELLOW + "There are URLs with complex reflected (inside <script>). Check the 'results/complexReflected.txt' file.")

    # Cleanup
    if os.path.exists('results/urlWithParam.txt'):
        os.remove('results/urlWithParam.txt')

    input(Fore.CYAN + "\nPress Enter to exit...")
    clear_terminal()  # Clear terminal after finishing

def save_partial_results(reflected_urls_word, reflected_urls_symbol, reflected_urls_complex):
    """Save partially analyzed results if interrupted."""
    save = input(Fore.YELLOW + "Do you want to save partially analyzed results? (yes/no): ").strip().lower()
    if save == 'yes' and (reflected_urls_word or reflected_urls_symbol or reflected_urls_complex):
        create_results_directory()
        with open('results/partial_wordReflected.txt', 'w') as file:
            for url in reflected_urls_word:
                file.write(url + '\n')
        with open('results/partial_symbolReflected.txt', 'w') as file:
            for url in reflected_urls_symbol:
                file.write(url + '\n')
        with open('results/partial_complexReflected.txt', 'w') as file:
            for url in reflected_urls_complex:
                file.write(url + '\n')
        print(Fore.GREEN + "Partial results saved.")
    else:
        print(Fore.YELLOW + "No results saved.")

if __name__ == "__main__":
    main()
