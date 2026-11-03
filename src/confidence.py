"""
Confidence scoring module.

Calculates heuristic confidence scores using:
- Extracted value availability
- Supporting document evidence
- Explicit field labels
- Basic value validation

Scores are heuristic indicators, not calibrated probabilities.
"""


def calculate_confidence(
    value,
    evidence=None,
    explicitly_labelled=False,
    validated=False
):
    """Calculate an evidence-based heuristic confidence score."""

    if value is None or str(value).strip() == "":
        return 0.0

    score = 0.40

    if evidence:
        score += 0.20

    if explicitly_labelled:
        score += 0.20

    if validated:
        score += 0.10

    return round(min(score, 0.90), 2)


def create_field(
    value=None,
    evidence=None,
    explicitly_labelled=False,
    validated=False
):
    """Create a standard extracted-field structure."""

    return {
        "value": value,
        "confidence": calculate_confidence(
            value=value,
            evidence=evidence,
            explicitly_labelled=explicitly_labelled,
            validated=validated
        ),
        "evidence": evidence
    }
