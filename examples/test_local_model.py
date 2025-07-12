import sys
import os
from transformers import AutoModelForCausalLM, AutoTokenizer # type: ignore [reportMissingImports]
import torch # type: ignore [reportMissingImports]

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_local_model():
    """Test local model inference"""
    try:
        print("Loading model and tokenizer...")
        # Using a small model for quick testing
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # Use float16 for efficiency
            device_map="auto"  # Automatically choose best device (CPU/GPU)
        )

        # Prepare input
        prompt = "Write a hello world message"
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Format prompt for chat
        chat_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # Tokenize input
        inputs = tokenizer(chat_prompt, return_tensors="pt").to(model.device)

        print("\nGenerating response...")
        # Generate response
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

        # Decode response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print("\nTest Response:")
        print(response.split("assistant")[-1].strip())
        return True

    except Exception as e:
        print(f"Error testing local model: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing local model...")
    success = test_local_model()
    if success:
        print("\nLocal model test successful!")
    else:
        print("\nLocal model test failed. Please check the error message above.") 