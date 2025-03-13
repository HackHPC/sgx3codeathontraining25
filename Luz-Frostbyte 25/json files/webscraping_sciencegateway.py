#import requests
from bs4 import BeautifulSoup
import json

# Read the provided HTML file
file_path = "C:/Users/lzvazquezrivera328/Desktop/sciencegateways"
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract all resources
resources = soup.find_all("li", class_="public")

# List to store extracted data
data_list = []

# Extract data for each resource
for resource in resources:
    title = resource.find("p", class_="title").get_text(strip=True) if resource.find("p", class_="title") else "N/A"
    abstract = resource.find("p", class_="result-description").get_text(strip=True) if resource.find("p",
                                                                                                     class_="result-description") else "N/A"
    date_source = resource.find("p", class_="details").get_text(strip=True) if resource.find("p",
                                                                                             class_="details") else "N/A"

    # Extract detailed page link
    link_tag = resource.find("a", href=True)
    detailed_link = f"https://sciencegateways.org{link_tag['href']}" if link_tag else "N/A"

    # Placeholder for Emails, Websites, Languages, Frameworks, Software
    email = "N/A"
    website = "N/A"
    languages = "N/A"
    frameworks = "N/A"
    software = "N/A"

    # Append extracted data
    data_list.append({
        "Title": title,
        "Abstract": abstract,
        "Date_Source": date_source,
        "Detailed_Link": detailed_link,
        "Email": email,
        "Website": website,
        "Languages": languages,
        "Frameworks": frameworks,
        "Software": software
    })

# Save the scraped data to a JSON file
output_file = 'C:/Users/lzvazquezrivera328/Desktop/science_gateways_data.json'
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data_list, f, indent=4, ensure_ascii=False)

output_file
