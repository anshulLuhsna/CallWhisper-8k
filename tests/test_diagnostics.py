import json

from callwhisper.eval.diagnostics import diagnose_row, read_json_predictions, summarize


def test_diagnose_row_flags_repetition_and_length_explosion():
    row = diagnose_row(
        {
            "model": "base",
            "slice": "gramvaani_dev_50",
            "condition": "telephone_mp3",
            "num_beams": "1",
            "reference_text": "ये संघ के जीतने भी सदस्य हैं",
            "hypothesis_text": "तो " * 24,
            "wer": "10.0",
            "cer": "7.5",
        }
    )

    assert row["repeated_token_loop"] is True
    assert row["length_explosion"] is True
    assert row["hallucination_risk"] is True


def test_diagnose_row_flags_script_drift_and_empty_output():
    script_drift = diagnose_row(
        {
            "model": "base",
            "slice": "gramvaani_dev_50",
            "condition": "telephone_mp3",
            "num_beams": "1",
            "reference_text": "मेरा नाम अनिल कुमार है",
            "hypothesis_text": "mera naam anil kumar hai",
            "wer": "1.0",
            "cer": "1.0",
        }
    )
    empty = diagnose_row(
        {
            "model": "base",
            "slice": "gramvaani_dev_50",
            "condition": "telephone_mp3",
            "num_beams": "1",
            "reference_text": "मेरा नाम अनिल कुमार है",
            "hypothesis_text": "",
            "wer": "1.0",
            "cer": "1.0",
        }
    )

    assert script_drift["script_drift"] is True
    assert script_drift["hallucination_risk"] is True
    assert empty["empty_or_near_empty"] is True


def test_summarize_groups_diagnostics_by_model_slice_and_beam():
    rows = [
        diagnose_row(
            {
                "model": "base",
                "slice": "gramvaani_dev_50",
                "condition": "telephone_mp3",
                "num_beams": "1",
                "reference_text": "ये संघ के जीतने भी सदस्य हैं",
                "hypothesis_text": "तो " * 24,
                "wer": "10.0",
                "cer": "7.5",
            }
        ),
        diagnose_row(
            {
                "model": "base",
                "slice": "gramvaani_dev_50",
                "condition": "telephone_mp3",
                "num_beams": "1",
                "reference_text": "मेरा नाम अनिल कुमार है",
                "hypothesis_text": "मेरा नाम अनिल कुमार है",
                "wer": "0.0",
                "cer": "0.0",
            }
        ),
    ]

    summary = summarize(rows)

    assert len(summary) == 1
    assert summary[0]["files"] == 2
    assert summary[0]["macro_wer"] == 5.0
    assert summary[0]["hallucination_risk_rate"] == 0.5
    assert summary[0]["repetition_rate"] == 0.5


def test_read_json_predictions_reads_eval_samples(tmp_path):
    path = tmp_path / "predictions.json"
    path.write_text(
        json.dumps(
            {
                "samples": [
                    {
                        "model": "large-v3",
                        "slice": "gramvaani_dev_100_8khz",
                        "condition": "telephone_mp3",
                        "reference_text": "मेरा नाम अनिल कुमार है",
                        "hypothesis_text": "मेरा नाम अनिल है",
                        "wer": 0.2,
                        "cer": 0.1,
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    rows = read_json_predictions([str(path)])

    assert len(rows) == 1
    assert rows[0]["model"] == "large-v3"
    assert rows[0]["wer"] == 0.2
