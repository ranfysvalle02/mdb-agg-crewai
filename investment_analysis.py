import os
import pymongo

MDB_URI = "mongodb+srv://<user>:<password>@cluster0.abc123.mongodb.net/"
client = pymongo.MongoClient(MDB_URI)
db = client["sample_analytics"]
collection = db["transactions"]

from langchain_openai import AzureChatOpenAI

AZURE_OPENAI_ENDPOINT = "https://__DEMO__.openai.azure.com"
AZURE_OPENAI_API_KEY = "__AZURE_OPENAI_API_KEY__" 
deployment_name = "gpt-4-32k"  # The name of your model deployment
default_llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    azure_deployment=deployment_name,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY
)

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool

search = GoogleSerperAPIWrapper(serper_api_key='__API_KEY__')
search_tool = Tool(
        name="Google Answer",
        func=search.run,
        description="useful for when you need to ask with search"
    )

from crewai import Crew, Process, Task, Agent

researcher = Agent(
  role='Investment Researcher',
  goal="""
  Research market trends, company news, and analyst reports to identify potential investment opportunities.
  """,
  verbose=True,
  llm=default_llm,
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

tech_crew = Crew(
  agents=[researcher],
  tasks=[analysis_task],
  process=Process.sequential
)

pipeline = [
  {"$unwind": "$transactions"},
  {"$group": {
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
  {"$project": {
      "_id": 0,
      "symbol": "$_id",
      "returnOnInvestment": { "$subtract": ["$sellValue", "$buyValue"] }
    }
  },
  {"$sort": { "returnOnInvestment": -1 }}
]
results = list(collection.aggregate(pipeline))
client.close()

print("MongoDB Aggregation Pipeline Results:")
print(results)

tech_crew.kickoff(inputs={'agg_data': str(results)})

# OUTPUT:
"""
Thought: I now know the final answer
Final Answer:

Financial Summary:

From the verified data, we can see that the following stocks have generated the highest returns on investment:

1. Amazon (AMZN): 72,769,230.71
2. SAP: 39,912,931.05
3. Apple (AAPL): 25,738,882.29
4. Adobe (ADBE): 17,975,929.73

On the other hand, the following stocks have produced negative returns:

1. Atlassian Corporation Plc (TEAM): -406,507.08
2. Netflix (NFLX): -2,133,963.99
3. Intel Corporation (INTC): -7,407,861.20
4. Salesforce (CRM): -15,106,640.20
5. Microsoft (MSFT): -15,665,720.74
6. IBM: -18,356,948.23
7. Google (GOOG): -168,114,276.92

Actionable Insights and Recommendations:

Based on current news and events:

1. Amazon (AMZN): The company's stock is performing strongly, approaching its record high of 2021. It is recommended to keep an eye on this stock for potential investment opportunities.

2. SAP: Despite the company's plan to cut jobs, analysts have a positive outlook on the stock. It is advisable to monitor the stock closely for any changes in its performance.

3. Apple (AAPL): The recent surge in the company's stock value due to its intention to delve into AI shows promising growth. Investors may consider this stock for potential investment.

4. Adobe (ADBE): The stock is showing a positive sentiment in relation to other stocks in the technology sector and has a high price target set by Wall Street analysts. It is recommended to watch this stock for potential growth.

It is also suggested to keep a close eye on those stocks that are currently showing negative returns. Understanding the reasons behind their poor performance could provide investment opportunities if these issues are addressed and the businesses start to turn around.
"""
