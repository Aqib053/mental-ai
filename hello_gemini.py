import google.generativeai as genai

# Use your AI Studio API key (not Vertex AI Studio key!)
genai.configure(api_key="AIzaSyCMUMHtYdcICVeQrQo7swft7hmTcYR4834")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Give me a short positive message for a stressed student.")
print("AI says:", response.text)
