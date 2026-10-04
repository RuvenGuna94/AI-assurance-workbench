import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "export_garak_review.py"
SPEC = importlib.util.spec_from_file_location("export_garak_review", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
export_garak_review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(export_garak_review)

MAX_EXCEL_CELL_LENGTH = export_garak_review.MAX_EXCEL_CELL_LENGTH
parse_sources = export_garak_review.parse_sources
read_jsonl = export_garak_review.read_jsonl
safe_excel_text = export_garak_review.safe_excel_text


def test_read_jsonl_parses_objects_and_skips_other_values(tmp_path) -> None:
    input_path = tmp_path / "results.jsonl"
    input_path.write_text(
        '\n{"entry_type":"init","run":"run-123"}\n["not", "an", "object"]\n',
        encoding="utf-8",
    )

    assert list(read_jsonl(input_path)) == [{"entry_type": "init", "run": "run-123"}]


def test_read_jsonl_reports_invalid_line_number(tmp_path) -> None:
    input_path = tmp_path / "invalid.jsonl"
    input_path.write_text('{"valid":true}\nnot-json\n', encoding="utf-8")

    with pytest.raises(ValueError, match=r"invalid\.jsonl at line 2"):
        list(read_jsonl(input_path))


def test_parse_sources_extracts_max_nested_detector_score(tmp_path) -> None:
    input_path = tmp_path / "garak.jsonl"
    records = [
        {"entry_type": "start_run setup", "run.generations": 3},
        {"entry_type": "init", "run": "run-123"},
        {
            "entry_type": "attempt",
            "status": 2,
            "probe_classname": "promptinject.HijackHateHumans",
            "uuid": "attempt-1",
            "seq": 1,
            "prompt": "test prompt",
            "outputs": ["test output"],
            "detector_results": {
                "promptinject.AttackRogueString": [
                    0.25,
                    {"nested": [0.75, True, None]},
                ]
            },
        },
        {
            "entry_type": "eval",
            "probe": "promptinject.HijackHateHumans",
            "detector": "promptinject.AttackRogueString",
            "passed": 2,
            "total": 3,
        },
    ]
    input_path.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    attempt_rows, summary_rows = parse_sources([input_path], review_threshold=0.5)

    assert len(attempt_rows) == 1
    assert attempt_rows[0]["Run_ID"] == "run-123"
    assert attempt_rows[0]["Detector_Score"] == 0.75
    assert attempt_rows[0]["Review_Flag"] == "Review"
    assert summary_rows[0]["Generations"] == 3
    assert summary_rows[0]["Review_Signals"] == 1
    assert summary_rows[0]["Pass_Rate"] == pytest.approx(2 / 3)


@pytest.mark.parametrize(
    "untrusted_value",
    ["=SUM(A1:A2)", "+cmd|' /C calc'!A0", "-1+2", "@SUM(A1:A2)"],
)
def test_safe_excel_text_prevents_formula_injection(untrusted_value) -> None:
    assert safe_excel_text(untrusted_value) == "'" + untrusted_value


def test_safe_excel_text_truncates_long_cells() -> None:
    suffix = "\n[truncated for Excel cell limit]"
    result = safe_excel_text("x" * (MAX_EXCEL_CELL_LENGTH + 100))

    assert len(result) == MAX_EXCEL_CELL_LENGTH
    assert result.endswith(suffix)
