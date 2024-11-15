import requests
import csv

def get_divar_urls(query, city_id="1", page_limit=3, initial_last_post_date=None):
    """
    Retrieves URLs from the Divar Cloudflare Worker API based on a query and city.
    
    Parameters:
        query (str): The search term (e.g., "207").
        city_id (str): The city ID to search within. Defaults to "1".
        page_limit (int): Number of pages to retrieve per request. Maximum is 50.
        initial_last_post_date (str): The starting timestamp for pagination, if continuing from a previous request.
        
    Returns:
        list: A list of URLs retrieved from the API.
    
    *Read more about this api: https://github.com/2077DevWave/divar-search-page-crawler
    """
    
    BASE_URL = "https://divar-search-page-extractor.sideco.ir/"
    urls = []
    last_post_date = initial_last_post_date

    try:
        for page in range(0,int(page_limit/50) + min(1,page_limit%50)):
            # Set up parameters for each API request
            params = {
                "city_id": city_id,
                "query": query,
                "page": min(50,page_limit - 50*page),  # Maximum pages per request
            }
            if last_post_date:
                params["lastPostDate"] = last_post_date
            
            # Send request to API
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raise an error if the request fails
            
            # Parse the response JSON
            data = response.json()
            if "urls" in data:
                urls.extend(data["urls"])
                print(f"Page {page}: Retrieved {len(data['urls'])} URLs")
            else:
                print(f"Page {page}: No URLs found.")
                break
            
            # Get the lastPostDate for the next request
            last_post_date = data.get("lastPostDate")
            if not last_post_date:
                print("No further results available.")
                break

        return urls

    except requests.exceptions.RequestException as e:
        print("Error connecting to the Divar API:", e)
        return []

def fetch_product_details(tag):
    """
    Fetches detailed information about a product from the Divar Product Details Fetch API.
    
    Parameters:
        tag (str): The unique product tag extracted from the Divar URL.
        
    Returns:
        dict: The product details in JSON format.

    *Read more about this api: https://github.com/2077DevWave/divar-page-info-creawler
    """
    
    PRODUCT_API = f"https://divar-page-info.sideco.ir/?tag={tag}"
    
    try:
        response = requests.get(PRODUCT_API)
        response.raise_for_status()  # Raise an error if the request fails
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product details for tag {tag}: {e}")
        return None

def extract_tag_from_url(url):
    """
    Extracts the tag from a Divar product URL.
    
    Parameters:
        url (str): The full Divar product page URL.
        
    Returns:
        str: The extracted page tag.
    """
    
    # Extract the tag from the last part of the URL (after the last '/')
    return url.split('/')[-1]

def save_to_csv(data, filename="divar_product_details.csv"):
    """
    Saves the product details to a CSV file with dynamic headers.
    
    Parameters:
        data (list): The list of product details to save.
        filename (str): The name of the CSV file to save the data.
    """
    
    # Collect all unique titles across all products
    unique_titles = set()
    for product in data:
        for item in product:
            unique_titles.add(item.get("title", ""))
    
    # Convert to a sorted list of titles for consistent ordering
    unique_titles = sorted(list(unique_titles))
    
    # Open the CSV file in write mode
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header (titles of the fields)
        writer.writerow(unique_titles)
        
        # Write the details for each product
        for product in data:
            row = []
            # For each title in the header, get the corresponding value for the product, or null if not present
            for title in unique_titles:
                value = None
                for item in product:
                    if item.get("title") == title:
                        value = item.get("value")
                        break
                row.append(value if value is not None else "null")
            writer.writerow(row)

def main():
    # Step 1: Fetch URLs based on the search query and city
    page_limit = int(url_limit/20) + min(1,url_limit%20)   # Adjust this to control the number of pages to retrieve (each page contain 20 to 30 url)
    urls = get_divar_urls(query=search_query, city_id=city_id, page_limit=page_limit)
    urls = urls[0:min(len(urls),url_limit)-1]
    
    print("\nTotal URLs Retrieved:", len(urls))
    
    all_product_details = []
    
    # Step 2: For each URL, extract the product tag and fetch the product details
    for url in urls:
        tag = extract_tag_from_url(url)
        print(f"\nFetching details for product with tag: {tag}")
        
        product_details = fetch_product_details(tag)
        if product_details:
            all_product_details.append(product_details)
            print(f"Details for {url} fetched successfully.")
        else:
            print(f"Failed to fetch details for {url}.")
    
    # Step 3: Save the collected details to a CSV file
    save_to_csv(all_product_details,filename=csv_file)
    print(f"\nProduct details saved to 'divar_product_details.csv'.")


# Example Usage
if __name__ == "__main__":
    global search_query,city_id,url_limit,csv_file
    ################################## Set this parameters only ###############################################
    search_query = "207"                    # Change this query as needed
    city_id = "38"                          # Optional: Specify a different city ID if desired (38=yasouj , 1=tehran)
    url_limit = 5                           # how many url you want to crawel
    csv_file = "divar_product_details.csv"  # where to save product information
    ###########################################################################################################

    main() # run the application
