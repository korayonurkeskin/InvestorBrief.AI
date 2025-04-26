import requests
from bs4 import BeautifulSoup
import json
import os
import re

def clean_text(text):
    # Remove reference markers and non-breaking spaces
    text = re.sub(r'\[\d+\]', '', text)
    text = text.replace('\xa0', ' ').strip()
    return text

def scrape_company_wikipedia(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: Status {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    company_info = {}
    
    # first paragraph summary
    paragraphs = soup.select("div.mw-parser-output > p")
    for para in paragraphs:
        if para.text.strip():
            company_info["summary"] = clean_text(para.text)
            break
    
    # info box parsing
    infobox = soup.select_one("table.infobox")
    if infobox:
        rows = infobox.find_all("tr")
        for row in rows:
            if row.th and row.td:
                key = row.th.get_text().strip().lower()
                key_clean = key.replace(" ", "_").replace("(", "").replace(")", "")
                
                if key_clean == "traded_as":
                    ticker_dict = {}
                    exchange_symbols = []
                    for item in row.td.contents:
                        if isinstance(item, str) and item.strip():
                            continue
                        if getattr(item, 'name', None) == 'a':
                            exchange_symbols.append(item.get_text().strip())
                        elif getattr(item, 'name', None) == 'ul':
                            for li in item.find_all('li'):
                                links = li.find_all('a')
                                if len(links) >= 2:
                                    exchange = links[0].get_text().strip()
                                    symbol = links[1].get_text().strip()
                                    ticker_dict[exchange] = symbol
                    
                    if len(exchange_symbols) >= 2 and not ticker_dict:
                        for i in range(0, len(exchange_symbols) - 1, 2):
                            if i+1 < len(exchange_symbols):
                                exchange = exchange_symbols[i]
                                symbol = exchange_symbols[i+1]
                                ticker_dict[exchange] = symbol
                    
                    if ticker_dict:
                        company_info[key_clean] = ticker_dict
                
                elif key_clean == "key_people":
                    people = []
                    lines = [str(x) for x in row.td.contents if str(x).strip()]
                    html_content = "".join(lines)
                    for line in html_content.replace("<br/>", "<br>").split("<br>"):
                        if not line.strip():
                            continue
                        soup_line = BeautifulSoup(line, "html.parser")
                        raw = soup_line.get_text(" ", strip=True)
                        name_parts = raw.split(",", 1)
                        if len(name_parts) > 1:
                            name = name_parts[0].strip()
                            title = name_parts[1].strip()
                            people.append({"name": name, "title": title})
                        else:
                            match = re.match(r"^(.*?)\s*\(([^)]+)\)$", raw)
                            if match:
                                name, title = match.groups()
                                people.append({"name": name.strip(), "title": title.strip()})
                            else:
                                people.append({"name": raw, "title": ""})
                    
                    if people:
                        company_info[key_clean] = people
                
                elif row.td.find("ul"):
                    list_items = row.td.find_all("li")
                    company_info[key_clean] = [clean_text(li.get_text()) for li in list_items]
                
                elif row.td.find("a") and key_clean in ["website", "homepage"]:
                    links = row.td.find_all("a")
                    if links:
                        company_info[key_clean] = links[0].get('href')
                
                elif key_clean in ["founded", "industry", "headquarters"]:
                    value = clean_text(row.td.get_text())
                    company_info[key_clean] = value
                
                else:
                    value = clean_text(row.td.get_text())
                    company_info[key_clean] = value
    
    # try to get additional structured data (Revenue, Assets, Number of employees)
    try:
        financial_table = soup.select_one("table.wikitable")
        if financial_table:
            rows = financial_table.find_all("tr")
            if len(rows) > 1:  # Has header and data rows
                headers = [th.get_text().strip().lower() for th in rows[0].find_all(["th"])]
                if headers and rows[1].find_all(["td", "th"]):
                    data_cells = [clean_text(td.get_text()) for td in rows[1].find_all(["td", "th"])]
                    for i, header in enumerate(headers):
                        if i < len(data_cells):
                            key = header.replace(" ", "_").replace("(", "").replace(")", "")
                            company_info[f"financial_{key}"] = data_cells[i]
    except:
        pass

    # add source URL
    company_info["source_url"] = url
    
    return company_info

if __name__ == "__main__":
    url = input("Enter the Wikipedia URL for the company: ").strip()
    
    try:
        data = scrape_company_wikipedia(url)
        
        if not os.path.exists("./data"):
            os.makedirs("./data")
        
        filename = url.split("/")[-1].replace("_", "-").lower()
        output_path = f"./data/{filename}_wikipedia.json"
        
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved company data to {output_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")