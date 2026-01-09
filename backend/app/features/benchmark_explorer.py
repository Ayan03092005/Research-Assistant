from ..io.schemas import BenchmarkRequest, BenchmarkResponse

# Minimal registry for MVP
_METRICS = {
    "image-classification": [
        {"name":"Top-1 Accuracy","direction":"higher-better","equation":"correct/total"},
        {"name":"Top-5 Accuracy","direction":"higher-better"},
        {"name":"F1-score","direction":"higher-better"}
    ],
    "text-generation": [
        {"name":"BLEU","direction":"higher-better"},
        {"name":"ROUGE-L","direction":"higher-better"}
    ]
}

def recommend_benchmarks(payload: BenchmarkRequest, db, current):
    metrics = _METRICS.get(payload.task_type.lower(), [{"name":"Accuracy","direction":"higher-better"}])
    guidance = "Select metrics aligned with your task and constraints (e.g., latency, fairness). Report definitions and pitfalls."
    return BenchmarkResponse(metrics=metrics, guidance=guidance)
