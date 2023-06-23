import requests
from bs4 import BeautifulSoup
import csv

"""
    CSV format 
    Course,,Title,ACP,CS,,HUM,NAT,QR,SBS
"""

def website_table_to_csv(url):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')  # Assuming there is only one table in the webpage
    
    rows = []
    for row in table.find_all('tr'):
        cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
        rows.append(cells)
    
    # Write the rows to a CSV file
    with open('courses.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

website_table_to_csv('https://courses.illinois.edu/gened/2023/fall/CS')
