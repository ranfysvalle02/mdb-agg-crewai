**README.md**

## MongoDB + CrewAI: Enhancing Investment Analysis

This repo houses the code and resources related to the blog post "Beyond Vectors: Augment LLM Capabilities with MongoDB Aggregation Framework and CrewAI."

**Usage:**

1. **Prerequisites**
   - MongoDB Atlas Cluster with the sample_analytics dataset loaded
   - SERPER API Key (for accessing news and market data via CrewAI) [https://serper.dev/](https://serper.dev/).
   - LLM Resource (CrewAI supports various options; instructions for these can be found at [https://docs.crewai.com/how-to/LLM-Connections/](https://docs.crewai.com/how-to/LLM-Connections/)) 

2. **Installation**
   ```bash
   pip install pymongo crewai crewai-tools langchain_openai
   ```

3. **Configuration**
   * Replace placeholders in the `config.py` file with your:
      - MongoDB Atlas connection string
      - Serper API Key
      - LLM connection details (if using CrewAI)

4. **Run the Script**
   ```bash
   python investment_analysis.py
   ```

**investment_analysis.py**

This Python script demonstrates the techniques discussed in the blog post:

* Utilizes MongoDB's Aggregation Framework to calculate Return on Investment (ROI) directly within the database, optimizing performance.
* Integrates with CrewAI to enrich the analysis with real-time news and market insights using a Large Language Model (LLM).

**Notes:**

* The provided code establishes a foundation for understanding concepts. You can customize and expand upon it for your specific investment analysis workflows.

**For further details and the complete blog post, please visit:** [Insert Blog Post Link Here]

