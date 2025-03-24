import subprocess
import os
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

HEADERS = {}

def set_custom_headers():
    """Prompt user for custom headers and store them in a global dictionary."""
    global HEADERS
    print(Fore.YELLOW + "\nEnter Cookie/A.bearer if (key:value), one per line. Press Enter to finish/Skip:")
    
    skipped = True  # Track if the user skips input
    
    while True:
        header = input().strip()
        if not header:  # Stop if input is empty (Enter key)
            break
        if ':' in header:
            key, value = header.split(':', 1)
            HEADERS[key.strip()] = value.strip()
            skipped = False  # User entered at least one header
        else:
            print(Fore.RED + "Invalid format. Use key:value")
    
    if skipped:
        print(Fore.YELLOW + "No cookies set. Skipping...")  # Message when user skips
    else:
        print(Fore.GREEN + "Cookies set! Nyum nyum.")  # Message when cookies are set



def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_domains():
    """Ask for domain names from the user."""
    domains = input("Enter domain names (comma-separated, e.g., domain1.com, domain2.com): ")
    domain_list = [domain.strip() for domain in domains.split(',')]
    return domain_list

def save_domains_to_file(domains):
    """Save the domain names to 'domains.txt'."""
    with open("domains.txt", "w") as file:
        for domain in domains:
            file.write(domain + "\n")
    print("Domains saved to domains.txt.")

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
    """Run Wayback URLs extraction and save output with query parameters."""
    print("Running Wayback URLs extraction and processing...")

    with open("domains.txt", "r") as file:
        domains = file.readlines()

    result = subprocess.run(["waybackurls"] + [domain.strip() for domain in domains], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    urls = result.stdout.decode().splitlines()

    # Deduplicate URLs
    unique_urls = deduplicate_urls(sorted(set(urls)))
    url_with_param = [url for url in unique_urls if '?' in url or '=' in url]

    # Ensure the 'results' directory exists
    if not os.path.exists("results"):
        os.makedirs("results")

    with open("results/urlWithParam.txt", "w") as file:
        for url in url_with_param:
            file.write(url + "\n")

    if os.path.exists("domains.txt"):
        os.remove("domains.txt")

    if os.path.exists("results/urlWithParam.txt"):
        print("URLs with query parameters found and saved.")
    else:
        print("No output saved to urlWithParam.txt.")

    print("Commands executed and temporary files cleaned up.")

def analyze_urls(urls):
    """Analyze URLs for SQL Injection patterns."""
    pattern_a_urls = []
    pattern_b_urls = []

    try:
        if not HEADERS:
            HEADERS['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'

        for url in urls:
            url = url.strip()
            if not url:
                continue

            print(Fore.CYAN + "-" * 100)
            print(Fore.GREEN + f"\nAnalyzing URL: {url}")

            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)

            for param in params:
                print(Fore.GREEN + f"\nAnalyzing parameter: {param}")
                content_lengths = []

                for variation in range(3):
                    modified_params = params.copy()
                    if variation == 0:
                        description = "Normal request"
                    elif variation == 1:
                        modified_params[param] = [value + "'" for value in params[param]]
                        description = "Single apostrophe"
                    elif variation == 2:
                        modified_params[param] = [value + '"' for value in params[param]]
                        description = "Double apostrophe"

                    modified_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(modified_params, doseq=True)}"

                    try:
                        response = requests.get(modified_url, headers=HEADERS)
                        content_length = len(response.content)
                        content_lengths.append(content_length)
                    except Exception as e:
                        print(Fore.RED + f"{description}: Error = {e}")
                        content_lengths.append(None)

                if all(content_lengths):
                    first, second, third = content_lengths
                    if first != second and second == third:
                        print(Fore.YELLOW + "\nPattern Detected [B]: ≤ 5% chance SQLI.")
                        pattern_a_urls.append(url)
                    elif first == third and first != second:
                        print(Fore.RED + "\nPattern Detected [A]: 80% chance SQLI.")
                        pattern_b_urls.append(url)
                    else:
                        print(Fore.GREEN + "\nNot Vulnerable: No matching pattern found.")
                else:
                    print(Fore.YELLOW + "\nNot Vulnerable: Incomplete responses.")
    
    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted!")
    
    return pattern_a_urls, pattern_b_urls

def save_partial_results(pattern_a_urls, pattern_b_urls):
    """Save partially analyzed results."""
    if pattern_a_urls:
        with open("results/partial_pattern_b_sqli.txt", "w") as file:
            file.write("\n".join(pattern_a_urls))
    if pattern_b_urls:
        with open("results/partial_pattern_a_sqli.txt", "w") as file:
            file.write("\n".join(pattern_b_urls))

def main():
    """Main function to orchestrate the script."""
    clear_terminal()  # Clear terminal before starting
    set_custom_headers()
    
    try:
        # Ask user if they want to use a custom file
        use_custom_file = input(Fore.YELLOW + "Do you want to use a custom file for URLs? (yes/no): ").strip().lower()
        
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

        # Deduplicate URLs before analyzing them
        unique_urls = deduplicate_urls(urls)
        pattern_a_urls, pattern_b_urls = analyze_urls(unique_urls)

        save_to_file = input("\nDo you want to save the results? (yes/no): ").strip().lower()
        if save_to_file == 'yes':
            with open("results/pattern_b_sqli.txt", 'w') as file:
                file.write("\n".join(pattern_a_urls))
            with open("results/pattern_a_sqli.txt", 'w') as file:
                file.write("\n".join(pattern_b_urls))
            print(Fore.GREEN + "Results saved successfully.")
        
        if os.path.exists("results/urlWithParam.txt"):
            os.remove("results/urlWithParam.txt")

        input("\nPress Enter to exit...")
        clear_terminal()  # Clear terminal after finishing

    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted!")
        save = input("Do you want to save partially analyzed results? (yes/no): ").strip().lower()
        if save == 'yes':
            save_partial_results([], [])
            print(Fore.GREEN + "Partially analyzed results saved.")
        else:
            print(Fore.YELLOW + "No results saved.")
        clear_terminal()

if __name__ == "__main__":
    main()
