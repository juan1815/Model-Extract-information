# Model-Extract-information: Extracting Project Information from A3 Gaceta PDFs

This project uses Python to extract information (projects, entities, dates, etc.) from A3-sized PDF "Gacetas" containing project details.  These Gacetas span the years 2000-2025 and may have varying structural formats.  We leverage pre-trained open-source models and tools.

**Project Goals:**

* Develop a robust and accurate model for extracting key information from Gaceta PDFs.
* Handle variations in document structure across different Gaceta files.
* Extract information relevant to projects within the 2000-2025 timeframe.

**Technical Approach:**

* **Programming Language:** Python
* **Libraries:**  We'll utilize libraries like `transformers`, `torch`, `spaCy`, and regular expressions (`re`).  Specific model choices (e.g., BERT, RoBERTa) will be determined based on performance and suitability.
* **PDF Processing:**  A library like `PyPDF2`, `tika`, or `camelot` will be used to handle PDF parsing and text extraction.  Consideration will be given to handling scanned documents (OCR).
* **Named Entity Recognition (NER):** spaCy's `es_core_news_sm` model will be a starting point for NER, potentially augmented with custom training or other advanced NER models depending on the data characteristics.
* **Date Extraction:** Regular expressions and potentially dedicated date parsing libraries will be employed.
* **Model Training:**  We will likely fine-tune a pre-trained language model on a labeled dataset of Gaceta extracts. (Dataset creation details are in a separate document).


**Project Setup:**

This project uses a conda environment for dependency management.

1. **Create conda environment:**
   ```bash
   conda create -n extraction python=3.9  # Specify Python version; 3.9 recommended.
   ```
2. **Activate enviroment:**
    ```bash
     conda activate extraction
    ```
3. **Installl libraries:**
    ```bash
    conda install -c conda-forge transformers torch pytorch-lightning  # Use conda for optimal package management; including pytorch-lightning is recommended for better model training workflows.
    ```
    ```bash
python -m spacy download es_core_news_sm
conda install -c conda-forge pypdf2  #Or another PDF processing library as needed.
    ```
   
