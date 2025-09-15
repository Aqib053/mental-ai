import google.generativeai as genai

# Configure Gemini (replace with your key before running)
genai.configure(api_key="YOUR_API_KEY_HERE")

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate a test response
response = model.generate_content("Give me a short positive message for a stressed student.")
print("AI says:", response.text)
