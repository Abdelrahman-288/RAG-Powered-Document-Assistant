# TechRAG End-to-End RAG Evaluation

## Summary

- Total questions: **21**
- Auto-routing accuracy: **20/21 (95.24%)**
- Grounded responses: **20/21 (95.24%)**
- Citation validity: **20/21 (95.24%)**
- Overall pass rate: **19/21 (90.48%)**
- Questions requiring manual category selection: **0**

## Results

| # | Question | Expected | Resolved | Grounded | Citations | Overall |
|---:|---|---|---|---|---|---|
| 1 | What is overfitting in machine learning? | ai_ml | ai_ml | PASS | PASS (3) | PASS |
| 2 | What is regularization in machine learning? | ai_ml | ai_ml | PASS | PASS (5) | PASS |
| 3 | What is dynamic programming? | algorithms_data_structures | ai_ml | PASS | PASS (3) | FAIL |
| 4 | What is a binary search tree? | algorithms_data_structures | algorithms_data_structures | PASS | PASS (4) | PASS |
| 5 | What is SQL injection? | cybersecurity | cybersecurity | FAIL | FAIL | FAIL |
| 6 | What is cross-site scripting? | cybersecurity | cybersecurity | PASS | PASS (4) | PASS |
| 7 | What is penetration testing? | cybersecurity | cybersecurity | PASS | PASS (3) | PASS |
| 8 | What is privilege escalation? | cybersecurity | cybersecurity | PASS | PASS (4) | PASS |
| 9 | What is a pandas DataFrame? | data_science | data_science | PASS | PASS (2) | PASS |
| 10 | What is exploratory data analysis? | data_science | data_science | PASS | PASS (3) | PASS |
| 11 | What is static malware analysis? | malware_analysis | malware_analysis | PASS | PASS (3) | PASS |
| 12 | What is dynamic malware analysis? | malware_analysis | malware_analysis | PASS | PASS (3) | PASS |
| 13 | What is a Python decorator? | python | python | PASS | PASS (3) | PASS |
| 14 | What is a Python generator? | python | python | PASS | PASS (4) | PASS |
| 15 | What is a Python context manager? | python | python | PASS | PASS (3) | PASS |
| 16 | What is transfer learning in deep learning? | deep_learning | deep_learning | PASS | PASS (2) | PASS |
| 17 | What is an object detector in computer vision? | computer_vision | computer_vision | PASS | PASS (3) | PASS |
| 18 | What is cloud security? | cloud_security | cloud_security | PASS | PASS (4) | PASS |
| 19 | What is an embedded system? | embedded_systems | embedded_systems | PASS | PASS (4) | PASS |
| 20 | What is a large language model? | llm | llm | PASS | PASS (1) | PASS |
| 21 | What is tokenization in natural language processing? | nlp | nlp | PASS | PASS (3) | PASS |

## Failure Analysis

### What is dynamic programming?

- Expected category: `algorithms_data_structures`
- Resolved category: `ai_ml`
- Grounded: True
- Citation valid: True
- Citation count: 3
- Required category selection: False

### What is SQL injection?

- Expected category: `cybersecurity`
- Resolved category: `cybersecurity`
- Grounded: False
- Citation valid: False
- Citation count: 0
- Required category selection: False

## Evaluation Criteria

A test case is considered an overall pass when:

1. Auto routing selects the expected category.
2. The system does not require manual category selection.
3. The generated response is marked as grounded.
4. All generated citations are valid.
5. At least one citation is produced.
6. At least one source is retrieved.

## Pipeline Evaluated

**Question → Auto Routing → Retrieval → Reranking → Grounded Generation → Citation Validation**
