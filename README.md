## InvestorBrief.AI

InvestorBrief.AI is a fully automated Python-based tool that generates professional-grade investor briefs by combining Wikipedia company data, live Yahoo Finance metrics, and LLM-powered strategic analysis using LangChain and Azure OpenAI.
The entire pipeline from data scraping and financial analysis to brief generation runs seamlessly with a single command.

---

## How It Works

1. **Scrape Company Information**

   - Extract structured company metadata (industry, leadership, AUM, etc.) from the company's Wikipedia page.

2. **Fetch Financial Metrics**

   - Pull real-time financial data such as Market Cap, P/E Ratio, Revenue, Net Income, EBITDA, YoY Revenue Growth, and 5-Year Stock Price Growth from Yahoo Finance.

3. **Generate Investor Brief**

   - Automatically craft a Mubadala-style internal investor memo using LangChain prompts and Azure OpenAI's LLMs, with SWOT, Strategic Fit, and Financial Snapshot sections.

4. **Visualize the Output**
   - Instantly launches a Streamlit web app to view the brief in a clean, investor-ready markdown layout.

---

## Tech Stack

- **Python**: Core automation and orchestration
- **BeautifulSoup**: Wikipedia scraping
- **YFinanceAPI**: Live financial data extraction
- **LangChain** + **Azure OpenAI**: LLM-powered memo generation
- **Streamlit**: Local web app for viewing the briefs
- **dotenv**: Environment variable management
