# Design Note

## 1. Stack & Decisions

### Technology Stack

**LLM**

* OpenAI GPT-4o-mini

**Data Layer**

* Pandas

**Visualization**

* Matplotlib

**User Interface**

* Gradio

### Why These Choices?

Pandas provides reliable analytical operations over structured CSV datasets and is sufficient for datasets of this size.

Matplotlib offers lightweight chart generation without introducing unnecessary dependencies.

Gradio enables rapid deployment of an interactive web interface and integrates easily with Google Colab.

GPT-4o-mini was selected because it provides reliable structured output generation at low cost and low latency.

### Structured JSON vs Generated Code

I intentionally avoided executing model-generated Python code.

Instead, the model produces structured JSON describing:

* intent
* filters
* grouping
* aggregation parameters

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

The Query Engine translates this validated structure into trusted Pandas operations.

This approach significantly reduces security risk and prevents arbitrary code execution.

### Trade-off

The structured approach is safer and easier to validate, but less flexible than allowing unrestricted code generation.

For a government-facing application, safety and auditability are more important than maximum flexibility.

---

## 2. Correctness & Trust

The language model never generates numerical answers.

Its only responsibility is converting natural language into structured JSON.

All numerical results are computed directly from the dataset using Pandas.

To improve transparency, every answer includes:

* query intent
* applied filters
* rows used
* confidence score
* explanation of execution

The system also refuses unsupported questions rather than attempting to invent answers.

Example:

Question:

> Who is the Prime Minister of India?

Result:

The system generates a refusal response because the answer is not available in the air quality dataset.

This ensures factual correctness and prevents hallucinated outputs.

---

## 3. Government Deployment Considerations

This prototype operates on public data, but similar systems could eventually operate on sensitive government datasets.

For production deployment I would add:

### Data Residency

* Store data within approved government infrastructure.
* Avoid transferring data to third-party environments.

### Audit Logging

Maintain records of:

* user question
* generated query
* execution time
* returned result

This allows full traceability.

### Access Control

Implement:

* role-based permissions
* user authentication
* dataset-level authorization

### Security

Model-generated code execution would be prohibited.

Only validated structured operations would be allowed.

This reduces the risk of malicious prompts and unauthorized access.

---

## 4. Scaling Considerations

The current implementation uses a single CSV dataset.

Several changes would be required at larger scale.

### Data Layer

Replace Pandas with:

* DuckDB
* PostgreSQL
* BigQuery

depending on deployment requirements.

### Metadata Layer

Introduce a dataset catalog describing:

* tables
* columns
* relationships

to support multiple datasets.

### Query Planning

Implement query routing and optimization when datasets become large.

### Caching

Frequently requested analytical queries can be cached to reduce latency.

### Multi-Dataset Support

Future versions could support joins and comparisons across multiple government datasets.

---

## 5. Validation Strategy

Evaluation should involve:

### Stakeholders

* government analysts
* administrative staff
* policy teams
* citizens

### Failure Modes

Potential failures include:

* incorrect aggregations
* incorrect filters
* ambiguous language
* unsupported questions
* low-confidence responses

### Testing Approach

The evaluation set contains:

* analytical questions
* comparison questions
* visualization questions
* refusal questions

At least one answer was manually verified against a direct Pandas computation to ensure correctness.

---

## 6. Honest Limitations

Current limitations include:

### Single Dataset

The system only operates on one air quality dataset.

### Limited Intent Coverage

Only predefined analytical operations are supported.

### No Dataset Joins

Questions requiring multiple datasets cannot be answered.

### No Agentic Self-Correction

If the model generates an invalid structured query, the system currently does not automatically repair it.

### Dependence on External LLM API

The parser depends on OpenAI API availability.

### Confidence Heuristic

The confidence score is rule-based and should not be interpreted as a statistically calibrated probability.

---

## Future Work

A future enhancement would be an agentic self-correction loop:

```text
Question
    ↓
LLM
    ↓
Structured JSON
    ↓
Validator
    ↓
Validation Error
    ↓
LLM Repair Step
    ↓
Corrected JSON
    ↓
Query Engine
```

This would allow automatic recovery from malformed structured outputs before execution.

Additional future improvements include:

* multi-dataset support
* confidence calibration
* audit dashboards
* SQL/DuckDB backend
* human feedback loops
* government-scale deployment infrastructure
