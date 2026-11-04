# Telugu Language Positional Index

## 1. Introduction

This implementation creates a **Positional Inverted Index for the Telugu language** using the Telugu Wikipedia dataset.

It supports single-term search and phrase search. For each term, it maintains collection frequency (CF), document frequency (DF), and positional postings containing document IDs, document titles, and term positions.

The vocabulary and its aggregate statistics are maintained in main memory during indexing, while the positional postings are stored on secondary storage using SQLite.

This work was developed as part of the Information Retrieval course assignment.

## 2. Complete Implementation and Dataset

The complete working implementation, including the Telugu Wikipedia dataset and the pre-built positional index, is available in the GitHub repository:

**GitHub Repository:** [Telugu-PosIndex](GITHUB_REPOSITORY_URL)

The dataset and complete index are provided through GitHub or a linked storage location for reference and verification, as permitted by the assignment instructions.

The dataset and complete index are not included in the final Google Form submission package, in accordance with the assignment instructions.

### Dataset Download

The Telugu Wikipedia dataset can also be downloaded from:

[Download Telugu Wikipedia Articles Dump](https://dumps.wikimedia.org/tewiki/latest/tewiki-latest-pages-articles.xml.bz2)

## 3. Directory Structure

```text
Telugu-PosIndex/
├── data/
│   └── raw/
│       └── tewiki-latest-pages-articles.xml.bz2
├── index/
│   └── positional_index.db
├── src/
│   ├── dataset_loader.py
│   ├── text_processor.py
│   ├── positional_index.py
│   ├── search.py
│   ├── generate_output.py
│   └── main.py
├── tests/
│   └── test_positional_index.py
├── output/
│   └── telugu_output.txt
├── requirements.txt
└── README.md
```

The `data/` directory contains the input dataset, and the `index/` directory contains the generated SQLite index. Both are excluded from the final assignment submission package.

## 4. Module Description

### `dataset_loader.py`
Loads and parses the Telugu Wikipedia XML dump and extracts article content.

### `text_processor.py`
Processes Telugu text, performs tokenization, and extracts Telugu terms.

### `positional_index.py`
Builds the positional inverted index. It maintains vocabulary statistics and stores positional postings in an SQLite database.

### `search.py`
Implements single-term search and phrase search using the positional index.

### `generate_output.py`
Generates the required output containing five search test cases and ten rare terms with their positional index details.

### `main.py`
Provides the main application interface for building the index and performing searches.

### `test_positional_index.py`
Contains unit tests to verify index statistics, term positions, and phrase-search functionality.

## 5. Requirements

- **Python 3:** Required to run the application. [Download Python](https://www.python.org/downloads/).
- **SQLite3:** Used for storing the positional index. The `sqlite3` module is included with Python.
- **lxml:** Required for parsing the Wikipedia XML dataset.

Install the required Python packages from the terminal:

```bash
pip install -r requirements.txt
```

This command installs the dependencies listed in `requirements.txt`, including `lxml`.

Verify Python installation:

```bash
python --version
```

## 6. How to Run

### Option 1: Run the Complete Implementation from GitHub

1. Clone or download the GitHub repository.
2. Ensure the dataset and pre-built index are available in their respective directories.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python src/main.py
   ```

The existing index can be used for searching without rebuilding it.

### Option 2: Build the Index from Scratch

If the dataset is not available locally:

1. Download the Telugu Wikipedia dataset using the link provided in Section 2.
2. Place the downloaded file at:

   ```text
   data/raw/tewiki-latest-pages-articles.xml.bz2
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python src/main.py
   ```

5. Select the index-building option and enter the number of articles to process.

If no number is entered, the program uses the default of 100 articles. This provides a smaller index for quick testing.

**Note:** The supplied output file, `output/telugu_output.txt`, was generated using 9,000 Wikipedia articles. Rebuilding the index with the default 100 articles creates a smaller testing index and will not reproduce the same output statistics.

## 7. Output

The generated output file is:

```text
output/telugu_output.txt
```

It contains:
- Five search test cases, including single-term and phrase searches.
- Ten rare Telugu terms with their collection frequency (CF), document frequency (DF), and positional postings.

The output was generated using an index built from 9,000 Telugu Wikipedia articles.

The complete positional index is not included in the final assignment submission, in accordance with the assignment instructions.

## 8. Testing

Run the unit tests using:

```bash
python -m unittest discover -s tests -v
```

The tests verify positional indexing, CF and DF statistics, and phrase-search behavior.

## 9. Storage Architecture

The implementation follows the storage requirements of the assignment:
- **Main Memory:** The vocabulary and aggregate collection statistics are maintained using a Python dictionary during indexing.
- **Secondary Storage:** Positional postings are stored in an SQLite database.
- **Index Metadata:** The index maintains terms, positional postings, collection frequency (CF), and document frequency (DF).

The dataset and complete index are available through the GitHub repository or linked storage location for verification. They are excluded from the final Google Form submission package, as required by the assignment instructions.