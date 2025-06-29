import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma:2b" 

def query_llm(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return "⚠️ LLM Error: " + response.text
    except requests.exceptions.Timeout:
        return "⚠️ Ollama timed out. Try a shorter prompt."
    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"



def generate_summary(text):
    prompt = (
        f"You are an insurance assistant.\n"
        f"Summarize the following insurance policy in simple terms. Include:\n"
        f"- ✅ Total coverage\n- ✅ Premium\n- ❌ Exclusions\n- ⏳ Waiting period (if any)\n\n"
        f"Policy Text:\n{text[:600]}"
    )
    return query_llm(prompt)



def generate_claim_guidance(policy_type):
    prompt = (
        f"You are a claims advisor.\n"
        f"List all required documents and steps to file a {policy_type.lower()} insurance claim in India.\n"
        f"Use a numbered checklist format."
    )
    return query_llm(prompt)



def generate_letter(doc_type):
    if doc_type == "nominee":
        prompt = (
            "Write a formal letter requesting nominee update in a life insurance policy. "
            "Include policy number, nominee name, relationship, and reason for change."
        )
    elif doc_type == "appeal":
        prompt = (
            "Write a polite appeal letter to challenge a rejected insurance claim. "
            "Mention policy number, reason for rejection, and request for reconsideration."
        )
    else:
        prompt = "Write a short formal insurance-related letter."
    return query_llm(prompt)



def explain_irda_rule(question):
    prompt = (
        f"You are an insurance expert. Answer this question using IRDAI regulations in India.\n"
        f"Use clear language and include section references if applicable:\n\nQ: {question}"
    )
    return query_llm(prompt)



def check_coverage_fit(age, income, dependents):
    prompt = (
        f"You are a financial advisor.\n"
        f"The user is {age} years old, earns ₹{income}/month, and has {dependents} dependents.\n\n"
        f"Evaluate if their current insurance coverage is sufficient. Suggest:\n"
        f"- Term insurance range\n- Health coverage\n- Emergency fund\n- Education savings\n\n"
        f"Conclude with a 2-line recommendation."
    )
    return query_llm(prompt)



def compare_policies(text1, text2):
    prompt = (
        f"Compare the following two insurance policies.\n"
        f"List differences in:\n- Coverage\n- Premiums\n- Exclusions\n- Waiting periods\n\n"
        f"Policy A:\n{text1[:400]}\n\nPolicy B:\n{text2[:400]}"
    )
    return query_llm(prompt)



def analyze_renewal_change(old_text, new_text):
    prompt = (
        f"You are a policy analyzer.\n"
        f"Identify the changes between the old and renewed policy. Focus on:\n"
        f"- Premium change\n- Coverage amount\n- Exclusions\n- Any added/removed clauses\n\n"
        f"Old Policy:\n{old_text[:400]}\n\nNew Policy:\n{new_text[:400]}"
    )
    return query_llm(prompt)



def analyze_premium_breakdown(text):
    prompt = (
        "You are a financial analyst. Extract and calculate the following from the insurance policy:\n"
        "- Risk Cover (the base premium before tax)\n"
        "- Admin Charges (if not mentioned, assume Rs. 0)\n"
        "- GST (add CGST + SGST if both are present)\n"
        "- Total (sum of Risk Cover + Admin Charges + GST)\n\n"
        "Return only in this format:\n"
        "Risk Cover: ₹xxxxx\nAdmin Charges: ₹xxxxx\nGST: ₹xxxxx\nTotal: ₹xxxxx\n\n"
        f"Text:\n{text[:1000]}"
    )

    response = query_llm(prompt)

    breakdown = {}
    try:
        for line in response.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                amount = ''.join(filter(str.isdigit, v.replace(",", "")))
                breakdown[k.strip()] = int(amount) if amount else 0

        
        if all(k in breakdown for k in ["Risk Cover", "Admin Charges", "GST"]):
            calculated_total = (
                breakdown["Risk Cover"]
                + breakdown["Admin Charges"]
                + breakdown["GST"]
            )
            if "Total" not in breakdown or breakdown["Total"] != calculated_total:
                breakdown["Corrected Total"] = calculated_total

    except Exception:
        breakdown = {"Error": "⚠️ Could not parse premium breakdown."}

    return breakdown


