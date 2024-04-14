import os

from crewai import Agent
from crewai_tools import SerperDevTool
from crewai import Task
from langchain_openai import AzureChatOpenAI
from crewai import Crew, Process
import pymongo
import os
os.environ["SERPER_API_KEY"] = "__KEY_GOES_HERE__"
MDB_URI = "mongodb+srv://user:password@cluster2.abc123.mongodb.net/"
client = pymongo.MongoClient(MDB_URI)
search_tool = SerperDevTool()
azure_llm = AzureChatOpenAI(
    azure_endpoint="https://demo.openai.azure.com",
    azure_deployment="gpt-4-32k",
    api_key="demo",
    api_version="2023-03-15-preview",
)

researcher = Agent(
  role='Investment Researcher',
  goal="""
  Research market trends, company news, and analyst reports to identify potential investment opportunities.
  """,
  verbose=True,
  llm=azure_llm, 
  backstory='Expert in using search engines to uncover relevant financial data, news articles, and industry analysis.',
  tools=[search_tool] 
) 

analysis_task = Task(
  description="""
Using the following information:

[VERIFIED DATA]
{agg_data}

*note* 
The data represents the average price of each stock symbol for each transaction type (buy/sell), 
and the total amount of transactions for each type. This would give us insight into the average costs and proceeds from each stock, 
as well as the volume of transactions for each stock.
[END VERIFIED DATA]

[TASK]
- Provide a financial summary of the VERIFIED DATA
- Research current events and trends, and provide actionable insights and recommendations
  """,
  agent=researcher,
  expected_output='concise markdown financial summary and list of actionable insights and recommendations',
  tools=[search_tool],
)
# Instantiate your crew
tech_crew = Crew(
  agents=[researcher],
  tasks=[analysis_task],
  process=Process.sequential 
)

db = client["sample_analytics"]
collection = db["transactions"]
pipeline = [
  {
    "$unwind": "$transactions"
  },
  {
    "$group": {
      "_id": "$transactions.symbol",
      "buyValue": {
        "$sum": {
          "$cond": [
            { "$eq": ["$transactions.transaction_code", "buy"] },
            { "$toDouble": "$transactions.total" },
            0
          ]
        }
      },
      "sellValue": {
        "$sum": {
          "$cond": [
            { "$eq": ["$transactions.transaction_code", "sell"] },
            { "$toDouble": "$transactions.total" },
            0
          ]
        }
      }
    }
  },
  {
    "$project": {
      "_id": 0,
      "symbol": "$_id",
      "returnOnInvestment": { "$subtract": ["$sellValue", "$buyValue"] }
    }
  },
  {
    "$sort": { "returnOnInvestment": -1 }
  }
]
results = list(collection.aggregate(pipeline))
print(results)
client.close()
# Begin the task execution
tech_crew.kickoff(inputs={'agg_data': str(results)})
