```python
from google.cloud import aiplatform

def list_models():
    client = aiplatform.gapic.ModelServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    parent = f"projects/mental-wellness-ai-472205/locations/us-central1"
    models = client.list_models(parent=parent)

    for model in models:
        print(model.name, "-", model.display_name)

if __name__ == "__main__":
    list_models()
