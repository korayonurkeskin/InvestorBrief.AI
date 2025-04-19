import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

try:
    data_file = "data/ci-financial_wikipedia.json"
    with open(data_file, "r", encoding="utf-8") as f:
        company = json.load(f)
    
    # Format key people
    key_people = company.get("key_people", [])
    key_people_str = ", ".join(
        f"{p['name']} ({p['title']})" for p in key_people if p.get("name")
    )
    
    prompt = PromptTemplate(
        input_variables=["summary", "industry", "headquarters", "aum", "key_people"],
        template="""
You are an analyst at Mubadala Capital. Write an internal investor brief using the information provided.

The brief should include:
- Company overview
- Leadership highlights
- Strategic relevance to Mubadala
- Any red flags or areas to monitor

Company Summary: {summary}
Industry: {industry}
Headquarters: {headquarters}
Assets Under Management: {aum}
Key People: {key_people}

Write the investor brief below:
"""
    )
    
    # Fill the prompt with data
    filled_prompt = prompt.format(
        summary=company.get("summary", ""),
        industry=company.get("industry", ""),
        headquarters=company.get("headquarters", ""),
        aum=company.get("aum", company.get("assets_under_management", "")),
        key_people=key_people_str
    )
    
    # Initialize Azure OpenAI with explicit model configuration for GPT-3.5
    llm = AzureChatOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        temperature=0.3
    )
    
    # Generate the response
    response = llm.invoke(filled_prompt)
    
    output_dir = "output"
    Path(output_dir).mkdir(exist_ok=True)
    
    output_path = os.path.join(output_dir, f"{Path(data_file).stem}_brief.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.content)
    
except FileNotFoundError:
    print(f"❌ Error: Could not find the data file at {data_file}")
except json.JSONDecodeError:
    print(f"❌ Error: The data file contains invalid JSON")
except Exception as e:
    print(f"❌ Error: {str(e)}")