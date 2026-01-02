import time
from data_loader import load_data
from llm_handler import query_llm_for_parameters
from filters import retrieve_relevant_info
from display import get_display_fields, display_results
from config import MANDATORY_FIELDS, PARAMETER_FIELD_MAP

if __name__ == "__main__":
    data = load_data("data_list.json")
    user_query = input("Enter your query: ")

    # Get parameters from LLM
    llm_time = time.time()
    parameters = query_llm_for_parameters(user_query)
    print(f"LLM processing time: {time.time() - llm_time:.2f} seconds")

    # Filter data based on parameters
    filter_time = time.time()
    results = retrieve_relevant_info(data, parameters)
    print(f"Data filtering time: {time.time() - filter_time:.2f} seconds")

    # Prepare fields to display
    display_time = time.time()
    display_fields = get_display_fields(parameters, MANDATORY_FIELDS, PARAMETER_FIELD_MAP)
    print(f"Display fields preparation time: {time.time() - display_time:.2f} seconds")
    # Display results
    display_results(results, display_fields)
