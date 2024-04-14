**README.md**

**Beyond Vectors: Augment LLM Capabilities with MongoDB Aggregation Framework and CrewAI**

![](https://cosanostra-2024-vsyfm.mongodbstitch.com/crystal2.png)

How can you harness the power of data to make sound investment decisions? In the dynamic landscape of investment management, data is your most powerful ally. A single bad investment can have a ripple effect felt throughout your entire portfolio. Unlocking the actionable insights buried within raw transactional data holds the key to making sound, strategic investment decisions. This blog post will explore how MongoDB's Aggregation Framework, Large Language Models (LLMs), and CrewAI can work together to transform your investment analysis workflow.

For investment researchers and analysts, stock transaction data serves as this crystal ball, offering a glimpse into what's working and what's not. By analyzing these trends, they can make data-driven decisions on crucial aspects like investment mix, asset allocation, and balancing risk against performance.

Large Language Models (LLMs) have revolutionized our interaction with computers, providing capabilities such as drafting emails, writing poetry, and even engaging in human-like conversations. However, when it comes to dealing with complex data processing and mathematical calculations, LLMs have their limitations. That's where MongoDB's Aggregation Framework shines, offering an efficient and powerful solution for complex data analysis tasks.

**The Power of Transactional Data**

Stock transaction data offers a wealth of information for investment researchers and analysts. By carefully examining patterns within this data, you can:

* **Identify Trends:** Spot emerging market movements and potential shifts in investor sentiment.
* **Uncover Hidden Opportunities:** Discover undervalued stocks or sectors poised for growth.
* **Manage Risk:** Assess the volatility of specific holdings and make informed decisions about asset allocation for optimal risk-return balance.

## The Task: Investment Performance Analysis

Consider a scenario where we need to determine the return on investment (ROI) for each stock over a certain period. This task involves filtering the sales by product, calculating the ROI, and then sorting these to find the stocks with the highest returns. Traditional methods like SQL or application code processing can be complex and inefficient, especially with large datasets.

In SQL, this would require multiple subqueries, temporary tables, and joins - a complex and potentially inefficient process, especially with large datasets. With application code, you would need to retrieve all the data first, calculate the ROI, and then perform the sorting, which could be resource-intensive.

**Benefits**

* **Informed Decision-Making:**  ROI analysis provides a clear metric for evaluating the success of past investments. This data empowers investors, from individuals to large institutions, to make informed decisions about buying, selling, or holding specific stocks. 
* **Portfolio Optimization:**  Identifying high and low-performing stocks is crucial for adjusting your investment mix. You might shift investments towards top-performing assets or re-evaluate underperforming ones.
* **Identifying Trends:** Analyzing ROI over time can reveal trends within individual stocks or broader market sectors. Recognizing these patterns helps investors anticipate potential opportunities or risks.
* **Benchmarking:** Comparing your portfolio's ROI to relevant market indices helps gauge how your investments are performing relative to the overall market.
* **Tax Implications:** In many jurisdictions, calculating the ROI of investments plays a role in determining capital gains or losses, impacting tax calculations.

**Usage:**

1. **Prerequisites**
   - MongoDB Atlas Cluster with the sample_analytics dataset loaded
   - SERPER API Key (for accessing news and market data via CrewAI) [https://serper.dev/](https://serper.dev/)
   - LLM Resource (CrewAI supports various options; [https://docs.crewai.com/how-to/LLM-Connections/](https://docs.crewai.com/how-to/LLM-Connections/)) 

2. **Installation**
   ```bash
   pip install pymongo crewai crewai-tools langchain_openai
   ```

3. **Run the Script**
   ```bash
   python investment_analysis.py
   ```

**investment_analysis.py**

```
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
```

This Python script demonstrates the techniques discussed in the blog post:

* Utilizes MongoDB's Aggregation Framework to calculate Return on Investment (ROI) directly within the database, optimizing performance.
* Integrates with CrewAI to enrich the analysis with real-time news and market insights using a Large Language Model (LLM).

**Notes:**

* The provided code establishes a foundation for understanding concepts. You can customize and expand upon it for your specific investment analysis workflows.

**For further details and the complete blog post, please visit:** [Insert Blog Post Link Here]

