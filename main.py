import os
import json
import subprocess
from scraper.scrape_company_data import scrape_company_wikipedia
from llm.langchain_brief import generate_brief

def launch_streamlit_viewer():
    print("\n🚀 Launching the Investor Brief Viewer...\n")
    subprocess.run(["streamlit", "run", "llm/generate_brief_viewer.py"])

if __name__ == "__main__":
    try:
        print("Scraping company data from Wikipedia...")

        url = "https://en.wikipedia.org/wiki/CI_Financial"
        company_data = scrape_company_wikipedia(url)

        os.makedirs("data", exist_ok=True)
        data_path = "data/ci-financial_wikipedia.json"
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(company_data, f, indent=2)

        print("Scraped and saved company data.\n")

        print("Generating investor brief with LangChain...\n")
        generate_brief(data_path)

        print("✅ Generated investor brief.\n")

        launch_streamlit_viewer()

    except Exception as e:
        print(f"❌ Error: {str(e)}")