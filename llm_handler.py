import openai, json, re, os
from dotenv import load_dotenv
from config import JSON_SCHEMA

# Load environment variables
load_dotenv(override=True)

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def query_llm_for_parameters(user_query: str) -> dict:
    prompt = f'''Use the following schema as a guide:\n\n{json.dumps(JSON_SCHEMA, indent=2)}\n\nQuery: {user_query}\n\n:
               You are a helpful assistant. Based on the user query, generate a JSON object with parameters.
                - Use **exact values** from the user query.
                - Map keywords in the query to these fields:
                - 'boarding point <name>' → 'standardBpName'
                - 'dropping point <name>' → 'standardDpName'
                - '<city> to <city>' → 'source' and 'destination'
                - 'AC' or 'AC Sleeper' → 'bus_type' and 'is_ac'
                - 'Sleeper' → 'is_sleeper'
                - 'primo' → 'rs555'
                - Any date in YYYY-MM-DD → 'travel_date'
                - Include a field **only if it appears in the query**.
                - Do **not guess or overwrite** any field.
                - also standardize the city names to proper nouns (e.g., 'Bengaluru' to 'Bangalore', 'blr' to 'Bangalore' etc ).
               - The output must be **wrapped in a JSON markdown code block**, like this:
                ```json
                {{
                }}```
                '''
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    content = response["choices"][0]["message"].get("content", "")
    match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
    print(content)
    if not match:
        raise ValueError("No valid JSON found in LLM response")
    
    return json.loads(match.group(1))
