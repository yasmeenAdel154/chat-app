from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os

def generate_response(prompt: str) -> str:
    try:
        # Hugging Face token (optional for gated models)
        HF_TOKEN = os.getenv("HF_TOKEN")

        # Model ID (gated example)
        MODEL_ID = "meta-llama/Llama-2-7b-hf"

        # Load tokenizer & model
        print("🔄 Loading model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, token=HF_TOKEN)

        # Create pipeline
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

        # Generate response
        output = generator(
            prompt,
            max_length=200,
            temperature=0.7,
            do_sample=True
        )

        return output[0]["generated_text"]

    except Exception as e:
        # Catch any exception and return the message as "reply"
        #return f"⚠️ An error occurred: {str(e)}"
        return f"⚠️ there is not free llm available , please try again later  "

# Example usage
if __name__ == "__main__":
    user_prompt = "What is the capital of Egypt?"
    reply = generate_response(user_prompt)
    print("\nAssistant reply:\n", reply)



"""
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Free, open small model (no approval needed)
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

print("Loading model... (first time will download ~2GB)")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Create pipeline
chat = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,
    temperature=0.7,
    do_sample=True
)

# Example conversation
user_input = "answer this question ,what is the capital of egypty ?"
print("\nUser:", user_input)

response = chat(user_input)[0]["generated_text"]
print("\nAssistant:", response)
"""
