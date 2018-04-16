# OpenSesamIE

This is a simple approach to open information extraction (OpenIE) using the SpacyIO dependency parser. It accepts a text file and outputs a tab-delimited set of subj-predicate-obj triples. Over a large corpus of text, frequent patterns of relations can be identified between different entities.

## Installation

This tool requires Python3 with Spacy installed. The English language data files for Spacy also need to be installed.

```
pip install spacy
python -m spacy download en
```

## Usage

The usage is below. Input is a plain-text file and output is a tab-delimited file.

```
python opensesamie.py --in doc.txt --out relations.tsv
```

## PubRunner

This tool is integrated with PubRunner so it can be executed on a large corpus (e.g. PubMed).

To run the test case (with PubRunner installed):
```
pubrunner --test .
```

And to run across PubMed and PMCOA entirely (which could take a long time):
```
pubrunner .
```
