import anthropic
import json
import os
import re
import time


def _get_client() -> anthropic.Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY is not set.")
    return anthropic.Anthropic(api_key=key)


def _parse_json(text: str) -> any:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text.strip())


def _call_with_retry(fn, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return fn()
        except anthropic.RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise
        except anthropic.APIError:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise


def generate_assignment(
    topics: list[dict],      # [{"topic": "...", "locked_marks": None or int}]
    total_marks: int,
    reference_texts: list[str],
    title: str = "",
    course: str = "",
) -> dict:
    """
    Generate a balanced assignment.

    - Topics without locked_marks share remaining marks proportionally to complexity.
    - Broader / more complex topics get more questions and marks.
    - Common per-question mark values: 1, 2, 3, 4, 5, 6, 8, 10.
    - Mix of question types per topic.
    - Grand total MUST equal total_marks exactly.
    """
    client = _get_client()

    combined_ref = "\n\n---\n\n".join(reference_texts) if reference_texts else ""
    if len(combined_ref) > 60000:
        combined_ref = combined_ref[:60000] + "\n\n[Reference truncated]"

    ref_section = (
        f"Reference / Course Material (base all questions on this):\n{combined_ref}"
        if combined_ref
        else "No reference material provided — generate academically sound questions for the topics."
    )

    topic_lines = []
    locked_total = 0
    for t in topics:
        if t.get("locked_marks"):
            topic_lines.append(f"- {t['topic']} (FIXED: exactly {t['locked_marks']} marks)")
            locked_total += t["locked_marks"]
        else:
            topic_lines.append(f"- {t['topic']} (AI to allocate from remaining marks)")

    free_marks = total_marks - locked_total
    topics_str = "\n".join(topic_lines)

    def call():
        return client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": f"""You are an expert academic assignment designer.

Create a well-balanced assignment using the topics below.

Assignment details:
- Title: {title or "(suggest an appropriate title)"}
- Course: {course or "(not specified)"}
- Total marks: {total_marks}
- Marks fixed to specific topics: {locked_total}
- Marks to distribute freely: {free_marks}

Topics:
{topics_str}

{ref_section}

Mark allocation rules:
1. Topics marked FIXED must receive exactly the stated marks.
2. Distribute the remaining {free_marks} marks proportionally across other topics.
   - Judge complexity from the reference material or topic breadth.
   - Broader / more complex topics → more marks and more questions.
   - Narrow / simple topics → fewer marks.
3. Per-question marks must be whole numbers from: 1, 2, 3, 4, 5, 6, 8, 10.
4. Mix question types within each topic:
   - Define / State / List           → 1–2 marks
   - Explain / Describe / Outline    → 3–5 marks
   - Discuss / Analyse / Compare     → 6–10 marks
   - Evaluate / Justify / Critique   → 8–15 marks
5. Aim for 2–6 questions per topic.
6. The grand total of ALL question marks MUST equal exactly {total_marks}.
7. Questions must be clear and answerable from the reference material.

Return ONLY valid JSON — no extra text, no markdown fences.

Format:
{{
  "assignment_title": "title here",
  "course": "course here",
  "total_marks": {total_marks},
  "mark_allocation_rationale": "one paragraph explaining mark distribution across topics",
  "topics": [
    {{
      "topic": "Topic Name",
      "marks_allocated": 20,
      "complexity_note": "why this topic received this weighting",
      "questions": [
        {{
          "question_number": 1,
          "question": "Full question text here.",
          "marks": 5,
          "question_type": "explain"
        }}
      ]
    }}
  ]
}}"""
            }]
        )

    response = _call_with_retry(call)
    data = _parse_json(response.content[0].text)

    # Verify total and auto-correct small rounding errors
    actual_total = sum(q["marks"] for t in data["topics"] for q in t["questions"])
    if actual_total != total_marks:
        diff = total_marks - actual_total
        largest = max(data["topics"], key=lambda t: t["marks_allocated"])
        largest["questions"][-1]["marks"] = max(1, largest["questions"][-1]["marks"] + diff)
        largest["marks_allocated"] += diff
        data["total_marks"] = total_marks

    # Re-number questions sequentially across all topics
    n = 1
    for t in data["topics"]:
        for q in t["questions"]:
            q["question_number"] = n
            n += 1

    return data
