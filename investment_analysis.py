import os
import pymongo
import pprint 

# MongoDB Setup
MDB_URI = "mongodb+srv://<user>:<password>@cluster0.abc123.mongodb.net/"
client = pymongo.MongoClient(MDB_URI)
db = client["sample_analytics"]
collection = db["transactions"]

# Azure OpenAI Setup
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

# Web Search Setup
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
duck_duck_go = DuckDuckGoSearchResults(backend="news",max_results=10)

# Search Tool - Web Search
@tool
def search_tool(query: str):
  """
  Perform online research on a particular stock.
  Will return search results along with snippets of each result.
  """
  print("\n\nSearching DuckDuckGo for:", query)
  search_results = duck_duck_go.run(query)
  search_results_str =  "[recent news for: " + query + "]\n" + str(search_results)
  return search_results_str


# Research Agent Setup
from crewai import Crew, Process, Task, Agent
AGENT_ROLE = "Investment Researcher"
AGENT_GOAL = """
  Research stock market trends, company news, and analyst reports to identify potential investment opportunities.
"""
researcher = Agent(
  role=AGENT_ROLE,
  goal=AGENT_GOAL,
  verbose=True,
  llm=default_llm,
  backstory='Expert stock researcher with decades of experience.',
  tools=[search_tool]
)

task1 = Task(
  description="""
Using the following information:

[VERIFIED DATA]
{agg_data}

*note*
The data represents the net gain or loss of each stock symbol for each transaction type (buy/sell).
Net gain or loss is a crucial metric used to gauge the profitability or efficiency of an investment. 
It's computed by subtracting the total buy value from the total sell value for each stock.
[END VERIFIED DATA]

[TASK]
- Generate a detailed financial report of the VERIFIED DATA.
- Research current events and trends, and provide actionable insights and recommendations.


[report criteria]
  - Use all available information to prepare this final financial report
  - Include a TLDR summary
  - Include 'Actionable Insights'
  - Include 'Strategic Recommendations'
  - Include a 'Other Observations' section
  - Include a 'Conclusion' section
  - IMPORTANT! You are a friendly and helpful financial expert. Always provide the best possible answer using the available information.
[end report criteria]
  """,
  agent=researcher,
  expected_output='concise markdown financial summary of the verified data and list of key points and insights from researching current events',
  tools=[search_tool],
)
# Crew Creation
tech_crew = Crew(
  agents=[researcher],
  tasks=[task1],
  process=Process.sequential
)

# MongoDB Aggregation Pipeline
pipeline = [
  {
    "$unwind": "$transactions"  # Deconstruct the transactions array into separate documents
  },
  {
    "$group": {             		 # Group documents by stock symbol
      "_id": "$transactions.symbol",  # Use symbol as the grouping key
      "buyValue": {           		 # Calculate total buy value
   	 "$sum": {
 		 "$cond": [          		 # Conditional sum based on transaction type
   		 { "$eq": ["$transactions.transaction_code", "buy"] },  # Check for "buy" transactions
   		 { "$toDouble": "$transactions.total" },      		 # Convert total to double for sum
   		 0                                         		 # Default value for non-buy transactions
 		 ]
   	 }
      },
      "sellValue": {          		 # Calculate total sell value (similar to buyValue)
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
    "$project": {            		 # Project desired fields (renaming and calculating net gain)
      "_id": 0,               		 # Exclude original _id field
      "symbol": "$_id",        		 # Rename _id to symbol for clarity
      "netGain": { "$subtract": ["$sellValue", "$buyValue"] }  # Calculate net gain
    }
  },
  {
    "$sort": { "netGain": -1 }  # Sort results by net gain (descending)
  },
  {"$limit": 3}  # Limit results to top 3 stocks 
]
results = list(collection.aggregate(pipeline))
client.close()

# Print MongoDB Aggregation Pipeline Results
print("MongoDB Aggregation Pipeline Results:")

pprint.pprint(results) #pprint is used to  to “pretty-print” arbitrary Python data structures

# Start the task execution
tech_crew.kickoff(inputs={'agg_data': str(results)})
