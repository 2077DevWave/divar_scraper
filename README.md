# Divar Product Scraper

This Python script allows users to crawl and retrieve product listings from Divar, a popular Iranian marketplace website. The script fetches product details from Divar's Cloudflare Worker API, extracts key information from each product listing, and saves the data in a CSV file. The CSV file has dynamic headers, where each unique product title becomes a header column.

## Features

- **Crawl Divar Product Listings**: Retrieve product URLs based on search queries and city.
- **Fetch Detailed Product Information**: Extract detailed data (e.g., title, value) for each product.
- **Dynamic CSV Export**: Save the data into a CSV file with dynamic headers based on unique product titles.
- **Pagination Support**: Supports pagination to retrieve multiple pages of results.

## Requirements

- Python 3.x
- `requests` library (You can install it using `pip install requests`)

## How It Works

1. **Fetching URLs**: The script fetches product URLs based on a search query and city using Divar's search API.
2. **Fetching Product Details**: For each URL, the product's unique tag is extracted and used to fetch detailed product information using Divar's product details API.
3. **Saving Data**: The product details are saved in a CSV file, with dynamic headers corresponding to unique product titles. If a title is missing for a product, `null` is placed in the CSV file.

## How to Use

### Step 1: Set Parameters

Set the following parameters in the script to customize the behavior:

- **`search_query`**: The search term for products (e.g., `"207"` to find Peugeot 207 cars).
- **`city_id`**: The city ID to search within (e.g., `"1"` for Tehran, `"38"` for Yasouj).
- **`url_limit`**: The number of URLs to crawl. Each page can contain 20 to 30 URLs, depending on the results.
- **`csv_file`**: The name of the CSV file where the product details will be saved.

Example:
```python
search_query = "207"                    # Change this query as needed
city_id = "38"                          # Optional: Specify a different city ID if desired (38 = Yasouj, 1 = Tehran)
url_limit = 5                           # Set the number of URLs to crawl
csv_file = "divar_product_details.csv"  # Name of the CSV file to save the product information
```

### Step 2: Run the Script

Once the parameters are set, run the script:

```bash
python divar_scraper.py
```

This will start the crawling process, fetch product details, and save them into the specified CSV file.

## Example

For example, if you want to search for "Peugeot 207" in the city of Yasouj (`city_id = "38"`) and limit the crawl to 5 URLs, set the parameters like this:

```python
search_query = "207"    # Searching for Peugeot 207 cars
city_id = "38"          # Yasouj city ID
url_limit = 5           # Crawl 5 product URLs
csv_file = "divar_207.csv"  # Save results to divar_207.csv
```

### Output

After running the script, the details of the crawled products will be saved in a CSV file, for example `divar_product_details.csv`. The CSV file will contain dynamic headers for each unique title (e.g., "کارکرد", "مدل (سال تولید)", "رنگ"), and the corresponding product values for each product.

Example CSV format:

```csv
کارکرد, مدل (سال تولید), رنگ, برند و تیپ
1, 1403, مشکی, پژو 207i اتوماتیک
2, 1402, سفید, پژو 207 اتوماتیک
null, 1401, نقره‌ای, پژو 206
```

- If a product does not have a particular title (e.g., "کارکرد"), `null` will be placed in its place.

## API Documentation

1. **Divar Search API (URL Fetch)**  
   - Endpoint: `https://divar-search-page-extractor.sideco.ir/`
   - Returns a list of product URLs based on the search query, city ID, and pagination.

   **Parameters:**
   - `query`: The search term (e.g., "207").
   - `city_id`: The city ID (e.g., `"1"` for Tehran).
   - `page`: The page number to fetch.
   - `lastPostDate`: The timestamp for pagination.

   **Example**:  
   `https://divar-search-page-extractor.sideco.ir/?city_id=1&query=207&page=1`

2. **Divar Product Details API (Details Fetch)**  
   - Endpoint: `https://divar-page-info.sideco.ir/?tag={tag}`
   - Retrieves detailed product information for a specific tag.

   **Parameters:**
   - `tag`: The product tag, extracted from the URL.

   **Example**:  
   `https://divar-page-info.sideco.ir/?tag=12345`

## Error Handling

The script handles connection errors and exceptions by using `try-except` blocks. If any request to the Divar API fails, an error message is printed, and the script continues with the next URL or product.

## Notes

- The script assumes that the Divar API returns consistent data structures. If there are any changes in the API response format, the script may need adjustments.
- The number of URLs per page is capped at 50 for each API request. If the `url_limit` exceeds the total number of available URLs, the script will crawl as many URLs as possible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For more information about the APIs used in this script, visit:
- [Divar Search Page Extractor API](https://github.com/2077DevWave/divar-search-page-crawler)
- [Divar Page Info API](https://github.com/2077DevWave/divar-page-info-creawler)
