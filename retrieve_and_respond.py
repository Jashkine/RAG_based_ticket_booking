import json
import faiss
import numpy as np
import openai
from dotenv import load_dotenv
import os
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("preprocessed_data.json", "r") as file:
    data = json.load(file)

index = faiss.read_index("bus_service_index.faiss")

# Function to generate embeddings (dummy for now, replace with actual model)
def generate_embedding(query):
    return np.random.rand(512).astype('float32')

# Function to retrieve relevant data
def retrieve_data(query, top_k=3):
    start_time = time.time()
    query_embedding = generate_embedding(query)
    distances, indices = index.search(np.array([query_embedding]), top_k)
    results = [data[i] for i in indices[0]]
    retrieval_time = time.time() - start_time
    return results, retrieval_time

# Updated generate_response to count input and output tokens and ensure combined tokens are below 5000
def generate_response(query, context):
    # Calculate input tokens
    input_tokens = len(context.split()) + len(query.split()) + 50  # Approximation for prompt structure
    max_output_tokens = min(5000 - input_tokens, 2048)  # Ensure combined tokens are below 5000
    prompt = f"You are a helpful assistant. Answer the query based on the following context:\n\n{context}\n\nQuery: {query}\n\nResponse:. Always list them based on ratings"
    print(f"Max output tokens: {max_output_tokens}")

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                 {"role": "user", "content": prompt}],
        max_tokens=max_output_tokens
    )
    output_tokens = response["usage"]["total_tokens"] - input_tokens
    return response["choices"][0]["message"]["content"], input_tokens, output_tokens

# Main function to handle user query
def handle_query(query):
    results, retrieval_time = retrieve_data(query)
    summarized_context = "\n".join([
        f"Bus: {result['travelsName']}, Route: {result['routeId']}, Fare: {result['fareList'][0]} INR, Departure: {result['departureTime']}, Arrival: {result['arrivalTime']}"
        for result in results
    ])
    response, input_tokens, output_tokens = generate_response(query, summarized_context)
    print(f"Response: {response}\n")
    print(f"Retrieval Time: {retrieval_time:.2f}s, Input Tokens: {input_tokens}, Output Tokens: {output_tokens}")

# Example usage
if __name__ == "__main__":
    # user_query = "Show me buses from Bangalore to Hyderabad with AC and sleeper options."
    user_query = "Give list of all buses from Bangalore to Hydrabad."

    handle_query(user_query)