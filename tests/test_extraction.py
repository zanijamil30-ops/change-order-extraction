
import json
import pytest

from src.extractor import (
    read_document,
    extract_information,
    process_document
)

from src.validator import validate_extraction


# --------------------------------------------
# TEST 1: DOCUMENT READING
# --------------------------------------------

def test_read_sample_document():

    text = read_document(
        "data/sample_change_order.txt"
    )

    assert "CO-102" in text
    assert "ABC Construction Ltd." in text


# --------------------------------------------
# TEST 2: CHANGE ORDER NUMBER EXTRACTION
# --------------------------------------------

def test_extract_change_order_number():

    text = """
    Change Order Number: CO-102
    """

    result = extract_information(text)

    assert (
        result["change_order_number"]["value"]
        == "CO-102"
    )


# --------------------------------------------
# TEST 3: MONETARY VALUE EXTRACTION
# --------------------------------------------

def test_extract_monetary_values():

    text = """
    Change Amount: $3,000.00
    """

    result = extract_information(text)

    assert result["change_amount"]["value"] == 3000.0


# --------------------------------------------
# TEST 4: CONFIDENCE SCORE
# --------------------------------------------

def test_confidence_score():

    text = """
    Project Name: Office Renovation Project
    """

    result = extract_information(text)

    confidence = result["project_name"]["confidence"]

    assert 0.0 <= confidence <= 1.0

    assert confidence > 0


# --------------------------------------------
# TEST 5: MISSING FIELD DETECTION
# --------------------------------------------

def test_missing_fields():

    text = """
    Project Name: Office Renovation Project
    """

    result = extract_information(text)

    assert result["contractor"]["value"] is None

    assert result["change_amount"]["value"] is None


# --------------------------------------------
# TEST 6: FINANCIAL VALIDATION
# --------------------------------------------

def test_contract_amount_validation():

    data = extract_information("""
    Change Order Number: CO-102
    Original Contract Amount: $50,000
    Change Amount: $3,000
    Revised Contract Amount: $60,000
    """)

    result = validate_extraction(data)

    assert (
        result["validation_status"]
        == "review_required"
    )

    assert len(result["validation_warnings"]) > 0


# --------------------------------------------
# TEST 7: COMPLETE EXTRACTION PIPELINE
# --------------------------------------------

def test_complete_pipeline(tmp_path):

    output_file = tmp_path / "result.json"

    result = process_document(
        "data/sample_change_order.txt",
        str(output_file)
    )

    assert output_file.exists()

    assert (
        result["change_order_number"]["value"]
        == "CO-102"
    )

    assert (
        result["validation_status"]
        == "passed"
    )

    # Verify that generated JSON is readable.
    with open(output_file, "r", encoding="utf-8") as file:

        saved_data = json.load(file)

    assert saved_data["change_amount"]["value"] == 3000.0


# --------------------------------------------
# TEST 8: UNSUPPORTED FILE FORMAT
# --------------------------------------------

def test_unsupported_file_format(tmp_path):

    invalid_file = tmp_path / "document.docx"

    invalid_file.write_text(
        "Invalid document format"
    )

    with pytest.raises(ValueError):

        read_document(str(invalid_file))


# --------------------------------------------
# TEST 9: EMPTY DOCUMENT HANDLING
# --------------------------------------------

def test_empty_document(tmp_path):

    empty_file = tmp_path / "empty.txt"

    empty_file.write_text("")

    with pytest.raises(ValueError):

        process_document(
            str(empty_file),
            str(tmp_path / "output.json")
        )

