import json
import json.decoder
import openai
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load data
with open("data_list.json", "r") as file:
    data = json.load(file)
def retrieve_relevant_information(parameters):
    results = []

    for entry in data:
        match = True

        for key, value in parameters.items():
            # -------- SOURCE --------
            if key == "source":
                if value.lower() not in entry.get("standardBpName", "").lower():
                    match = False
                    break

            # -------- DESTINATION --------
            elif key == "destination":
                if value.lower() not in entry.get("standardDpName", "").lower():
                    match = False
                    break

            # -------- PRIMO BUS --------
            elif key == "rs555":
                if entry.get("rs555", False) != value:
                    match = False
                    break

            # -------- AC --------
            elif key == "is_ac":
                if entry.get("isAc", False) != value:
                    match = False
                    break

            # -------- SLEEPER --------
            elif key == "is_sleeper":
                if entry.get("isSleeper", False) != value:
                    match = False
                    break

            # -------- RATINGS --------
            elif key == "ratings_above":
                if float(entry.get("totalRatings", 0)) < float(value):
                    match = False
                    break

            # -------- BUS TYPE --------
            elif key == "bus_type":
                if value.lower() not in entry.get("busType", "").lower():
                    match = False
                    break

            # -------- FARE RANGE --------
            elif key == "min_fare":
                fare = (entry.get("fareList") or [0])[0]
                if fare < value:
                    match = False
                    break

            elif key == "max_fare":
                fare = (entry.get("fareList") or [0])[0]
                if fare > value:
                    match = False
                    break

            # -------- AMENITIES --------
            elif key == "amenities":
                if not all(a in entry.get("amenities", []) for a in value):
                    match = False
                    break

            # -------- TRAVELS NAME --------
            elif key == "travelsName":
                if value.lower() not in entry.get("travelsName", "").lower():
                    match = False
                    break

            # -------- FALLBACK (DIRECT MATCH) --------
            else:
                if entry.get(key) != value:
                    match = False
                    break

        if match:
            results.append(entry)

    # Sort only AFTER filtering
    results.sort(key=lambda x: x.get("totalRatings", 0), reverse=True)

    return results


# Updated retrieve_relevant_info to include all parameters from the schema
def retrieve_relevant_info(parameters):
    # Extract parameters
    source = parameters.get("source", "")
    destination = parameters.get("destination", "")
    min_fare = parameters.get("min_fare", 0)
    max_fare = parameters.get("max_fare", float("inf"))
    bus_type = parameters.get("bus_type", None)
    travel_date = parameters.get("travel_date", None)
    departure_time = parameters.get("departure_time", None)
    arrival_time = parameters.get("arrival_time", None)
    is_ac = parameters.get("is_ac", None)
    is_sleeper = parameters.get("is_sleeper", None)
    is_live_tracking_available = parameters.get("is_live_tracking_available", None)
    is_mticket_enabled = parameters.get("is_mticket_enabled", None)
    ratings_above = parameters.get("ratings_above", 0)
    operator_id = parameters.get("operatorId", None)
    travels_name = parameters.get("travelsName", None)
    route_id = parameters.get("routeId", None)
    service_name = parameters.get("serviceName", None)
    service_id = parameters.get("serviceId", None)
    amenities = parameters.get("amenities", None)
    red_deal_offer = parameters.get("redDeal_Offer_is_available", None)
    discount_available = parameters.get("discount_is_available", None)
    is_rtc = parameters.get("isRTC", None)
    rs555 = parameters.get("rs555", None)


    # Filter data based on parameters
    results = [
        entry for entry in data
        if (not source or source.lower() in entry.get("standardBpName", "").lower())
        and (not destination or destination.lower() in entry.get("standardDpName", "").lower())
        and (min_fare <= entry.get("fareList", [0])[0] <= max_fare)
        and (not bus_type or bus_type.lower() in entry.get("busType", "").lower())
        and (not travel_date or entry.get("doj", "") == travel_date)
        and (not departure_time or entry.get("departureTime", "") >= departure_time)
        and (not arrival_time or entry.get("arrivalTime", "") <= arrival_time)
        and (is_ac is None or entry.get("isAc", False) == is_ac)
        and (is_sleeper is None or entry.get("isSleeper", False) == is_sleeper)
        and (is_live_tracking_available is None or entry.get("isLiveTrackingAvailable", False) == is_live_tracking_available)
        and (is_mticket_enabled is None or entry.get("isMticketEnabled", False) == is_mticket_enabled)
        and (entry.get("totalRatings", 0) >= ratings_above)
        and (not operator_id or entry.get("operatorId", None) == operator_id)
        and (not travels_name or travels_name.lower() in entry.get("travelsName", "").lower())
        and (not route_id or entry.get("routeId", None) == route_id)
        and (not service_name or service_name.lower() in entry.get("serviceName", "").lower())
        and (not service_id or entry.get("serviceId", None) == service_id)
        and (not amenities or all(amenity in entry.get("amenities", []) for amenity in amenities))
        and (red_deal_offer is None or entry.get("redDeal_Offer_is_available", False) == red_deal_offer)
        and (discount_available is None or entry.get("discount_is_available", False) == discount_available)
        and (is_rtc is None or entry.get("isRTC", False) == is_rtc)
        and (rs555 is None or entry.get("rs555", False) == rs555)

    ]

    # Sort results by totalRatings in descending order
    results = sorted(results, key=lambda x: x.get("totalRatings", 0), reverse=True)

    return results

