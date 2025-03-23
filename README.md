# **WhatsApp Chat Analysis**

This project analyzes WhatsApp chat data (Especially Group Chat Data) using **Text Preprocessing, Topic Modeling, and Network Analysis** to extract meaningful insights.

## **Features**
- **Preprocessing:** Cleans and structures WhatsApp chat data.
- **Topic Modeling:** Uses LDA (Latent Dirichlet Allocation) to identify key discussion topics.
- **Network Analysis:** Visualizes user interactions as a network graph.

---

## **Installation**

### **Clone the Repository**
```bash
git clone [<repo_link>](https://github.com/N-0-MAD/WhatsApp-Chat-Analyzer)
cd <repo_folder>
```
### **Install Dependencies**
```bash
pip install -r requirements.txt
```
## **Usage**
### Step 1: Preprocess the Chat Data
- This script cleans and structures the raw WhatsApp chat data.
- File: Preprocess.py

Run the script:
```python
import Preprocess

# Load and clean the WhatsApp chat data
df = Preprocess.load_chat("WhatsApp Chat with Biz Core team 2024-25.txt")

# Save the processed data
df.to_csv("data/processed_chat.csv", index=False)
```
**Output File:**
data/processed_chat.csv (Cleaned and structured chat data)

### Step 2: Perform Topic Modeling
- This step identifies key topics discussed in the chat using LDA.
- File: topic_modeling.py

Run the script:
```python
import pandas as pd
import topic_modeling

# Load preprocessed data
df = pd.read_csv("data/processed_chat.csv", parse_dates=['date'])

# Run topic modeling
lda_model, vectorizer, X, df = topic_modeling.perform_topic_modeling(df, num_topics=5)

# Save processed data with topic labels
df.to_csv("data/chat_with_topics.csv", index=False)

# Display results
feature_names = vectorizer.get_feature_names_out()
topic_modeling.display_topics(lda_model, feature_names)

# Plot topic trends over time
topic_modeling.plot_topic_trends(df)

# Show top users per topic
topic_modeling.top_users_per_topic(df)
```
**Output Files:**
- data/chat_with_topics.csv (Chat data with assigned topics)
- Graph: Topic trends over time

### Step 3: Generate and Plot Network Graph
- This step visualizes user interactions in a network graph.
- File: network_analysis.py

Run the script:
```python
import pandas as pd
import network_analysis

# Load preprocessed data
df = pd.read_csv("data/processed_chat.csv", parse_dates=['date'])

# Create interaction graph
G = network_analysis.create_interaction_graph(df)

# Plot the network
network_analysis.plot_graph(G, output_path="data/interaction_network.png")
```
**Output File:**
data/interaction_network.png (WhatsApp user interaction graph)

## **Notes**
- Ensure your chat file follows the standard WhatsApp export format.
- Ensure that the timestamps are in am/pm format (12-hours)
- Adjust num_topics in topic_modeling.py for different topic analysis.
- Large chat datasets may take longer to process.


### Now you’re all set to analyze your WhatsApp group discussions! 
