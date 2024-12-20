import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = 'https://www.qatarairways.com/en/baggage/allowance.html'
driver.get(url)

# Wait for the page to fully load
driver.implicitly_wait(10)  # Adjust the wait time if necessary

# Get the page source after JavaScript has rendered the tables
html = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all table elements
tables = soup.find_all('table')

# Loop through each table and save them to CSV files
for idx, table in enumerate(tables):
    # Extract table headers (if present)
    headers = [header.text.strip() for header in table.find_all('th')]
    
    # Extract table rows
    rows = table.find_all('tr')

    # Extract data from each row and store it in a list
    table_data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols if ele.text.strip()]
        
        # Skip rows that don't have any data
        if len(cols) > 0:
            # Ensure the number of columns matches the header
            if len(cols) == len(headers):
                table_data.append(cols)
            elif len(cols) < len(headers):  # If fewer columns, add empty values
                table_data.append(cols + [''] * (len(headers) - len(cols)))
            elif len(cols) > len(headers):  # If more columns, trim extra columns
                table_data.append(cols[:len(headers)])

    # Create a DataFrame with headers
    df = pd.DataFrame(table_data, columns=headers)

    # Save the DataFrame to CSV in the same directory
    csv_filename = f'table_{idx + 1}_data.csv'  # Creating a unique filename for each table
    df.to_csv(csv_filename, index=False, encoding='utf-8')

    print(f"Table {idx + 1} has been saved as {csv_filename}")

# Close the browser
driver.quit()

print("All tables have been saved as separate CSV files.")
