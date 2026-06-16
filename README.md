<div align="center">
  <h1>🔊 HalluAudio</h1>
  <p>
    Official inference code for<br>
    <b><em>HalluAudio: A Comprehensive Benchmark for Hallucination Detection in Large Audio-Language Models</em></b>
  </p>
  <p>
    <a href="https://huggingface.co/datasets/zhaozhao09/HalluAudio"><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-blue' alt="HF-dataset"></a>
    <a href="https://github.com/Feiyuzhao25/halluaudio"><img src="https://img.shields.io/badge/Code-Github-red" alt="Code"></a>
    <a href="https://arxiv.org/abs/2604.19300"><img src="https://img.shields.io/badge/arXiv-2604.19300-b31b1b" alt="arXiv"></a>
  </p>
</div>

## Overview

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

## Dataset

### 1. Dataset Overview

| Domain | #QA Pairs |
|---|---|
| Speech | 2,200 |
| Environmental Sound | 1,958 |
| Music | 1,562 |
| **Total** | **5,720** |

---

### 2. Dataset Format

Each subset in HalluAudio is organized into four fields:

| Field | Description |
|---|---|
| `audio` | Audio sample stored in byte format |
| `prompt` | Prompt for every task |
| `reference` | Ground-truth answer |
| `subset` | Task category / evaluation subset |

---

## Evaluation Metrics

HalluAudio includes several hallucination-oriented metrics:

| Metric | Description |
|---|---|
| Accuracy | Standard task correctness |
| Yes Prediction Ratio | Measures affirmative bias |
| Unrelated Error Ratio | Measures semantically unrelated responses |
| Conditional Accuracy | Accuracy conditioned on valid answer type |
| False Refusal Rate (FRR) | Measures over-conservative refusals |

---

## 🚀 Quick Start

### 1. Download Dataset

Download our dataset from [huggingface](https://huggingface.co/datasets/zhaozhao09/HalluAudio) and extract it to your data directory.

### 2. Test LALMs

Run inference using your LALM.

Example workflow:
```bash
for sample in dataset:

    audio = sample["audio"]
    prompt = sample["prompt"]

    prediction = model.generate(audio, prompt)

    save({
        "audio": audio,
        "prompt": prompt,
        "reference": sample["reference"],
        "pred": prediction,
        "subset": sample["subset"]
    })
```

The final prediction file should contain:

```bash
['audio', 'prompt', 'reference', 'pred', 'subset']
```

### 3. Clone Repository

```bash
git clone https://github.com/Feiyuzhao25/halluaudio.git
cd halluaudio
```

### 4. Calculate Indicators

Structured / classification-style Evaluation:

```bash
python accuracy_classify.py
```

Open-ended Evaluation:

```bash
python accuracy_else.py
```

Yes/No Bias Evaluation and Generate Visualization Figures:

```bash
python yesno_bias_test.py
python yesno_bias_figure.py
```

False Refusal Evaluation and Generate Visualization Figures:

```bash
python reject_group.py
```
---

# Citation

If you find HalluAudio useful, please consider citing our work.

```text
@article{zhao2026halluaudio,
  title={HalluAudio: A Comprehensive Benchmark for Hallucination Detection in Large Audio-Language Models},
  author={Zhao, Feiyu and Chen, Yiming and Lu, Wenhuan and Zhang, Daipeng and Yue, Xianghu and Wei, Jianguo},
  journal={arXiv preprint arXiv:2604.19300},
  year={2026}
}
```
