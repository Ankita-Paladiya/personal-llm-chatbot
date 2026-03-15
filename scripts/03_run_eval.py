import json
from pathlib import Path
from datetime import datetime

from app.chat_engine import ChatEngine


TEST_CASES_PATH = Path("app/eval/test_cases.json")
OUTPUT_PATH = Path("data/processed/eval_results.json")


def load_test_cases():
    with TEST_CASES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def keyword_match_score(answer: str, expected_keywords: list[str]) -> dict:
    answer_lower = answer.lower()
    matched = [kw for kw in expected_keywords if kw.lower() in answer_lower]
    missing = [kw for kw in expected_keywords if kw.lower() not in answer_lower]

    score = 0.0
    if expected_keywords:
        score = len(matched) / len(expected_keywords)

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "keyword_score": round(score, 2)
    }


def run_evaluation():
    engine = ChatEngine()
    test_cases = load_test_cases()

    results = []

    for tc in test_cases:
        print(f"Running {tc['id']} -> {tc['question']}")

        result = engine.answer(tc["user_id"], tc["question"])

        if isinstance(result, dict):
            answer = result.get("answer", "")
            sources = result.get("sources", [])
        else:
            answer = str(result)
            sources = []

        keyword_result = keyword_match_score(answer, tc["expected_keywords"])
        source_check = len(sources) >= tc["min_sources"]

        results.append({
            "test_case_id": tc["id"],
            "user_id": tc["user_id"],
            "question": tc["question"],
            "answer": answer,
            "sources": sources,
            "source_count": len(sources),
            "source_check_passed": source_check,
            "expected_keywords": tc["expected_keywords"],
            "matched_keywords": keyword_result["matched_keywords"],
            "missing_keywords": keyword_result["missing_keywords"],
            "keyword_score": keyword_result["keyword_score"],
            "timestamp": datetime.utcnow().isoformat()
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nEvaluation results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    run_evaluation()
