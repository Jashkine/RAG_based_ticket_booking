import json
import faiss
import numpy as np
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load data
with open("data_list.json", "r") as file:
    data = json.load(file)

# Preprocess data and compute derived flags
for entry in data:
    entry["redDeal_Offer_is_available"] = entry.get("rdBoostInfo", {}).get("dealType", "") == "REDDEAL"
    entry["discount_is_available"] = entry.get("rdBoostInfo", {}).get("dealType", "") != ""
    entry["isRTC"] = entry.get("travelsName", "").lower().startswith("rtc")

# Create embeddings (dummy embeddings for now, replace with actual embeddings)
embeddings = [np.random.rand(512).astype('float32') for _ in data]

# Create FAISS index
d = 512  # Dimension of embeddings
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings))

# Save index
faiss.write_index(index, "bus_service_index.faiss")

# Save preprocessed data
with open("preprocessed_data.json", "w") as file:
    json.dump(data, file)

print("Data preprocessing and indexing complete.")