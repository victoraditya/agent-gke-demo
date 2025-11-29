import os
from google.cloud import aiplatform
import vertexai

project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "agent-gke-demo")
location = "us-central1"

print(f"Initializing Vertex AI for project: {project_id}, location: {location}")

try:
    vertexai.init(project=project_id, location=location)
    from vertexai.preview.generative_models import GenerativeModel
    
    print("Attempting to list models or load a model...")
    # Try to just instantiate a model and see if it works
    model = GenerativeModel("gemini-1.5-flash")
    print("Successfully instantiated gemini-1.5-flash")
    
    response = model.generate_content("Hello")
    print("Successfully generated content:", response.text)

except Exception as e:
    print(f"Error: {e}")

print("\nListing available models in Model Garden (if possible via SDK)...")
try:
    # There isn't a direct simple list_models for foundation models in the high level SDK easily accessible
    # but we can try to use the lower level API
    from google.cloud import aiplatform_v1
    client = aiplatform_v1.ModelServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )
    # This lists custom models, not publisher models usually, but let's see
    request = aiplatform_v1.ListModelsRequest(parent=f"projects/{project_id}/locations/{location}")
    page_result = client.list_models(request=request)
    print("Custom Models found:")
    for response in page_result:
        print(response)
except Exception as e:
    print(f"Error listing custom models: {e}")
