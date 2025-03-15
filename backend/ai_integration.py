import os
import openai
from datetime import datetime

# Configure OpenAI API (replace with your API key in production)
openai.api_key = os.environ.get('OPENAI_API_KEY', 'your-api-key-here')

def generate_code(file_info, model_type, run_mode):
    """
    Generate code using OpenAI API based on the uploaded file and selected parameters.
    """
    prompt = f"""
    Generate Python code to:
    1. Load and process the dataset from '{file_info['filename']}'
    2. Implement a {model_type} model
    3. Execute the model in {run_mode} mode
    4. Include appropriate error handling and logging
    
    The dataset content preview:
    {file_info['content'][:500]}...
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that generates Python code for machine learning tasks."},
                {"role": "user", "content": prompt}
            ]
        )
        
        generated_code = response.choices[0].message.content
        return generated_code

    except Exception as e:
        raise Exception(f"Error generating code: {str(e)}")

def ai_chat(message, username):
    """
    Process chat messages using OpenAI API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for a machine learning platform."},
                {"role": "user", "content": f"User {username}: {message}"}
            ]
        )
        
        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Error processing chat message: {str(e)}")

# Audit logging for alpha users
def log_action(username, action, details):
    """
    Log user actions for audit purposes.
    """
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] User: {username}, Action: {action}, Details: {details}\n"
    
    # In a production environment, this should write to a secure audit log
    print(log_entry)  # Replace with proper logging in production
