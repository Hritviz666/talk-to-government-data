# Talk to Government Data

A Natural Language Analyst over Open Public Data.

This project allows users to ask questions about government air quality data in plain English and receive data-backed answers, visualizations, provenance information, and query explanations.

Built as part of the NeuralCity Applied GenAI Intern Screening Assignment.

---

# Problem Statement

Government datasets contain valuable information but are often difficult for non-technical users to query.

This project bridges that gap by enabling users to interact with structured public datasets using natural language.

Example:

**User Question**

> What is the average PM2.5 level in Bihar?

**System Response**

* Structured query generation
* Dataset computation using Pandas
* Numerical answer
* Provenance information
* Visualization (when applicable)

---

# Dataset

Dataset Used:

**Air_Quality.csv**

Source:

Central Pollution Control Board (CPCB) Air Quality Dataset

Dataset Schema:

```text
country
state
city
station
last_update
latitude
longitude
pollutant_id
pollutant_min
pollutant_max
pollutant_avg
```

---

# Features

* Natural Language Question Answering
* Structured JSON Generation using GPT-4o-mini
* Query Validation
* Secure Query Execution
* Data-backed Answers
* Provenance Tracking
* Automatic Chart Generation
* Query Explanation
* Refusal Handling
* Confidence Score
* Human Review Routing

---

# System Architecture

```text
User Question
        ↓
GPT-4o-mini
        ↓
Structured JSON
        ↓
Validator
        ↓
Query Engine
        ↓
Chart Engine
        ↓
Confidence Engine
        ↓
Answer + Chart + Provenance
```

---

# Design Choice

## Why Structured JSON?

The language model never generates executable Python code.

Instead, it generates a constrained JSON representation of the user's intent.

Example:

```json
{
  "intent": "average",
  "pollutant": "PM2.5",
  "filters": {
    "state": "Bihar"
  }
}
```

The Query Engine executes trusted Pandas operations.

This avoids the security risks associated with executing model-generated code.

---

# Supported Intents

| Intent          | Description            |
| --------------- | ---------------------- |
| average         | Compute average value  |
| maximum         | Compute maximum value  |
| minimum         | Compute minimum value  |
| count           | Count matching records |
| compare         | Compare locations      |
| top_n           | Top N entities         |
| bottom_n        | Bottom N entities      |
| summary         | Summary statistics     |
| unique_values   | List unique values     |
| station_lookup  | Search station records |
| location_filter | Filter by location     |
| distribution    | Generate histogram     |

---

# Example Questions

```text
Average PM2.5 in Bihar

Maximum PM10 in Delhi

Top 5 cities by PM2.5

Bottom 10 stations by PM10

Summarize PM2.5 in Delhi

Show distribution of PM2.5

Which states exist?

Show Anand Vihar station
```

---

# Refusal Handling

Out-of-scope questions are refused gracefully.

Example:

```text
Question:
Who is the Prime Minister of India?

Response:
This question cannot be answered using the Air Quality dataset.
```

---

# Confidence Scoring

The system computes a confidence score based on:

* Number of matching records
* Query type
* Available evidence

Low-confidence responses are automatically flagged for human review.

Example:

```text
Confidence Score: 0.62

Status:
Needs Human Review
```

---

# Evaluation

The system was evaluated using:

* Average queries
* Top-N queries
* Summary queries
* Distribution queries
* Station lookup queries
* Out-of-scope questions

A manually verified answer was compared against a direct Pandas computation to ensure correctness.

See:

```text
evaluation.md
```

for complete results.

---

# Project Structure

```text
gov_data_chatbot/

├── app.py
├── pipeline.py
├── requirements.txt
├── README.md
├── evaluation.md
│
├── data/
│   └── Air_Quality.csv
│
├── prompts/
│   └── parser_prompt.txt
│
├── llm/
│   └── openai_parser.py
│
├── engine/
│   ├── query_engine.py
│   ├── validator.py
│   ├── chart_engine.py
│   └── confidence_engine.py
│
├── utils/
│   ├── data_loader.py
│   └── explanation.py
│
└── docs/
    ├── Design_Note.md
    └── decisions_log.md
```

---

# Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run

Start the application:

```bash
python app.py
```

Open the Gradio URL displayed in the terminal.

---

# Future Work

* Agentic self-correction loop
* Multi-dataset support
* Dataset joins
* Confidence calibration
* SQL / DuckDB backend
* User authentication
* Audit logging
* Government-scale deployment

---

# Author

Hritviz Manral

B.Tech Information Technology

IIIT Una
