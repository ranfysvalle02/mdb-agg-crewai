**Beyond Vectors: Augment LLM Capabilities with MongoDB Aggregation Framework**

![Augment LLM Capabilities with MongoDB Aggregation Framework](https://raw.githubusercontent.com/ranfysvalle02/blog-drafts/main/blog-flow.png)

In the dynamic landscape of investment management, real-time transaction data is your most powerful ally. A single bad decision can have a ripple effect felt throughout your entire portfolio. Unlocking the actionable insights buried within raw transactional data holds the key to making sound, strategic investment decisions. This blog post will explore how [MongoDB's Aggregation Framework](https://www.mongodb.com/developer/products/mongodb/introduction-aggregation-framework/) and GenAI can work together to transform your data analysis workflow.

Large Language Models (LLMs) have revolutionized our interaction with computers, providing capabilities such as drafting emails, writing poetry, and even engaging in human-like conversations. However, when it comes to dealing with complex data processing and mathematical calculations, LLMs have their limitations.


While Large Language Models (LLMs) excel at language, they lack the ability to understand and manipulate numbers or symbols in the same way. That's where MongoDB's Aggregation Framework shines, offering an efficient and powerful solution for complex data analysis tasks. It allows you to process entire collections of data, passing it through a multi-stage data pipeline. Within these stages, you can perform calculations and transformations on entire collections. This bypasses the limitations of LLMs for numerical computations, providing a robust and reliable method for data analysis.

In this blog post, we’ll combine the power of the MongoDB Aggregation framework with GenAI to overcome the limitations of “Classic RAG”. We'll explore this by delving into the MongoDB Atlas Sample Dataset, specifically the `sample_analytics` database and the `transactions` collection. The sample_analytics database contains three collections for a typical financial services application. It has customers, accounts, and transactions. For this example, we'll focus on the transaction data which offers a realistic dataset that allows users to hone their skills in data analysis, querying, and aggregation, particularly in the context of financial data.

The source code is available at [GitHub - mdb-agg-crewai](https://github.com/ranfysvalle02/mdb-agg-crewai/blob/main/investment_analysis.py)

**Before We Start**

To follow along, you'll need:

1. **MongoDB Atlas Cluster:** [Create your free cluster](https://www.mongodb.com/docs/guides/atlas/cluster/) and [load the Sample Dataset](https://www.mongodb.com/basics/sample-database). The transaction data in the sample analytics dataset offers a realistic dataset that allows users to hone their skills in data analysis, querying, and aggregation, particularly in the context of financial data.

2. **LLM Resource:** CrewAI supports various LLM connections, including local models (Ollama), APIs like Azure, and all LangChain LLM components for customizable AI solutions. [Click here to learn more about CrewAI LLM Support](https://docs.crewai.com/how-to/LLM-Connections/)

**note:** _The source code in the example uses Azure OpenAI. To follow along, you’ll need a valid [Azure OpenAI deployment](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)_

**Required Python Packages**
- `pip install pymongo crewai`

### `sample_analytics.transactions`

The [sample_analytics database](https://www.mongodb.com/docs/atlas/sample-data/sample-analytics/) contains three collections (customers, accounts, transactions) for a typical financial services application. The transactions collection contains transaction details for users. Each document contains an account id, a count of how many transactions are in this set, the start and end dates for transactions covered by this document, and a list of sub documents. Each sub document represents a single transaction and the related information for that transaction.

- `transaction_id`: This is a unique identifier that distinctly marks each transaction.
- `account_id`: This field establishes a connection between the transaction and its corresponding account.
- `date`: This represents the precise date and time at which the transaction took place.
- `transaction_code`: This indicates the nature of the transaction, such as a deposit, withdrawal, buy, or sell.
- `symbol`: This field denotes the symbol of the stock or investment involved in the transaction.
- `amount`: This reflects the value of the transaction.
- `total`: This captures the comprehensive transacted amount, inclusive of quantities, fees, and any additional charges associated with the transaction.

![Transaction Document Schema](https://raw.githubusercontent.com/ranfysvalle02/blog-drafts/main/schema.png)

### The Task: Uncover Hidden Opportunities

Picture this: You're running a company with a standard financial services application. Your objective? To spot hidden opportunities in the market by scrutinizing all transaction data and identifying the top three stocks based on net gain or loss. We can then research current events and market trends to uncover potential opportunities in the stocks that have historically shown the best net gain, according to our transaction data.

Net gain is a critical metric in investment analysis as it provides a clear picture of the profitability of an investment over a certain period. It's the difference between the total amount received from selling an investment (like stocks) and the total amount spent buying it.

Here's why net gain matters:

1. **Profitability Assessment:** Net gain allows investors to assess the profitability of their investments. A positive net gain indicates that the investment has generated a profit, while a negative net gain suggests a loss.

2. **Performance Comparison:** It helps investors compare the performance of different investments. By calculating the net gain for each investment, investors can identify which investments are performing well and which are underperforming.

3. **Investment Strategy Evaluation:** Net gain can be used to evaluate the effectiveness of an investment strategy. If an investment strategy consistently results in a positive net gain, it's likely a good strategy. Conversely, a strategy that often results in a negative net gain may need to be reevaluated.

4. **Risk Management:** Understanding the net gain can help in managing investment risks. If an investment consistently results in a negative net gain, it might be too risky and may need to be sold off.

5. **Decision Making:** Net gain is a crucial piece of information that can influence future investment decisions. For instance, knowing which stocks have historically shown the best net gain can guide investors towards potentially profitable opportunities.

In summary, net gain is a vital metric in investment management. It provides valuable insights into the profitability of investments, aids in performance comparison, helps evaluate investment strategies, assists in risk management, and guides decision-making. It's a key piece of information that can help investors make informed decisions and maximize their returns.

In a traditional SQL environment, calculating the net gain on transactional data would require multiple subqueries, temporary tables, and joins - a complex and potentially inefficient process, especially when dealing with large datasets. If you were to use application code, you'd need to first retrieve all the data, calculate the net gain or loss, and then sort the results. This could be a resource-intensive task, demanding significant computational power and time.

Navigating these complexities can be made more efficient by harnessing the power of MongoDB's Aggregation Framework, combined with the intelligent capabilities of AI technologies like CrewAI and Large Language Models (LLMs). This potent combination not only streamlines the process but also uncovers deeper insights from our data.


### The Solution: MongoDB's Aggregation Framework

The aggregation pipeline we will be building calculates the total buy and sell values for each stock, and then calculates the net gain or loss by subtracting the total buy value from the total sell value. The stocks are then sorted by net gain or loss in descending order, so the stocks with the highest net gains are at the top. If you’re new to MongoDB, I suggest you build this aggregation pipeline using the aggregation builder in compass, then export it to Python. [The Aggregation Pipeline Builder in MongoDB Compass](https://www.mongodb.com/docs/compass/current/create-agg-pipeline/) helps you create aggregation pipelines to process documents from a collection or view and return computed results.

### Supercharge Investment Analysis with MongoDB and CrewAI

![CrewAI Visualization](https://raw.githubusercontent.com/ranfysvalle02/blog-drafts/main/HighLevelChart_noBG.jpg)

(_image from  [LangChain Blog | CrewAI: The Future of AI Agent Teams](https://blog.langchain.dev/crewai-unleashed-future-of-ai-agent-teams/))_


The MongoDB Aggregation Pipeline gives us the data we need to analyze. The faster you can extract meaningful insights from raw data, the better your investment decisions will be. CrewAI, combined with the power of MongoDB Atlas, provides a unique approach that goes beyond basic number-crunching to deliver truly actionable analysis.

For this example, we will create an Investment Researcher Agent. This agent is our expert, skilled in finding valuable data using tools like search engines. It's designed to hunt down financial trends, company news, and analyst insights. To learn more about creating agents using CrewAI [click here](https://learn.crewai.com/)

**Unlocking the Power of AI Collaboration: Agents, Tasks, and Tools**

The realm of artificial intelligence (AI) is rapidly evolving, transforming how we approach tasks and projects in the data-driven world we live in. CrewAI takes this a step further by introducing a groundbreaking framework for collaborative AI. This framework empowers teams to achieve more than ever before by leveraging the combined strengths of specialized AI units and streamlined workflows.

At the core of CrewAI lie **agents**. These are not your typical AI assistants; instead, they function as intelligent team members, each with a distinct **role** (e.g., researcher, writer, editor) and a well-defined **goal**. They possess the capability to perform tasks, make decisions, and even communicate with other agents to achieve the overarching objectives of a crew.

But what truly sets CrewAI apart is its ability to orchestrate seamless collaboration between these agents. This is achieved through a system of **tasks**. Tasks act as the building blocks of CrewAI workflows, allowing you to define a sequence of actions that leverage the strengths of different agents.

CrewAI also provides a comprehensive arsenal of **tools** that further empower these agents. These tools encompass a wide range of capabilities, including web scraping, data analysis, and content generation. By equipping agents with the right tools, you can ensure they have everything they need to perform their tasks effectively.

In essence, CrewAI's powerful combination of agents, tasks, and tools empowers you to:

* **Automate repetitive tasks:** Free up your team's valuable time and resources by automating mundane or repetitive tasks.
* **Streamline workflows:** Design efficient workflows that leverage the strengths of AI collaboration.
* **Unlock the true potential of AI:** Move beyond basic AI functionalities and harness the power of collaborative AI for complex projects.


### The Code

In this section, we'll walk through the Python code used to perform financial analysis based on transaction data stored in MongoDB, using GenAI for data analysis and insights. The Python version used during development was: `3.10.10`

### MongoDB Setup

First, we set up a connection to MongoDB using [pymongo](https://pymongo.readthedocs.io/en/stable/). This is where our transaction data is stored. We'll be performing an aggregation on this data later.

**Important:** While we're including the connection string directly in the code for demonstration purposes, it's not recommended for real-world applications. A more secure approach is to retrieve the connection string from your MongoDB Atlas cluster.

Here's how to access your connection string from Atlas:

* Log in to your MongoDB Atlas account and navigate to your cluster.
* Click on "Connect" in the left-hand navigation menu.
* Choose the driver you'll be using (e.g., Python) and its version.
* You'll see a connection string provided. Copy this string for use in your application.

Once you have your connection string, you are ready to start.

#### **file: investment_analysis.py**
```python
import os
import pymongo

MDB_URI = "mongodb+srv://<user>:<password>@cluster0.abc123.mongodb.net/"
client = pymongo.MongoClient(MDB_URI)
db = client["sample_analytics"]
collection = db["transactions"]
```

### Azure OpenAI Setup

Next, we set up our Azure OpenAI LLM resource. The code in the example uses Azure OpenAI. To follow along, you’ll need a valid [Azure OpenAI deployment](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)


#### **file: investment_analysis.py**
```python
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
```


### Web Search API Setup

For this example, we will be using the [The DuckDuckGo Search Langchain Integration](https://python.langchain.com/v0.2/docs/integrations/tools/ddg/). The DuckDuckGo Search is a component that allows users to search the web using DuckDuckGo.

#### **file: investment_analysis.py**
```python
# Web Search Setup
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
duck_duck_go = DuckDuckGoSearchResults(backend="news")

# Search Tool - Web Search
@tool
def search_tool(query: str):
  """
  Perform online research on a particular stock.
  """
  return duck_duck_go.run(query)
```

DuckDuckGo was chosen for this example because it:

- **Requires NO API KEY**
- Easy to use
- Provides `snippets` I can use to get a general sense of the content

![DuckDuckGo Search Tool](https://raw.githubusercontent.com/ranfysvalle02/blog-drafts/main/x219.png)

### CrewAI Setup

We'll be using CrewAI to manage our agents and tasks. In this case, we have one agent - a researcher who is tasked with analyzing the data and providing actionable insights.

### CrewAI Setup

We'll be using CrewAI to manage our agents and tasks. In this case, we have one agent - a researcher who is tasked with analyzing the data and providing actionable insights. ​​In CrewAI, tasks are the individual steps that make up a larger workflow.

**Agents & Tasks: Working Together as a Crew**

CrewAI orchestrates the execution of tasks by agents. In CrewAI, a Crew represents a collaborative group of agents working together to achieve a set of tasks. While our example is a single-agent Crew for simplicity, CrewAI's power truly shines when you create multi-agent Crews for complex workflows.

* **Tasks:** These are the individual steps that make up your investment research workflow. Each task represents a specific action the agent needs to take to achieve the overall goal.
* **Agents:** Think of these as the workers who execute the tasks. We'll have a dedicated "Investment Researcher" agent equipped with the necessary tools and knowledge to complete the assigned tasks.

**Fine-Tuning Your Investment Researcher**

CrewAI allows you to customize your agent's behavior through various parameters: 

* **Role & Goal (AGENT_ROLE & AGENT_GOAL):** These define the agent's purpose.  Here, we set the role to "Investment Researcher" with a goal of "identifying investment opportunities." This guides the agent towards relevant data sources and analysis methods (e.g., market trends, company news, analyst reports).
* **Backstory:** Craft a backstory like "Expert stock researcher with decades of experience" to add context and potentially influence the agent's communication style and interpretation of information.
* **Tools:** Equip your agent with tools (functions or classes) to complete its tasks. This could include a search tool for gathering information or an analysis tool for processing data.
* **Large Language Model (LLM):** This is the AI engine powering the agent's tasks like text processing and generation. Choosing a different LLM can significantly impact the agent's output based on the underlying LLM’s strengths and weaknesses.
* **Verbose (verbose):** Setting `verbose=True` provides a more detailed log of the agent's thought process for debugging purposes.

By adjusting these parameters, you can tailor your investment research agent to focus on specific market sectors, prioritize certain information sources, and even potentially influence its risk tolerance or investment style (through the `backstory`).

#### **file: investment_analysis.py**
```python
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

```

### MongoDB Aggregation Pipeline

Next, we define our MongoDB aggregation pipeline. This pipeline is used to process our transaction data and calculate the net gain for each stock symbol.

#### **file: investment_analysis.py**
```python
# MongoDB Aggregation Pipeline
pipeline = [
  {
	"$unwind": "$transactions"  # Deconstruct the transactions array into separate documents
  },
  {
	"$group": {        			  # Group documents by stock symbol
  	"_id": "$transactions.symbol",  # Use symbol as the grouping key
  	"buyValue": {      			  # Calculate total buy value
  	  "$sum": {
		  "$cond": [     			  # Conditional sum based on transaction type
  		  { "$eq": ["$transactions.transaction_code", "buy"] },  # Check for "buy" transactions
  		  { "$toDouble": "$transactions.total" }, 			  # Convert total to double for sum
  		  0                                    			  # Default value for non-buy transactions
		  ]
  	  }
  	},
  	"sellValue": {     			  # Calculate total sell value (similar to buyValue)
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
	"$project": {       			  # Project desired fields (renaming and calculating net gain)
  	"_id": 0,          			  # Exclude original _id field
  	"symbol": "$_id",   			  # Rename _id to symbol for clarity
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

print("MongoDB Aggregation Pipeline Results:")
print(results)
```


Here's a breakdown of what the MongoDB pipeline does:

1. **Unwinding Transactions:** First, it uses the `$unwind` operator to unpack an array field named "transactions" within each document. Each document contains information about multiple stock purchases and sales. Unwinding separates these transactions into individual documents, simplifying subsequent calculations.

2. **Grouping by Symbol:** Next, the `$group` operator groups the unwound documents based on the value in the "transactions.symbol" field. This essentially combines all transactions for a specific stock (represented by the symbol) into a single group.

3. **Calculating Buy and Sell Values:** Within each symbol group, the pipeline calculates two crucial values:
   - **buyValue:** This uses the `$sum` accumulator along with a conditional statement (`$cond`). The `$cond` checks if the "transaction_code" within the "transactions" object is "buy". If it is, it converts the "total" field (the transaction amount) to a double using `$toDouble` and adds it to the running total for buyValue. If it's not a buy transaction, it contributes nothing (0) to the sum. This effectively calculates the total amount spent buying shares of that specific symbol.
   - **sellValue:** Similar to buyValue, this calculates the total amount received by selling shares of the same symbol. It uses the same logic but checks for "transaction_code" equal to "sell" and sums those "total" values.

4. **Projecting Results:** Now, the `$project` operator steps in to define the final output format. It discards the automatically generated grouping identifier (`_id`) by setting it to 0. It then renames the grouping field (`_id` which held the "transactions.symbol") to a clearer name, "symbol". Finally, it calculates the net gain or loss for each symbol using the `$subtract` operator. This subtracts the `buyValue` from the `sellValue` to determine the net gain or loss for that symbol.

5. **Sorting by Net Gain:** The `$sort` operator organizes the results. It sorts the documents based on the "netGain" field in descending order (-1). This means symbols with the highest net gain (most profitable) will appear first in the final output.

6. **Limiting Results:** Lastly, the `$limit` operator is used to limit the number of documents passed to the next stage in the pipeline. In this case, it's set to 3, meaning only the top three documents (stocks with the highest net gain) will be included in the final output.

![MongoDB Aggregation Pipeline Results Screenshot](https://raw.githubusercontent.com/ranfysvalle02/blog-drafts/main/x221.png)

### Task Execution

Finally, we kick off our task execution. The researcher agent will use the data from our MongoDB aggregation, as well as any other tools at their disposal, to analyze the data and provide insights.

#### **file: investment_analysis.py**
```python
tech_crew.kickoff(inputs={'agg_data': str(results)})
```

### Complete Source Code
#### **file: investment_analysis.py**
```python
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
	"$group": {        			  # Group documents by stock symbol
  	"_id": "$transactions.symbol",  # Use symbol as the grouping key
  	"buyValue": {      			  # Calculate total buy value
  	  "$sum": {
		  "$cond": [     			  # Conditional sum based on transaction type
  		  { "$eq": ["$transactions.transaction_code", "buy"] },  # Check for "buy" transactions
  		  { "$toDouble": "$transactions.total" }, 			  # Convert total to double for sum
  		  0                                    			  # Default value for non-buy transactions
		  ]
  	  }
  	},
  	"sellValue": {     			  # Calculate total sell value (similar to buyValue)
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
	"$project": {       			  # Project desired fields (renaming and calculating net gain)
  	"_id": 0,          			  # Exclude original _id field
  	"symbol": "$_id",   			  # Rename _id to symbol for clarity
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
```


### Example OUTPUT

```
Thought:
The recent news for Apple indicates that the company's stock has reached a $3 trillion valuation, largely due to the hype surrounding the introduction of AI to iPhones. This could be a significant catalyst for Apple's future growth. Now, I have enough information to generate a detailed financial report of the verified data, including a TLDR summary, actionable insights, strategic recommendations, other observations, and a conclusion.

Final Answer:

**Financial Report**

**TLDR Summary**

Based on the verified data, the net gains for the three stocks are as follows:

1. Amazon (AMZN) - $72,769,230.71
2. SAP - $39,912,931.04
3. Apple (AAPL) - $25,738,882.29

Amazon has the highest net gain, followed by SAP and Apple.

**Actionable Insights**

- **Amazon (AMZN):** The company's stock is seen as a good buy due to its attractive valuation and significant dominance in the e-commerce market.
- **SAP:** The company is making a significant acquisition of WalkMe Ltd., which could potentially boost its value and market position.
- **Apple (AAPL):** The company's stock has reached a $3 trillion valuation, largely due to the hype surrounding the introduction of AI to iPhones. This could be a significant catalyst for Apple's future growth.

**Strategic Recommendations**

- **Amazon (AMZN):** Given its dominant position in e-commerce and attractive valuation, it might be a good idea to consider increasing investments in Amazon.
- **SAP:** Considering the potential value boost from the recent acquisition, investors might want to keep a close watch on SAP's performance and consider it for their portfolio.
- **Apple (AAPL):** With the hype around the introduction of AI to iPhones, Apple's stock could see significant growth. It might be a good time to invest or increase existing investments.

**Other Observations**

The companies have seen fluctuations in their stock prices but generally perform well. The current trends and developments indicate potential for further growth.

**Conclusion**

Given the net gains and recent developments, Amazon, SAP, and Apple seem to be promising investments. However, as with any investment decision, it's important to consider individual financial goals, risk tolerance, and market conditions. It's always recommended to conduct further research or consult with a financial advisor before making investment decisions.

This report provides a high-level overview of the current events and trends impacting these stocks, but the rapidly changing market environment necessitates regular monitoring and analysis of investment portfolios.

> Finished chain.

```

### Limitations and Considerations

While the combination of MongoDB's Aggregation Framework and GenAI represents a powerful tool for data analysis and interpretation, it's important to recognize a few potential limitations:

1. **Dependence on Historical Data:** Past performance may not always predict future results, especially in unpredictable markets where unforeseen events can significantly impact investment outcomes.

2. **Dependence on Search Result Snippets:** The snippets provided by DuckDuckGo may not always provide enough information. You could take this a step further by scraping the search result URL using something like [Firecrawl](https://www.firecrawl.dev/) - which can crawl and convert any website into clean markdown or structured data.

3. **Uncertainty in Predictions:** Despite the sophistication of the analysis, there will always be an inherent degree of uncertainty in investment predictions. Future outcomes are inherently unknowable, and factors beyond the scope of historical data can influence results.

4. **LLM Limitations:** LLMs are still evolving, and their ability to research, interpret and analyze data is continually improving. However, biases in training data or limitations in the model's architecture could lead to inaccurate or misleading insights.

By being aware of these limitations and taking steps to mitigate them, you can ensure a more responsible and well-rounded approach to investment analysis.

### Conclusion

In this blog post, we explored how MongoDB's Aggregation Framework, Large Language Models (LLMs), and CrewAI can be leveraged to transform investment analysis. The key to unlocking smarter investment decisions lies in harnessing the power of your transaction data. MongoDB's Aggregation Framework provides the tools to efficiently calculate essential metrics like net gain, and more right within the Data Platform with no additional code required at the application layer. When combined with CrewAI's ability to automate research workflows, you'll gain a deeper understanding of the market and be able to identify hidden opportunities, make informed decisions, and ultimately boost your investment success.

### The Future: AI-Powered Investment Analysis

The future of investment analysis belongs to those who embrace the power of data and AI. By combining MongoDB's robust data platform with the insight-generating capabilities of AI tools like CrewAI, you gain the ability to:

* **Analyze trends faster** than those relying on traditional methods.
* **Identify profitable patterns** that others miss.
* **Make informed decisions** backed by both raw data and contextual insights.
* **Automate tedious analysis**, giving you more time for strategic thinking.

Don't just analyze the market – shape it. Start harnessing the potential of MongoDB and AI today, and transform your investment decision-making process.

The source code is available at [GitHub - mdb-agg-crewai](https://github.com/ranfysvalle02/mdb-agg-crewai/blob/main/investment_analysis.py)

