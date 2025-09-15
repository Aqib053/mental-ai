from vertexai.generative_models import GenerativeModel
import vertexai

# Initialize Vertex AI
vertexai.init(project="mental-wellness-ai-472205", location="us-central1")

# Try Gemini 1.0 Pro (available in most free tier accounts)
model = GenerativeModel("gemini-1.0-pro")

# Test a prompt
response = model.generate_content("Give me a short positive message for a stressed student.")

print("AI says:", response.text)
