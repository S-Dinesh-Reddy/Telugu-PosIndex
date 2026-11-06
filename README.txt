TELUGU LANGUAGE POSITIONAL INDEX (Telugu-PosIndex)
=================================================

1. INTRODUCTION
---------------

Telugu Language Positional Index is an Information Retrieval system 
developed to build a positional index for Telugu Wikipedia articles and 
support term-based and phrase-based searching. Unlike a normal inverted index 
that records only the documents containing a term, a positional index stores 
the exact positions of terms within each document. This positional information 
enables phrase searching by verifying whether the query terms occur consecutively 
and in the specified order. As a result, the system can retrieve documents containing
an exact phrase rather than merely documents containing all the individual query terms.

For every term, the index stores its Collection Frequency (CF), Document Frequency (DF),
and the positions at which it occurs in each document. These positional entries are used
to perform phrase searches by checking whether consecutive query terms appear at adjacent positions
and in the correct order. This allows the system to identify documents containing the exact phrase
without maintaining a separate index for every possible phrase.

The system is implemented in Python. The vocabulary and term
statistics are maintained in main memory, while the postings lists
are stored in SQLite on secondary storage.

It supports searching for individual Telugu words, searching for
Telugu phrases, and retrieving the positional information of terms
within documents.


2. DATASET
----------

The system uses the Telugu Wikipedia articles dump.

Dataset:
Telugu Wikipedia pages-articles XML dump

Dataset file:
data/raw/tewiki-latest-pages-articles.xml.bz2

The XML dump is parsed article by article to avoid loading the entire
dataset into memory.

The pre-built positional index and the generated output were created
using 9,000 Telugu Wikipedia articles.

The dataset and the pre-built positional index are large files and are
not included in the source code ZIP because of their large size.
However both are included in the Github Repository. The Repository link and 
the direct dataset download link are provided in Section 11 at the end of this README.


3. REQUIREMENTS AND SETUP
-------------------------

Requirements:
- Python 3
- Required Python packages listed in requirements.txt

Install the required packages from the root directory:

    py -m pip install -r requirements.txt

Note:
On my Windows system, the 'python' command was not recognized in
PowerShell. The Python launcher 'py' works, so the commands below
use 'py'.


TYPING TELUGU TEXT FOR SEARCH
---------------------------------
The program supports searching for Telugu words and phrases. Users can enter Telugu text using a 
Telugu keyboard or an online Telugu transliteration tool.

Method 1: Using Telugu Transliteration
1. Open an online Telugu transliteration tool, such as Google Input Tools.
2. Select Telugu as the input language.
3. Type the required word using English letters. For example, typing "namaskaram" may produce "నమస్కారం".
4. Copy the Telugu text and paste it into the program's search prompt.

Method 2: Using the Telugu Keyboard in Windows
1. Open Settings → Time & Language → Language & Region.
2. Add Telugu as a language and install its keyboard.
3. Switch to the Telugu keyboard using Win + Space.
4. Type the required Telugu word or phrase in the terminal.

In this way, you can type Telugu words directly using a Telugu keyboard or an online Telugu transliteration tool.


4. RUNNING THE PROGRAM
----------------------

Run the main program from the root directory:

    py src/main.py

The program displays the following menu:

    ===== Telugu Language Positional Index =====
    1. Build positional index
    2. Search for a word
    3. Search for a phrase
    4. Exit


Option 1: Build positional index
--------------------------------

This option builds the positional index from the Telugu Wikipedia
XML dump.

The program asks how many articles should be indexed. Press Enter
to use the default value of 100 articles, or enter a different
number.

The generated index is stored in:

    index/positional_index.db

Note:
The pre-built index and benchmark output in
output/telugu_output.txt were generated using 9,000 articles.

The default value of 100 articles is intended for quick testing
and demonstrations. Rebuilding the index will replace the existing
database. Do not rebuild it unless you intend to replace the
current index.


Option 2: Search for a word
---------------------------

This option allows the user to search for an individual Telugu word.

The program asks the user to enter a Telugu word.

If the term exists in the index, the program displays:
- The searched term
- Collection Frequency (CF)
- Document Frequency (DF)
- Matching document titles
- Document IDs
- Positions of the term in each document

If the term is not found, the program displays a message indicating
that the term is not present in the index.


Option 3: Search for a phrase
-----------------------------

This option allows the user to search for a Telugu phrase.

The program asks the user to enter a Telugu phrase.

The phrase is tokenized, and the positional index is used to check
whether the terms occur consecutively and in the same order.

