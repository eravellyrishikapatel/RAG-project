from config import client, MODEL_NAME
import re


def generate_local_answer(prompt):
    context_match = re.search(
        r"Context\s*(.*?)\s*={20,}",
        prompt,
        re.DOTALL | re.IGNORECASE
    )
    question_match = re.search(
        r"Question\s*(.*?)\s*={20,}",
        prompt,
        re.DOTALL | re.IGNORECASE
    )

    if not context_match:
        return "I couldn't find the answer in the provided PDF."

    context = context_match.group(1).strip()
    question = question_match.group(1).strip() if question_match else ""

    stop_words = {
        "a", "an", "the", "is", "are", "was", "were", "of", "in", "to",
        "for", "and", "or", "what", "which", "who", "where", "when",
        "how", "does", "do", "did", "can", "could", "should",
    }
    question_terms = {
        word.lower() for word in re.findall(r"[A-Za-z0-9]+", question)
        if word.lower() not in stop_words
    }

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", context)
        if sentence.strip()
    ]

    ranked = []
    for sentence in sentences:
        terms = {
            word.lower()
            for word in re.findall(r"[A-Za-z0-9]+", sentence)
        }
        overlap = len(question_terms.intersection(terms))
        if overlap:
            ranked.append((overlap, sentence))

    ranked.sort(key=lambda item: item[0], reverse=True)
    selected = [sentence for _, sentence in ranked[:3]]

    if not selected:
        return "I couldn't find the answer in the provided PDF."

    return " ".join(selected)


def generate_answer(prompt):

    print("\n" + "=" * 60)
    print("STEP 8 : GENERATING ANSWER")
    print("=" * 60)

    if client is None:
        answer = generate_local_answer(prompt)
        print("\nLocal Free-Source Response\n")
        print(answer)
        return answer

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        answer = response.choices[0].message.content

        print("\nOpenRouter Response\n")
        print(answer)

        return answer

    except Exception as e:

        print(
            f"\nError generating response: {e}"
        )

        return (
            "Sorry, an error occurred while "
            "generating the response."
        )