# Function to count tokens in a string
def count_tokens(text):
    return len(text.split())

# Updated handle_query to display only the results based on parameters provided by LLM
def handle_query(query):
    # Define the full JSON schema for parameters
    json_schema = {
        "source": "Starting location of the buses (e.g., 'Bangalore')",
        "destination": "Destination location of the buses (e.g., 'Hyderabad')",
        "min_fare": "Minimum fare for filtering buses (e.g., 500)",
        "max_fare": "Maximum fare for filtering buses (e.g., 2000)",
        "bus_type": "Type of bus (e.g., 'AC Sleeper', 'Non-AC Seater')",
        "travel_date": "Date of travel in YYYY-MM-DD format (optional)",
        "departure_time": "Filter buses departing after this time (e.g., '18:00')",
        "arrival_time": "Filter buses arriving before this time (e.g., '06:00')",
        "is_ac": "Whether the bus is air-conditioned (true/false)",
        "is_sleeper": "Whether the bus has sleeper berths (true/false)",
        "is_live_tracking_available": "Whether live tracking is available (true/false)",
        "is_mticket_enabled": "Whether m-ticket (mobile ticket) is accepted (true/false)",
        "ratings_above": "Filter buses with ratings above this value (e.g., 4.5)",
        "operatorId": "Unique identifier for the bus operator",
        "travelsName": "Name of the bus operator or travel agency",
        "routeId": "Unique identifier for the bus route",
        "serviceName": "Name or label of the bus service (e.g., 'Express Service')",
        "serviceId": "Unique identifier for the bus service",
        "operatorLogoPath": "File path or URL of the bus operator’s logo image",
        "boReqParams": "Additional request parameters provided by the bus operator (BO)",
        "cancellationPolicy": "Rules and conditions for ticket cancellation",
        "isPartialCancellationAllowed": "Whether partial cancellation (for some passengers only) is allowed",
        "isSeatLayoutAvailable": "Whether seat layout information is available",
        "serviceNotes": "Special notes or instructions about the bus service",
        "inventoryData": "Raw data about seat availability, inventory, and booking rules",
        "journeyDurationMin": "Total journey duration of the bus from start boarding point to end dropping point in minutes",
        "firstBpTime": "Departure time of the first boarding point",
        "doj": "Date of journey",
        "rescheduleTime": "New departure time if the bus is rescheduled",
        "standardBpName": "Standardized boarding point name",
        "standardBpIdentifier": "Unique identifier for the boarding point",
        "standardDpName": "Standardized dropping point name",
        "standardDpIdentifier": "Unique identifier for the dropping point",
        "bpCount": "Total number of boarding points for the service",
        "dpCount": "Total number of dropping points for the service",
        "locationSearchParams": "Metadata related to boarding/dropping location search",
        "maxSeatsPerTransaction": "Maximum number of seats bookable in a single transaction",
        "availableWindowSeats": "Number of available window seats",
        "availableSingleSeats": "Number of available single (non-adjacent) seats",
        "availableSeats": "Total number of available seats",
        "totalSeats": "Total seat capacity of the bus",
        "availableAisleSeats": "Number of available aisle seats",
        "availableUpperSeats": "Number of available upper-berth seats (for sleeper buses)",
        "availableLowerSeats": "Number of available lower-berth seats (for sleeper buses)",
        "busImageCount": "Number of bus images available for the listing",
        "totalRatings": "Average rating given to the bus/operator",
        "numberOfReviews": "Total number of user reviews",
        "busScore": "Internal score/quality metric for the bus",
        "perzScore": "Personalized recommendation score (based on personalization algorithms)",
        "fareList": "List of fares for the service (base fare, discounts, dynamic pricing)",
        "vendorCurrency": "Currency in which fares are quoted",
        "campaignType": "Indicates if the service is part of a campaign or promotion",
        "isFlexiOperator": "Whether the operator supports flexible cancellation/rescheduling policies",
        "cheaperThanTerminal": "Whether price is cheaper than offline price",
        "amenities": "List of amenities provided (Wi-Fi, water bottle, charging point, etc.)",
        "isLiveTrackingAvailable": "Whether live tracking of the bus is available",
        "isMticketEnabled": "Whether m-ticket (mobile ticket) is accepted",
        "isAc": "Whether the bus is air-conditioned",
        "isSleeper": "Whether the bus has sleeper berths",
        "isRescheduled": "Whether the bus has been rescheduled",
        "rs555": "Whether the bus is primo bus",
        "redDeal_Offer_is_available": "Whether red Deal offer is available or not",
        "discount_is_available": "Whether any discount is available for that bus",
        "isRTC": "Is that bus a RTC bus i.e bus from regional transport corporation (state govt controlled bus)"
    }

    # Generate parameters dynamically using LLM
    prompt = f'''You are a helpful assistant. Based on the user query, generate only a JSON object with parameters. Use the following schema as a guide:\n\n{json.dumps(json_schema, indent=2)}\n\nQuery: {query}\n\nJSON Parameters:
                example
                 ```json
                {{
                "source": "Bangalore",
                "destination": "Hyderabad",
                "rs555": true
                }}
                ```'''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        content = response["choices"][0]["message"].get("content", "")
        if not content.strip():
            raise ValueError("The LLM returned an empty response.")

        # Count input tokens
        input_tokens = count_tokens(prompt)

        # Extract JSON object from the response
        json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON object found in the LLM response.")
        parameters = json.loads(json_match.group(1))

        # Count output tokens
        print(parameters)
        output_tokens = count_tokens(content)
        print(f"Input Tokens: {input_tokens}, Output Tokens: {output_tokens}")
        print(f"LLM Response: {content}")
    except (json.decoder.JSONDecodeError, ValueError) as e:
        print(f"Error: {e}")
        print(f"LLM Response: {content}")
        return

    # Retrieve relevant information
    results = retrieve_relevant_information(parameters)
    print(f"Results based on provided parameters: {results}")

    # Display results based on parameters
    for result in results:
        print(f"Travels Name: {result.get('travelsName', 'N/A')}")
        print(f"Source: {result.get('standardBpName', 'N/A')}")
        print(f"Destination: {result.get('standardDpName', 'N/A')}")
        print(f"Is Primo: {'Yes' if result.get('rs555', False) else 'No'}")
        print(f"Fare: {result.get('fareList', ['N/A'])[0]} INR")
        print(f"Departure: {result.get('departureTime', 'N/A')}")
        print(f"Arrival: {result.get('arrivalTime', 'N/A')}")
        print(f"Bus Type: {result.get('busType', 'N/A')}")
        print(f"Available Seats: {result.get('availableSeats', 'N/A')}")
        print(f"Ratings: {result.get('totalRatings', 'N/A')}")
        print("-" * 40)

# Example usage
if __name__ == "__main__":
    user_query = "primo"
    handle_query(user_query)