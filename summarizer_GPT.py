import openai

openai.api_key = '-' #replace with your api key for openai

def generate_summary(text):
    prompt_text = f"Summarize the following text: {text}"

    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt_text,
      max_tokens=150  # Adjust the token length as needed for your summary
    )

    return response.choices[0].text.strip()

# Example text to summarize
input_text = """
Hey my name is vidit sheth
"""

# Generate summary using GPT-3
result_summary = generate_summary(input_text)
print("Summary:", result_summary)








