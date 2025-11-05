# Contrastive Analysis of Constituent Order Preferences Within Adverbial Roles in English and Chinese News: A Large-Language-Model-Driven Approach

[![arXiv](https://img.shields.io/badge/arXiv-2508.06110-b31b1b.svg)](https://arxiv.org/abs/2508.14054)

## Data Sources

The research utilizes the following corpora:

- ToRCH2019 Modern Chinese Balanced Corpus (李佳蕾、孫銘辰、許家金，2022，ToRCH2019現代漢語平衡語料庫。北京外國語大學中國外語與教育研究中心)
- The CROWN2021 Corpus (Mingchen Sun, Jiajin Xu et al. 2022. National Research Centre for Foreign Language Education, Beijing Foreign Studies University)

## Repository Overview

The research paper is available in the `paper` directory, presented in both Chinese (original) and English (translated version). The English translation aims to provide accessibility to non-Chinese speakers while maintaining the core academic content.

## Components

The analysis was implemented through three main modules:

### 1. Annotation Module
- Utilizes GPT-4o for automated functional block annotation
- Implements robust sentence splitting with handling for abbreviations and special cases
- Processes both English and Chinese corpora in batches for efficiency
- Includes quality control measures through post-processing scripts

### 2. Statistical Analysis Module
- Analyzes three main research questions:
  - Q1: Distribution preferences of functional blocks
  - Q2: Patterns in SVO-functional block combinations
  - Q3: Multiple functional block ordering patterns
- Employs chi-square tests and t-tests for significance testing
- Utilizes conditional probability matrices for transition analysis

### 3. Semantic Analysis Module
- Uses MiniCPM-Embedding model for semantic feature extraction
- Implements dimensionality reduction through t-SNE
- Analyzes semantic similarities between functional blocks
- Explores semantic influence on word order preferences

## Setup

1. Create and activate a conda environment:
```bash
conda create -n constituent_order python=3.11
conda activate constituent_order
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```


## Usage

### Data Annotation & Processing
1. Configure OpenAI API key in `.env`
2. Run annotation scripts:
```python
python annotation/anno_en.py  # English corpus
python annotation/anno_ch.py  # Chinese corpus
```
3. Post-process and extract patterns:
```python
python annotation/post_ch.py  # Process Chinese annotations
python annotation/post_en.py  # Process English annotations
python annotation/extract.py  # Extract abstract patterns
python analysis/relative_position.py  # Convert to relative positions

# Then mannually copy-paste the terminal output to /analysis/ch.txt or en.txt (hereafter referred to as relative position files)
```

> Refer to `demo` directory for more detailed examples.

### Analysis Pipeline
1. **Q1: Distribution preferences**
```python
python analysis/histogram.py  # Distribution visualization
python analysis/chi.py  # Statistical tests for intralingual comparison
python analysis/t_test.py  # Statistical tests for interlingual comparison
```
- Input: Relative position files
- Output: Relative position distributions, statistical test results

2. **Q2: SVO-functional block patterns**
```python
python analysis/Q2/count_and_patterns/
```
- Input: Relative position files
- Output: Pattern frequencies, conditional probability

3. **Q3: Multiple block ordering**
```python
python analysis/markov.py  # Transition probability calculation
python analysis/heatmap.py  # Visualization
```
- Input: Relative position files
- Output: Transition matrices, combination patterns

4. **Semantic Analysis**
```python
# Q1: Compare overall corpus semantics and time-SVO vs. SVO-time patterns
python analysis/semantics/1/embed.py  # Generate embeddings
python analysis/semantics/1/1.py  # Calculate and visualize

# Q2: Compare functional block semantics between languages
python analysis/semantics/2/embed.py  # Generate embeddings
python analysis/semantics/2/2.py  # Calculate and visualize
```
- Input: Relative position files
- Output: Semantic similarity matrices, visualization plots


## Contact

For inquiries regarding code implementation or research reproduction, please contact the author via email. Contact information is available on my [personal website](https://rexera.github.io/about/).

## Citation

If you find this research or codeuseful for your work, feel free to star this repository. If ultimately necessary, contact me for proper citation information for this toy project for a course paper. :)