For every matching document, the program displays:
- Document title
- Document ID
- Starting position of the phrase

If no matching phrase is found, the program displays a message.


Option 4: Exit
--------------

This option exits the program.


5. INDEXING AND STORAGE
-----------------------

The positional index is built using the following approach:

1. Telugu Wikipedia articles are loaded from the XML dump.
2. The article text is processed and tokenized.
3. Each term is assigned its position within the document.
4. Collection Frequency (CF) and Document Frequency (DF) are maintained.
5. The vocabulary and term statistics are maintained in main memory.
6. The postings lists are written to SQLite, which acts as
   secondary storage.

Main Memory:
------------

The vocabulary is maintained using a Python dictionary during
indexing. It stores the terms along with their collection frequency,
document frequency, and related indexing information.

Secondary Storage:
------------------

The postings lists are stored in an SQLite database:

    index/positional_index.db

The postings are written to the database document by document
instead of keeping all postings in memory.

This helps reduce memory usage while indexing a large collection.


6. POSITIONAL INDEX AND PHRASE SEARCHING
----------------------------------------

A positional index stores the positions of each term within a
document.

The index uses zero-based token positions, meaning the first token
in a document is assigned position 0.

For example, if a term occurs at positions 4, 10, and 18 in a
document, its positional information is stored as:

    [4, 10, 18]

The positions are useful for phrase searching.

For a phrase such as:

    తెలుగు సాహిత్యం

the system checks whether the position of the second term is exactly
one greater than the position of the first term.

This ensures that the terms occur consecutively and in the correct
order.

The positional information also helps distinguish between documents
where the individual terms occur but do not form the required phrase.


7. OUTPUT
---------

The generated output file is:

    output/telugu_output.txt

It contains:

- Five search test cases
- Three individual term queries
- Two phrase queries
- Ten rare Telugu terms
- Collection Frequency (CF)
- Document Frequency (DF)
- Matching document titles and IDs
- Positional information for the terms
- Starting positions for matching phrases

The rare-term section provides the positional index entries for the
selected terms, including their matching documents and positions.

To generate the output file, run:

    py src/generate_output.py

The output is written to:

    output/telugu_output.txt

The output file is regenerated when this command is executed.


8. RUNNING UNIT TESTS
---------------------

The system includes unit tests to verify the positional index and
search functionality.

The tests cover:
- Term positions
- Collection Frequency (CF)
- Document Frequency (DF)
- Phrase searching
- Phrases with no matching documents

Run the unit tests from the root directory using:

    py -m unittest discover -s tests -v


9. MODULES
----------

The following modules are included:

src/dataset_loader.py
---------------------
Loads Telugu Wikipedia articles from the XML dump using iterative
parsing.

src/text_processor.py
--------------------
Processes the article text and tokenizes Telugu content for
indexing and searching.

src/positional_index.py
----------------------
Builds the positional index. It maintains the vocabulary and term
statistics in memory and stores the postings lists in SQLite.

src/search.py
-------------
Implements individual term searching and phrase searching using
the positional index.

src/main.py
-----------
Provides the main menu and allows the user to build the index,
search for terms, search for phrases, or exit.

src/generate_output.py
----------------------
Generates the required output file containing search test cases
and rare-term positional index entries.

tests/test_positional_index.py
------------------------------
Contains unit tests for verifying the positional indexing and
search functionality.


10. DIRECTORY STRUCTURE
-----------------------

Telugu-PosIndex/
|
|-- src/
|   |-- main.py
|   |-- dataset_loader.py
|   |-- text_processor.py
|   |-- positional_index.py
|   |-- search.py
|   |-- generate_output.py
|
|-- tests/
|   |-- test_positional_index.py
|
|-- data/
|   |-- raw/
|       |-- tewiki-latest-pages-articles.xml.bz2
|
|-- index/
|   |-- positional_index.db
|
|-- output/
|   |-- telugu_output.txt
|
|-- requirements.txt
|-- README.txt
|-- .gitignore
|-- .gitattributes


11. DATASET AND INDEX LINKS
---------------------------

Source Code Repository:
https://github.com/S-Dinesh-Reddy/Telugu-PosIndex

Telugu Language Wikipedia Dataset (Direct Download):
https://dumps.wikimedia.org/tewiki/latest/tewiki-latest-pages-articles.xml.bz2

The complete dataset and the pre-built positional index are available in the GitHub repository.
The dataset can also be downloaded directly from Wikimedia using the link provided above.
The pre-built index can be used to run search queries without rebuilding the index.