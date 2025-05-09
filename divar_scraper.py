import requests
import csv
import os

def get_divar_urls(query, city_id="1", page_limit=3, initial_last_post_date=None):
    BASE_URL = "https://divar-search-page-extractor.sideco.ir/"
    urls = []
    last_post_date = initial_last_post_date

    try:
        for page in range(0, (page_limit//50) + min(1, page_limit % 50)):
            params = {
                "city_id": city_id,
                "query": query,
                "page": min(50, page_limit - 50 * page),
            }
            if last_post_date:
                params["lastPostDate"] = last_post_date

            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()
            if "urls" in data:
                urls.extend(data["urls"])
                if not silent_mode : print(f"Page {page}: Retrieved {len(data['urls'])} URLs")
            else:
                print(f"Page {page}: No URLs found.")
                break

            last_post_date = data.get("last_post_date")
            if not last_post_date:
                print("No further results available.")
                break
            if silent_mode : print(f"\rPage url Retrieved: {page+1}/{(page_limit//50) + min(1, page_limit % 50)} of pages with {len(urls)} urls...",end="")
            
        return urls

    except requests.exceptions.RequestException as e:
        print("Error connecting to the Divar API:", e)
        return []

def fetch_product_details(tag):
    PRODUCT_API = f"https://divar-page-info.sideco.ir/?tag={tag}"
    try:
        response = requests.get(PRODUCT_API)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product details for tag {tag}: {e}")
        return None

def extract_tag_from_url(url):
    return url.split('/')[-1]

def save_to_csv(data, filename, unique_titles, write_header=False):
    mode = 'w' if write_header else 'a'
    with open(filename, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(unique_titles)
        for product in data:
            row = []
            for title in unique_titles:
                value = next((item.get("value") for item in product if item.get("title") == title), "null")
                row.append(value)
            writer.writerow(row)

def main():
    url_limit += ((url_limit*2)/100)  # add 2% fault page
    page_limit = int(url_limit / 20) + min(1, url_limit % 20)
    urls = get_divar_urls(query=search_query, city_id=city_id, page_limit=page_limit)
    urls = urls[0:min(len(urls), url_limit)]

    print("\nTotal URLs Retrieved:", len(urls))

    all_titles = set()
    buffer = []
    counter = 0
    write_header = True

    if os.path.exists(csv_file):
        os.remove(csv_file)

    for url in urls:
        tag = extract_tag_from_url(url)
        if not silent_mode : print(f"\nFetching details for tag: {tag}")
        product = fetch_product_details(tag)
        if product:
            buffer.append(product)
            for item in product:
                all_titles.add(item.get("title", ""))
            if not silent_mode :
              print(f"Details for {tag} fetched.")
        else:
            print(f"Failed for {tag}.")

        counter += 1
        if silent_mode : print(f"\rfetched {counter}/{len(urls)} and saved {counter - (counter%save_partition_size)}/{len(urls)} of urls...", end="")

        if counter % save_partition_size == 0 or counter == len(urls):
            sorted_titles = sorted(all_titles)
            save_to_csv(buffer, csv_file, sorted_titles, write_header=write_header)
            buffer = []
            write_header = False
            if not silent_mode:
              print(f"Saved {counter} items to {csv_file}.")
              

# Example Usage
if __name__ == "__main__":
    global search_query,city_id,url_limit,csv_file,silent_mode,save_partition_size
    ################################## Set this parameters only ###############################################
    search_query = "207"                    # Change this query as needed
    city_id = "1"                           # Optional: Specify a different city ID if desired (38=yasouj , 1=tehran)
    url_limit = 85000                       # how many url you want to crawel
    csv_file = "divar_product_details.csv"  # where to save product information
    save_partition_size = 1000
    silent_mode = True
    ###########################################################################################################

    main()