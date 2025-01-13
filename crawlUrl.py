import subprocess
import os
from urllib.parse import urlparse, parse_qs, urlencode

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_domains():
    """Ask for domain names from the user."""
    domains = input("Enter domain names (comma-separated, e.g., domain1.com, domain2.com): ")
    domain_list = [domain.strip() for domain in domains.split(',')]
    return domain_list

def save_domains_to_file(domains):
    """Save domains to a file."""
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

def run_commands():
    """Run WaybackURLs extraction and process the results."""
    print("Running Wayback URLs extraction...")

    with open("domains.txt", "r") as file:
        domains = file.readlines()

    result = subprocess.run(["waybackurls"] + [domain.strip() for domain in domains],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    urls = result.stdout.decode().splitlines()

    unique_urls = sorted(set(urls))
    url_with_param = [url for url in unique_urls if '?' in url or '=' in url]

    # Deduplicate URLs based on normalized keys
    seen = set()
    filtered_urls = []
    for url in url_with_param:
        normalized = normalize_url_keys(url)
        if normalized not in seen:
            seen.add(normalized)
            filtered_urls.append(url)

    # Ensure the 'results' directory exists
    if not os.path.exists("results"):
        os.makedirs("results")

    with open("results/url.txt", "w") as file:
        for url in filtered_urls:
            file.write(url + "\n")

    if os.path.exists("domains.txt"):
        os.remove("domains.txt")

    if os.path.exists("results/url.txt"):
        print("Check results/url.txt for results.")
    else:
        print("No output saved to url.txt.")

    print("Commands executed and temporary files cleaned up.")

def save_partial_results():
    """Save partially processed results if interrupted."""
    save = input("Process interrupted. Do you want to save partially analyzed results? (yes/no): ").strip().lower()
    if save == 'yes':
        # Ensure the 'results' directory exists
        if not os.path.exists("results"):
            os.makedirs("results")
        
        with open("results/partial_urls.txt", "w") as file:
            file.write("Partial results due to interruption.")
        print("Partial results saved to 'results/partial_urls.txt'.")
    else:
        print("Partial results not saved.")

def main():
    """Main function to run the script."""
    clear_terminal()  # Clear terminal before starting

    try:
        # Step 1: Get the domain names from user input
        domains = get_domains()

        # Step 2: Save domains to domains.txt file
        save_domains_to_file(domains)

        # Step 3: Run the commands
        run_commands()

    except KeyboardInterrupt:
        print("\nProcess interrupted by user!")
        save_partial_results()

    input("\nPress Enter to exit...")
    clear_terminal()  # Clear terminal after finishing

if __name__ == "__main__":
    main()
