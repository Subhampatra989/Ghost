import openai

# Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def fallback_to_chatgpt(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are JARVIS, a smart and helpful AI assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return "Sorry, I couldn’t process that with ChatGPT."
