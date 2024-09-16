import gradio as gr
import requests
import os
from transformers import pipeline

# Hugging Face API URL
API_URL = "https://api-inference.huggingface.co/models/google-t5/t5-base"

# Get the token from environment variable
API_TOKEN = os.getenv("HF_API_TOKEN")

# Set headers for API request
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Initialize the translation pipeline with T5-base model (local)
translator_local = pipeline("translation", model="google-t5/t5-base")

# Define available languages
AVAILABLE_LANGUAGES = ["French", "German", "Romanian"]

# Function to perform API-based translation
def query_api(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def translate_api(input_text, target_language):
    target_language = target_language.lower()

    # Set the task prefix based on the chosen language
    if target_language == "french":
        task_prefix = "translate English to French: "
    elif target_language == "german":
        task_prefix = "translate English to German: "
    elif target_language == "romanian":
        task_prefix = "translate English to Romanian: "
    else:
        return "Sorry, this language is not supported."

    # Prepare the input payload for the API request
    full_input = task_prefix + input_text
    payload = {"inputs": full_input}

    # Send the request to Hugging Face API and process the result
    result = query_api(payload)

    # Check for any errors in the API response
    if 'error' in result:
        return result['error']

    return result[0]['translation_text']

# Function to perform local-based translation
def translate_local(input_text, target_language):
    target_language = target_language.lower()

    # Set the task prefix based on the chosen language
    if target_language == "french":
        task_prefix = "translate English to French: "
    elif target_language == "german":
        task_prefix = "translate English to German: "
    elif target_language == "romanian":
        task_prefix = "translate English to Romanian: "
    else:
        return "Sorry, this language is not supported."

    # Perform translation using the local model
    full_input = task_prefix + input_text
    translated = translator_local(full_input, max_length=128)
    return translated[0]['translation_text']

# Wrapper function to switch between API-based and local-based model
def translate(input_text, target_language, model_type):
    if model_type == "API-Based":
        return translate_api(input_text, target_language)
    elif model_type == "Local-Based":
        return translate_local(input_text, target_language)
    else:
        return "Invalid model type selected."

def show_available_languages():
    return ", ".join(AVAILABLE_LANGUAGES)

# Test cases
def run_tests(model_type):
    test_cases = [
        ("Hello", "French"),
        ("How are you?", "German"),
        ("Good morning", "Romanian"),
        ("Hello", "Spanish")  # Expected to fail since Spanish is not supported
    ]
    
    results = []
    for input_text, target_lang in test_cases:
        try:
            result = translate(input_text, target_lang, model_type)
            status = "Passed" if result != "Sorry, this language is not supported." else "Failed"
            results.append(f"Test '{input_text}' to {target_lang}: {status}\nResult: {result}")
        except Exception as e:
            results.append(f"Test '{input_text}' to {target_lang}: Failed - {str(e)}")
    
    return "\n".join(results)

# Guard to prevent the Gradio app from running during imports (like testing)
if __name__ == "__main__":
    # Create Gradio interface
    with gr.Blocks() as iface:
        gr.Markdown("# Translation using T5-base (API or Local)")
        gr.Markdown("Translate English text to French, German, or Romanian using the T5-base model. Choose between using a local model or the Hugging Face API.")

        # Input fields and buttons
        with gr.Row():
            input_text = gr.Textbox(label="Enter English text", placeholder="Hi, how are you?")
            output_text = gr.Textbox(label="Translation")
        
        with gr.Row():
            target_lang = gr.Dropdown(AVAILABLE_LANGUAGES, label="Target Language")
            model_type = gr.Dropdown(["API-Based", "Local-Based"], label="Model Type", value="API-Based")

        translate_btn = gr.Button("Translate")

        # Section to show available languages
        with gr.Row():
            show_langs_btn = gr.Button("Show Available Languages")
            available_langs = gr.Textbox(label="Available Languages")

        # Test button
        test_btn = gr.Button("Run Tests")
        test_output = gr.Textbox(label="Test Results")

        # Button actions
        translate_btn.click(translate, inputs=[input_text, target_lang, model_type], outputs=output_text)
        show_langs_btn.click(show_available_languages, inputs=None, outputs=available_langs)
        test_btn.click(run_tests, inputs=[model_type], outputs=test_output)

    # Launch the app
    iface.launch()
