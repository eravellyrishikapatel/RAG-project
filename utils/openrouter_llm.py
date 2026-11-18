import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import client, MODEL_NAME

LOCAL_MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

_local_tokenizer = None
_local_model = None
_local_device = None


def _load_local_model():
    global _local_tokenizer, _local_model, _local_device

    if _local_tokenizer is None or _local_model is None:
        print(f"\nLoading local LLM: {LOCAL_MODEL_NAME}")
        _local_tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_NAME)
        _local_model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_NAME)
        _local_device = "cuda" if torch.cuda.is_available() else "cpu"
        _local_model.to(_local_device)
        _local_model.eval()
        print(f"Local LLM loaded on {_local_device}.")

    return _local_tokenizer, _local_model, _local_device


def generate_local_answer(prompt):
    tokenizer, model, device = _load_local_model()
    messages = [
        {
            "role": "system",
            "content": (
                "Answer the question using only the provided PDF context. "
                "If the answer is not in the context, reply exactly: "
                "\"I couldn't find the answer in the provided PDF.\""
            ),
        },
        {"role": "user", "content": prompt},
    ]
    model_inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(device)
    input_ids = model_inputs["input_ids"]

    with torch.inference_mode():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=256,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    answer_ids = generated_ids[0][input_ids.shape[-1]:]
    answer = tokenizer.decode(answer_ids, skip_special_tokens=True).strip()

    return answer or "I couldn't find the answer in the provided PDF."


def generate_answer(prompt):

    print("\n" + "=" * 60)
    print("STEP 8 : GENERATING ANSWER")
    print("=" * 60)

    if client is None:
        answer = generate_local_answer(prompt)
        print(f"\nLocal LLM Response ({LOCAL_MODEL_NAME})\n")
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