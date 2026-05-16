# HalluAudio

HalluAudio is a large-scale benchmark for evaluating hallucination behaviors in Large Audio-Language Models (LALMs).  
The benchmark covers three major audio domains:

- **Speech**
- **Environmental Sound**
- **Music**

Unlike conventional audio QA benchmarks that primarily focus on task accuracy, HalluAudio is specifically designed to evaluate:

- Unsupported assertions
- Affirmative bias
- Structural hallucinations
- Semantic hallucinations
- Perceptual hallucinations
- False refusal behaviors

The benchmark contains **5,720 human-verified QA pairs** with adversarial, contrastive, and open-ended task designs.

---

# Dataset

## HuggingFace Dataset

Dataset link:

👉 https://huggingface.co/datasets/zhaozhao09/HalluAudio

---

# Dataset Overview

| Domain | #QA Pairs |
|---|---|
| Speech | 2,200 |
| Environmental Sound | 1,958 |
| Music | 1,562 |
| **Total** | **5,720** |

---

# Benchmark Characteristics

HalluAudio contains:

- Contrastive constructions
- Adversarial invalid queries
- Binary QA
- Open-ended QA
- Counting tasks
- Temporal reasoning tasks
- Structural perturbation tasks

The benchmark evaluates hallucination from multiple perspectives beyond standard accuracy.

---

# Evaluation Metrics

HalluAudio includes several hallucination-oriented metrics:

| Metric | Description |
|---|---|
| Accuracy | Standard task correctness |
| Yes Prediction Ratio | Measures affirmative bias |
| Unrelated Error Ratio | Measures semantically unrelated responses |
| Conditional Accuracy | Accuracy conditioned on valid answer type |
| False Refusal Rate (FRR) | Measures over-conservative refusals |

---

# Repository Structure

```text
.
├── accuracy_classify.py
├── accuracy_else.py
├── refuse_to_answer.py
├── reject_group.py
├── yesno_bias_figure.py
├── yesno_bias_test.py
└── README.md
