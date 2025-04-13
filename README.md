# InvestorBrief.AI

An LLM-powered BD/IR assistant that scrapes company data, transforms it with dbt, stores it in Databricks, and generates investor-ready briefs using LangChain and Azure OpenAI.

## What It Does
InvestorBrief.AI simulates how BD/IR teams at Mubadala Capital can automate company research workflows by combining real-time data ingestion with GenAI summarization and Q&A.

## Features
- Scrape live company data from sources like Crunchbase and Yahoo Finance
- Build a modular data pipeline using Python, SQL, and dbt-core
- Store cleaned data in Databricks for scalable access
- Use LangChain + Azure OpenAI to generate:
  - Executive summaries
  - Investor brief templates
  - Mock Q&A for IR teams

## Tech Stack
- **Languages:** Python, SQL
- **LLM Tools:** Azure OpenAI, LangChain, crew.ai
- **Data & Storage:** dbt-core, Databricks, SQLite (for local demo)
