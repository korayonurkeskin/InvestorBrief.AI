# CompanyBrief.AI 🚀

📈 **CompanyBrief.AI** is a Python-based project that generates professional investor briefs for target companies by combining **Wikipedia-sourced data**, **live Yahoo Finance metrics**, and **strategic analysis** using **LangChain** + **Azure OpenAI**.  
The project is fully automated — from scraping, financial analysis, brief generation, and visualization through a **Streamlit** web app.

---

## 🛠️ How It Works

1. **Scrape Company Information**  
   - Extract structured company metadata (industry, leadership, AUM, etc.) from the company's Wikipedia page.

2. **Fetch Financial Metrics**  
   - Pull real-time financial data such as Market Cap, P/E Ratio, Revenue, Net Income, EBITDA, YoY Revenue Growth, and 5-Year Stock Price Growth from Yahoo Finance.

3. **Generate Investor Brief**  
   - Automatically craft a Mubadala-style internal investor memo using LangChain prompts and Azure OpenAI's LLMs, with SWOT, Strategic Fit, and Financial Snapshot sections.

4. **Visualize the Output**  
   - Instantly launch a **Streamlit** web app to view the brief in an organized and investor-ready markdown layout.

---

## 🧰 Tech Stack

- **Python**: Core scripting
- **BeautifulSoup**: Wikipedia scraping
- **YFinanceAPI**: Financial data extraction
- **LangChain** + **Azure OpenAI**: LLM-powered memo generation
- **Streamlit**: Local web app for viewing the briefs
- **dotenv**: Environment variable management
