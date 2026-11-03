"""
Main Change Order Extraction Pipeline.

Supports:
- PDF document reading
- Plain-text document reading
- Label-based information extraction
- Monetary value normalization
- Field-level confidence scoring
- Structured data validation
- JSON output generation
"""

import argparse
import json
import re

from pathlib import Path
from pypdf import PdfReader

from src.confidence import create_field
from src.validator import validate_extraction


# --------------------------------------------------
# 1. FIELD DEFINITIONS
# --------------------------------------------------

FIELD_LABELS = {

    "change_order_number": [
        r"change\s*order\s*(?:number|no\.?|#)"
    ],

    "project_name": [
        r"project\s*name",
        r"project"
    ],

    "contractor": [
        r"contractor",
        r"company"
    ],

    "change_date": [
        r"change\s*order\s*date",
        r"date"
    ],

    "change_description": [
        r"change\s*description",
        r"description",
        r"scope\s*of\s*work"
    ],

    "change_amount": [
        r"change\s*amount",
        r"additional\s*cost",
        r"total\s*change"
    ],

    "original_contract_amount": [
        r"original\s*contract\s*amount",
        r"original\s*contract\s*value"
    ],

    "revised_contract_amount": [
        r"revised\s*contract\s*amount",
        r"new\s*contract\s*amount",
        r"revised\s*contract\s*value"
    ]
}


MONETARY_FIELDS = {
    "change_amount",
    "original_contract_amount",
    "revised_contract_amount"
}


# --------------------------------------------------
# 2. DOCUMENT READING
# --------------------------------------------------

def read_document(file_path):
    """Read text from PDF or TXT documents."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".txt":

        return path.read_text(encoding="utf-8")

    elif extension == ".pdf":

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:

            pages.append(
                page.extract_text() or ""
            )

        return "\n".join(pages)

    else:

        raise ValueError(
            "Unsupported format. Please provide PDF or TXT."
        )


# --------------------------------------------------
# 3. IDENTIFY FIELD LABELS
# --------------------------------------------------

def identify_field_label(line):
    """Identify whether a line contains a known field label."""

    for field_name, patterns in FIELD_LABELS.items():

        for pattern in patterns:

            match = re.match(
                rf"^\s*{pattern}\s*[:\-]\s*(.*)$",
                line,
                flags=re.IGNORECASE
            )

            if match:

                return field_name, match.group(1).strip()

    return None, None


# --------------------------------------------------
# 4. EXTRACT FIELD VALUES
# --------------------------------------------------

def extract_labelled_value(text, field_name):
    """
    Extract a labelled value and its supporting evidence.

    Supports descriptions extending across multiple lines.
    """

    lines = text.splitlines()

    for index, line in enumerate(lines):

        detected_field, initial_value = identify_field_label(line)

        if detected_field != field_name:
            continue

        extracted_parts = []

        if initial_value:
            extracted_parts.append(initial_value)

        # Capture continuation lines.
        for next_line in lines[index + 1:]:

            cleaned_line = next_line.strip()

            if not cleaned_line:
                break

            next_field, _ = identify_field_label(cleaned_line)

            if next_field:
                break

            extracted_parts.append(cleaned_line)

        value = " ".join(extracted_parts).strip()

        evidence = line.strip()

        return value if value else None, evidence

    return None, None


# --------------------------------------------------
# 5. NORMALIZE MONETARY VALUES
# --------------------------------------------------

def parse_amount(value):
    """Convert monetary text into a numeric value."""

    if not value:
        return None

    cleaned = re.sub(
        r"[$£€,\s]",
        "",
        value
    )

    negative = (
        cleaned.startswith("(")
        and cleaned.endswith(")")
    )

    cleaned = cleaned.strip("()")

    try:

        amount = float(cleaned)

        return -amount if negative else amount

    except ValueError:

        return None


# --------------------------------------------------
# 6. EXTRACT DOCUMENT INFORMATION
# --------------------------------------------------

def extract_information(text):

    extracted = {}

    for field_name in FIELD_LABELS:

        raw_value, evidence = extract_labelled_value(
            text,
            field_name
        )

        validated = False

        if field_name in MONETARY_FIELDS:

            value = parse_amount(raw_value)

            validated = (
                value is not None
                and value >= 0
            )

        else:

            value = raw_value

            if value:

                validated = len(value.strip()) >= 3

        extracted[field_name] = create_field(
            value=value,
            evidence=evidence,
            explicitly_labelled=evidence is not None,
            validated=validated
        )

    return extracted


# --------------------------------------------------
# 7. COMPLETE EXTRACTION PIPELINE
# --------------------------------------------------

def process_document(input_file, output_file):

    print("\nStarting Change Order Extraction Pipeline")

    # Read input document.
    document_text = read_document(input_file)

    if not document_text.strip():

        raise ValueError(
            "No readable text found. "
            "The document may require OCR processing."
        )

    print("[1/4] Document reading completed.")

    # Extract information.
    extracted_data = extract_information(document_text)

    print("[2/4] Information extraction completed.")

    # Validate information.
    validated_data = validate_extraction(extracted_data)

    print("[3/4] Data validation completed.")

    # Generate JSON output.
    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as output:

        json.dump(
            validated_data,
            output,
            indent=4,
            ensure_ascii=False
        )

    print("[4/4] JSON generation completed.")

    print(f"\nOutput saved to: {output_path}")

    print(
        f"Validation status: "
        f"{validated_data['validation_status']}"
    )

    return validated_data


# --------------------------------------------------
# 8. COMMAND LINE INTERFACE
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Construction Change Order Extraction"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input PDF or TXT document"
    )

    parser.add_argument(
        "--output",
        default="output/extracted.json",
        help="Output JSON file path"
    )

    args = parser.parse_args()

    try:

        result = process_document(
            input_file=args.input,
            output_file=args.output
        )

        print("\nExtraction completed successfully.")

    except Exception as error:

        print(f"\nExtraction failed: {error}")

        raise SystemExit(1)


if __name__ == "__main__":

    main()
