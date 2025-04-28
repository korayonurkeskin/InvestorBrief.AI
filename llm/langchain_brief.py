import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from finance.yahoo_financials import get_all_financial_data, format_financials_string

load_dotenv()

def generate_brief(data_file="data/ci-financial_wikipedia.json"):
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            company = json.load(f)

        if not company.get("summary"):
            raise ValueError("Wikipedia data is incomplete or malformed.")

        key_people = company.get("key_people", [])
        key_people_str = ", ".join(
            f"{p['name']} ({p['title']})" for p in key_people if p.get("name")
        )

        ticker_symbol = "CIX.TO"
        financial_data = get_all_financial_data(ticker_symbol)
        formatted_financials = format_financials_string(financial_data)

        prompt = PromptTemplate(
            input_variables=["summary", "industry", "headquarters", "aum", "key_people", "financials"],
            template="""
You are a Data Analyst at Mubadala Capital preparing a memo for the BD/IR team.

Using the structured company data below, generate an internal investor brief with clear strategic analysis and investor-ready tone.

Your output must follow this format and reflect a thoughtful, data-backed perspective:

---

## 1. Executive Summary  
Craft a 2-sentence summary explaining the potential attractiveness of this company for Mubadala Capital. Focus on scale, market position, and strategic alignment.

## 2. Company Overview  
Concise and insightful overview — what does the company do, how big is it, who are its clients, where is it based, and what differentiates it?

## 3. Leadership Highlights  
Name the CEO, CFO, and COO. Include any context on leadership strength, track record, or relevance to Mubadala’s investment criteria.

## 4. Strategic Fit for Mubadala  
Explain how this company complements Mubadala’s portfolio. Mention regional diversification, client segment access, market trends, or operational capabilities.

## 5. SWOT Analysis  
Provide 2–3 points for each:

**Strengths**
- ...

**Weaknesses**
- ...

**Opportunities**
- ...

**Threats**
- ...

## 6. Key Risks / Monitoring Points  
Concisely list 2–3 investor-relevant risks that Mubadala should keep track of post-investment (e.g. regulatory, FX exposure, reliance on single geography).

## 7. Financial Snapshot  
{financials}

---

Structured Company Data:
- Summary: {summary}  
- Industry: {industry}  
- Headquarters: {headquarters}  
- AUM: {aum}  
- Key People: {key_people}
"""
        )

        filled_prompt = prompt.format(
            summary=company.get("summary", ""),
            industry=company.get("industry", ""),
            headquarters=company.get("headquarters", ""),
            aum=company.get("aum", company.get("assets_under_management", "")),
            key_people=key_people_str,
            financials=formatted_financials
        )

        llm = AzureChatOpenAI(
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
            temperature=0.3
        )

        response = llm.invoke(filled_prompt)

        output_dir = "output"
        Path(output_dir).mkdir(exist_ok=True)
        output_path = os.path.join(output_dir, f"{Path(data_file).stem}_brief.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.content)

        print(f"✅ Investor brief saved to {output_path}")

    except FileNotFoundError:
        print(f"❌ Error: Could not find the data file at {data_file}")
    except json.JSONDecodeError:
        print(f"❌ Error: The data file contains invalid JSON")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
