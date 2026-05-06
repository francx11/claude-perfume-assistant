# Phase 6: Interview Simulation

**Prerequisite:** Phases 1–5 complete, progress/tracker.md showing all topics [x].
**Goal:** Full rehearsal under interview conditions. No notes. Timed. Scored.

---

## How to Run This Phase

Tell Claude: `"Start interview simulation, level: basic/intermediate/advanced"` or use the `interview-drill` skill.

Rules Claude will enforce:
- No hints unless you say "hint"
- Score each answer 1–5
- After each question: "What would a stronger answer include?"
- Full debrief at end of session

---

## Question Bank by Level

### Basic — Python [INTERVIEW CRITICAL]

1. What is the difference between a list and a tuple?
2. What is a decorator? Show me a simple example.
3. What is `__init__.py`? What is its purpose?
4. What is a set? Give two use cases.
5. What's the problem with `def f(x=[])`? How do you fix it?

**Pass bar:** Answer all 5 in under 2 minutes each, score ≥4/5 on each.

---

### Basic — ML Classical [INTERVIEW CRITICAL]

1. Name 3 classification algorithms and explain when you'd use each.
2. What is overfitting? Give 3 ways to prevent it.
3. What is the difference between supervised and unsupervised learning?
4. What is a confusion matrix? Calculate precision and recall from this one: TP=90, FP=10, FN=20, TN=880.

**Pass bar:** All correct, including the calculation.

---

### Basic — AI General [INTERVIEW CRITICAL]

1. What is an embedding? Give an example relevant to your project.
2. What is an LLM?
3. What is an agent in an AI system?

**Pass bar:** Connect each answer to PerfumeShop or Loopgate.

---

### Intermediate — Python [INTERVIEW CRITICAL]

1. What is the difference between a function and a generator? When would you use a generator?
2. What are the main PEP8 rules you follow? What tools enforce them?
3. You have a Python Lambda that needs `pandas` and `sentence-transformers`. How do you deploy the dependencies?
4. What is a lambda expression? Give a real example from your code.

---

### Intermediate — ML [INTERVIEW CRITICAL]

1. What is learning rate? What happens if it's too high? Too low?
2. What is fine-tuning? How is it different from training from scratch?
3. What is cross-validation? Why is k-fold better than a single train/test split?
4. What is PCA? Give a use case.

---

### Intermediate — LLMs and RAG [INTERVIEW CRITICAL]

1. Explain how RAG works. Walk me through a query in your PerfumeShop system.
2. What is the relationship between embeddings and RAG?
3. What is a vector store? Name 3 options and their tradeoffs.
4. What is prompt engineering? Give 3 techniques.

---

### Intermediate — AWS [INTERVIEW CRITICAL]

1. What is Amazon S3? Give 3 use cases.
2. What is AWS Lambda? What are its limitations?
3. What is Amazon Textract? How is it different from Tesseract?
4. What is Amazon Bedrock? How does it differ from SageMaker?

---

### Advanced — Python [INTERVIEW CRITICAL]

1. How do you implement scalable logging in a Python microservice?
2. Your distributed system has intermittent failures. How do you handle transient errors?
3. You have a data pipeline processing 10M rows daily. It's slow. How do you optimize it?

---

### Advanced — ML [INTERVIEW CRITICAL]

1. You're building a multiclass classifier with 20 classes and imbalanced data. Walk me through your approach.
2. How do you identify the most important features in a model?
3. Your model has 99% accuracy but fails in production. What could be wrong?

---

### Advanced — LLMs, RAG, Agents [INTERVIEW CRITICAL]

1. How do you evaluate the quality of a RAG system? What metrics do you use?
2. What is LoRA? Why is it useful? How does it differ from full fine-tuning?
3. What is the difference between a single agent and a multiagent system? When would you use each?
4. Design an agent that answers questions from 3 sources: SQL database, S3 documents, and a REST API.
5. What are guardrails in Amazon Bedrock? What problems do they solve?

---

### Advanced — AWS [INTERVIEW CRITICAL]

1. Design a production architecture for a multi-agent system using AWS services. Walk me through each component.
2. Textract is returning poor quality results on your documents. What are your options?
3. What are Lambda layers? What goes in a layer vs the deployment package?

---

## Full Mock Interview Protocol

Tell Claude: `"Run full mock interview, 45 minutes"`.

Claude will:
1. Pick 12 questions (2 basic, 4 intermediate, 4 advanced, 2 architectural design)
2. Time each answer (2 min basic, 3 min intermediate, 5 min advanced)
3. Score 1–5 with immediate feedback
4. Final report: strongest areas, weakest areas, 3 things to review before the real interview

---

## Completion Criteria

- [ ] 3 full mock interviews completed
- [ ] Average score ≥4/5 on basic questions
- [ ] Average score ≥3.5/5 on intermediate questions
- [ ] Average score ≥3/5 on advanced questions
- [ ] All architectural design questions answered with concrete AWS service choices
- [ ] PerfumeShop and Loopgate used as examples in ≥70% of answers
