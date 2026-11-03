# change-order-extraction
AI-powered construction change-order extraction pipeline
# Change Order Extraction Pipeline

**An Automated Document Processing and Structured Information Extraction System for Construction Change Orders**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Validation-Pydantic-green)](https://docs.pydantic.dev/)
[![Testing](https://img.shields.io/badge/Testing-Pytest-orange)](https://pytest.org/)
[![Status](https://img.shields.io/badge/Project-Prototype-informational)]()

## 1. Project Overview

The Change Order Extraction Pipeline is a Python-based document-processing application designed to extract structured information from construction change-order documents and convert it into validated JSON.

Construction projects frequently generate change orders containing modifications to contractual scope, costs, project schedules and responsibilities. These documents may contain inconsistent formatting, lengthy descriptions and important financial information.

Manually reviewing these documents can be time-consuming and may introduce data-entry errors.

This project addresses this challenge through an automated extraction pipeline that reads PDF and plain-text documents, identifies important contractual information, assigns field-level confidence scores and validates the resulting data before generating structured JSON.

The system is designed around modular components, transparent extraction evidence and explicit validation rules.

## 2. Project Objectives

The primary objectives are to:

- Automate the extraction of important information from construction change-order documents.
- Support PDF and plain-text input formats.
- Convert unstructured document content into structured JSON.
- Generate confidence scores for individual extracted fields.
- Validate extracted information using structured data models.
- Identify missing information and financial inconsistencies.
- Provide evidence showing where extracted values originated.
- Identify extraction limitations and opportunities for future AI integration.

## 3. Key Features

| Feature | Description |
|---|---|
| PDF Processing | Extracts machine-readable text from PDF documents. |
| Text Processing | Processes plain-text change-order documents. |
| Information Extraction | Identifies eight important change-order fields. |
| Confidence Scoring | Assigns individual heuristic confidence scores. |
| Evidence Tracking | Retains supporting document text for extracted values. |
| Data Validation | Uses Pydantic to validate the output structure. |
| Financial Verification | Checks contract amount consistency. |
| Missing-Field Detection | Identifies information that could not be extracted. |
| JSON Generation | Produces structured machine-readable output. |
| Automated Testing | Uses Pytest to test extraction and validation functionality. |

## 4. System Architecture

The application follows a modular pipeline architecture in which each component performs a specific processing responsibility.

```text
             INPUT DOCUMENT
              PDF / TXT
                  |
                  v
          DOCUMENT READER
                  |
                  v
         TEXT PREPROCESSING
                  |
                  v
       INFORMATION EXTRACTION
                  |
                  v
          CONFIDENCE SCORING
                  |
                  v
          DATA VALIDATION
                  |
                  v
       FINANCIAL CONSISTENCY
               CHECKS
                  |
                  v
           JSON GENERATION
                  |
                  v
          STRUCTURED OUTPUT
```

### Component Responsibilities

**1. Document Reader**

The document reader accepts PDF and TXT files. It extracts readable text and provides it to the extraction component.

**2. Information Extractor**

The extraction component uses regular expressions and predefined field labels to identify relevant information, including monetary values and multiline descriptions.

**3. Confidence Scoring**

The confidence module evaluates extracted values using evidence availability, explicit field labels and basic validation indicators.

**4. Data Validator**

The validation module uses Pydantic to enforce the expected data structure and confidence-score boundaries.

**5. Financial Consistency Checker**

The application checks whether the original contract amount plus the change amount equals the revised contract amount.

**6. JSON Generator**

The final component exports the validated information into a structured JSON file.

## 5. Information Extracted

The pipeline currently extracts eight fields:

| Field | Example |
|---|---|
| Change Order Number | CO-102 |
| Project Name | Office Renovation Project |
| Contractor | ABC Construction Ltd. |
| Change Date | 15 October 2026 |
| Change Description | Additional electrical installation |
| Change Amount | 3000.00 |
| Original Contract Amount | 50000.00 |
| Revised Contract Amount | 53000.00 |

Each field contains three properties:

- `value`: The extracted information.
- `confidence`: A heuristic confidence score between 0 and 1.
- `evidence`: Supporting text from the source document.

## 6. Confidence Scoring Methodology

A field-level confidence scoring mechanism is implemented to communicate the reliability of individual extraction results.

The current scoring model considers four indicators:

| Indicator | Score |
|---|---:|
| Extracted value is present | 0.40 |
| Supporting evidence is available | 0.20 |
| Explicit field label is identified | 0.20 |
| Basic validation succeeds | 0.10 |
| Maximum score | 0.90 |

The scoring mechanism is heuristic rather than statistically calibrated. Therefore, a high score indicates that the extraction satisfies the implemented evidence and validation checks, not that the value has a verified probability of being correct.

Future development will introduce an annotated evaluation dataset to measure extraction accuracy and calibrate confidence scores against observed performance.

## 7. Data Validation Strategy

Data validation is an essential component because incorrectly extracted contractual information could affect financial reporting and construction decisions.

Pydantic is used to enforce the expected field structure and ensure that confidence scores remain within the permitted range.

Additional business rules identify missing fields and financial inconsistencies.

The financial validation rule is:

**Original Contract Amount + Change Amount = Revised Contract Amount**

For example:

```text
Original Contract Amount = $50,000
Change Amount            = $3,000
Revised Contract Amount  = $53,000

Validation Result: PASSED
```

If the revised contract amount does not match the calculated amount, the system generates a validation warning and marks the record for review.

Missing values are also reported rather than silently treated as successfully extracted information.

## 8. Technology Stack

| Technology | Application |
|---|---|
| Python | Core application development |
| PyPDF | PDF text extraction |
| Regular Expressions | Field identification and text extraction |
| Pydantic | Data structure and type validation |
| JSON | Structured output |
| Pytest | Automated testing |
| GitHub | Source-code management and project documentation |

The current implementation uses deterministic, rule-based extraction. It does not yet use an LLM or machine-learning model.

## 9. Repository Structure

```text
change-order-extraction/
│
├── data/
│   ├── sample_change_order.pdf
│   └── sample_change_order.txt
│
├── src/
│   ├── extractor.py
│   ├── validator.py
│   └── confidence.py
│
├── output/
│   └── extracted.json
│
├── tests/
│   └── test_extraction.py
│
├── requirements.txt
└── README.md
```

## 10. Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Git.
- A terminal or command-line environment.

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/change-order-extraction.git
```

### Step 2: Navigate to the Project

```bash
cd change-order-extraction
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## 11. Running the Application

The application accepts both PDF and TXT input documents.

### Process a TXT Document

```bash
python -m src.extractor --input data/sample_change_order.txt
```

### Process a PDF Document

```bash
python -m src.extractor --input data/sample_change_order.pdf
```

### Specify a Custom Output Location

```bash
python -m src.extractor --input data/sample_change_order.txt --output output/custom_result.json
```

By default, the generated JSON is saved to:

```text
output/extracted.json
```

## 12. Example JSON Output

The following illustrates the expected structure of an extracted change-order record:

```json
{
  "change_order_number": {
    "value": "CO-102",
    "confidence": 0.9,
    "evidence": "Change Order Number: CO-102"
  },
  "project_name": {
    "value": "Office Renovation Project",
    "confidence": 0.9,
    "evidence": "Project Name: Office Renovation Project"
  },
  "contractor": {
    "value": "ABC Construction Ltd.",
    "confidence": 0.9,
    "evidence": "Contractor: ABC Construction Ltd."
  },
  "change_amount": {
    "value": 3000.0,
    "confidence": 0.9,
    "evidence": "Change Amount: $3,000.00"
  },
  "original_contract_amount": {
    "value": 50000.0,
    "confidence": 0.9,
    "evidence": "Original Contract Amount: $50,000.00"
  },
  "revised_contract_amount": {
    "value": 53000.0,
    "confidence": 0.9,
    "evidence": "Revised Contract Amount: $53,000.00"
  },
  "validation_warnings": [],
  "validation_status": "passed"
}
```

*Note: This is an illustrative output showing the expected structure. The complete generated output also includes the remaining extracted fields.*

## 13. Testing and Quality Assurance

Automated testing is implemented using Pytest.

The test suite covers:

- Successful document reading.
- Change-order number extraction.
- Monetary value extraction.
- Confidence-score generation.
- Missing-field identification.
- Financial inconsistency detection.
- Complete extraction pipeline execution.
- Unsupported document formats.
- Empty document handling.

Run the tests using:

```bash
pytest -v
```

The tests should be executed in a Python environment before reporting successful test results.

## 14. Failure Modes and Limitations

The system is designed with transparent limitations. Identifying these limitations is important because construction documents can contain ambiguous information and financially significant errors.

### 14.1 Scanned PDF Documents

The current PDF reader extracts machine-readable text. Scanned documents containing images may not produce readable text.

**Mitigation:** Integrate OCR technology such as Tesseract or a cloud-based document recognition service.

### 14.2 Inconsistent Document Formatting

The extraction engine relies on predefined labels. Unusual terminology or alternative document layouts may prevent accurate field identification.

**Mitigation:** Introduce flexible label recognition, document classification and LLM-based extraction.

### 14.3 Multiline and Complex Descriptions

Although the current implementation supports basic multiline descriptions, complex layouts, tables and irregular paragraph structures may affect extraction boundaries.

**Mitigation:** Introduce layout-aware PDF processing and structured document segmentation.

### 14.4 Handwritten Information

The current system is not designed to interpret handwritten amendments, notes or signatures.

**Mitigation:** Integrate handwriting recognition and human verification.

### 14.5 Financial Inconsistencies

The application checks arithmetic relationships but cannot independently establish whether the original figures are contractually correct.

**Mitigation:** Introduce additional business rules, approval checks and human review.

### 14.6 Confidence Calibration

The current confidence scores are heuristic indicators. They should not be interpreted as statistically verified probabilities.

**Mitigation:** Evaluate the system against manually annotated documents and calibrate confidence using observed extraction performance.

### 14.7 Ambiguous or Missing Information

Documents may contain conflicting values or omit important contractual details.

**Mitigation:** Flag uncertain records for manual review rather than automatically accepting incomplete results.

## 15. Future Development

The project provides a foundation for a more advanced AI-driven document extraction solution.

Potential enhancements include:

1. **OCR Integration:** Support scanned construction documents.
2. **LLM-Based Extraction:** Identify information from unstructured and inconsistent documents.
3. **Semantic Field Recognition:** Recognise alternative terminology and contextual relationships.
4. **Advanced Confidence Calibration:** Measure extraction reliability using labelled datasets.
5. **Human-in-the-Loop Review:** Allow users to verify uncertain fields before approval.
6. **Advanced Financial Validation:** Introduce more comprehensive contractual and financial rules.
7. **Evaluation Framework:** Measure field-level precision, recall and F1-score.
8. **API Integration:** Expose extraction functionality through a REST API.

## 16. Conclusion

The Change Order Extraction Pipeline demonstrates a modular approach to automating the extraction of contractual information from construction documents.

By combining PDF and text processing, evidence-based field extraction, heuristic confidence scoring and structured validation, the application converts document content into machine-readable JSON.

The implementation establishes a transparent baseline that can be evaluated, tested and extended.

Its modular architecture also provides a practical foundation for introducing advanced AI models, OCR capabilities and human verification workflows.

---

**Project:** Change Order Extraction Pipeline  
**Purpose:** AI Engineer Recruitment Technical Assessment  
**Language:** Python  
**Output:** Validated JSON with field-level confidence scores
