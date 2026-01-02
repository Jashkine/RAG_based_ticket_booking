import json
import json.decoder
import openai
from dotenv import load_dotenv
import os
import re
# Load environment variables
load_dotenv(override=True)

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
with open("data_list.json", "r") as file:
    data = json.load(file)

# Function to count tokens in a string
def count_tokens(text):
    return len(text.split())
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
        "standardBpName": "Standardized boarding point name (e.g., 'Hebbal')",
        "standardBpIdentifier": "Unique identifier for the boarding point",
        "standardDpName": "Standardized dropping point name (e.g., 'Lakdikapul')",
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
    prompt = f'''Use the following schema as a guide:\n\n{json.dumps(json_schema, indent=2)}\n\nQuery: {query}\n\n:
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
               - The output must be **wrapped in a JSON markdown code block**, like this:
                ```json
                {{
                }}```
                '''
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
    return parameters
    
# Retrieve relevant information
def retrieve_relevant_info(parameters):
    results = data  # start with full dataset

    # -------- SOURCE --------
    if "source" in parameters:
        source = parameters["source"].lower()
        results = [
            e for e in results
            if source in e.get("serviceName", "").lower()
               or source in e.get("standardBpName", "").lower()
        ]

    # -------- DESTINATION --------
    if "destination" in parameters:
        destination = parameters["destination"].lower()
        results = [
            e for e in results
            if destination in e.get("serviceName", "").lower()
               or destination in e.get("standardDpName", "").lower()
        ]

    # -------- FARE RANGE --------
    if "min_fare" in parameters or "max_fare" in parameters:
        min_fare = parameters.get("min_fare", 0)
        max_fare = parameters.get("max_fare", float("inf"))
        results = [
            e for e in results
            if min_fare <= (e.get("fareList") or [0])[0] <= max_fare
        ]

    # -------- BUS TYPE --------
    if "bus_type" in parameters:
        bus_type = parameters["bus_type"].lower()
        results = [
            e for e in results
            if bus_type in e.get("busType", "").lower()
        ]

    # -------- TRAVEL DATE --------
    if "travel_date" in parameters:
        results = [
            e for e in results
            if e.get("doj") == parameters["travel_date"]
        ]

    # -------- AC --------
    if "is_ac" in parameters:
        results = [
            e for e in results
            if e.get("isAc") == parameters["is_ac"]
        ]

    # -------- SLEEPER --------
    if "is_sleeper" in parameters:
        results = [
            e for e in results
            if e.get("isSleeper") == parameters["is_sleeper"]
        ]

    # -------- LIVE TRACKING --------
    if "is_live_tracking_available" in parameters:
        results = [
            e for e in results
            if e.get("isLiveTrackingAvailable") == parameters["is_live_tracking_available"]
        ]

    # -------- MTICKET --------
    if "is_mticket_enabled" in parameters:
        results = [
            e for e in results
            if e.get("isMticketEnabled") == parameters["is_mticket_enabled"]
        ]

    # -------- RATINGS --------
    if "ratings_above" in parameters:
        results = [
            e for e in results
            if e.get("totalRatings", 0) >= parameters["ratings_above"]
        ]

    # -------- OPERATOR --------
    if "operatorId" in parameters:
        results = [
            e for e in results
            if e.get("operatorId") == parameters["operatorId"]
        ]

    # -------- TRAVELS NAME --------
    if "travelsName" in parameters:
        tn = parameters["travelsName"].lower()
        results = [
            e for e in results
            if tn in e.get("travelsName", "").lower()
        ]

    # -------- SERVICE NAME --------
    if "serviceName" in parameters:
        sn = parameters["serviceName"].lower()
        results = [
            e for e in results
            if sn in e.get("serviceName", "").lower()
        ]

    # -------- AMENITIES --------
    if "amenities" in parameters:
        amenities = parameters["amenities"]
        results = [
            e for e in results
            if all(a in e.get("amenities", []) for a in amenities)
        ]

    # -------- PRIMO / RS555 --------
    if "rs555" in parameters:
        results = [
            e for e in results
            if e.get("rs555") is not None and e.get("rs555") == parameters["rs555"]
        ]

    results.sort(key=lambda x: x.get("totalRatings", 0), reverse=True)
    return results

user_query = "departure on 15th Dec 2025 and ratings above 4.0"
parameters = handle_query(user_query)
results = retrieve_relevant_info(parameters)

MANDATORY_FIELDS = [
    ("inventoryData.sourceName", "Source"),
    ("inventoryData.destinationName", "Destination"),
    ("travelsName", "Travels Name"),
    ("fareList", "Fare"),
    ("departureTime", "Departure"),
    ("arrivalTime", "Arrival"),
    ("busType", "Bus Type"),
    ("availableSeats", "Available Seats"),
    ("totalRatings", "Ratings")
]

# Parameter → display field mapping
PARAMETER_FIELD_MAP = {
    "source": ("inventoryData.sourceName", "Source"),
    "destination": ("inventoryData.destinationName", "Destination"),
    "min_fare": ("minFare", "Minimum Fare"),
    "max_fare": ("maxFare", "Maximum Fare"),
    "bus_type": ("busType", "Bus Type"),
    "travel_date": ("doj", "Travel Date"),
    "departure_time": ("departureTime", "Departure Time"),
    "arrival_time": ("arrivalTime", "Arrival Time"),
    "is_ac": ("isAc", "AC"),
    "is_sleeper": ("isSleeper", "Sleeper"),
    "is_live_tracking_available": ("isLiveTrackingAvailable", "Live Tracking"),
    "is_mticket_enabled": ("isMticketEnabled", "M-Ticket"),
    "ratings_above": ("totalRatings", "Ratings"),
    "operatorId": ("operatorId", "Operator ID"),
    "travelsName": ("travelsName", "Travels Name"),
    "routeId": ("routeId", "Route ID"),
    "serviceName": ("serviceName", "Service Name"),
    "serviceId": ("serviceId", "Service ID"),
    "operatorLogoPath": ("operatorLogoPath", "Operator Logo"),
    "boReqParams": ("boReqParams", "BO Request Params"),
    "cancellationPolicy": ("cancellationPolicy", "Cancellation Policy"),
    "isPartialCancellationAllowed": ("isPartialCancellationAllowed", "Partial Cancellation Allowed"),
    "isSeatLayoutAvailable": ("isSeatLayoutAvailable", "Seat Layout Available"),
    "serviceNotes": ("serviceNotes", "Service Notes"),
    "inventoryData": ("inventoryData", "Inventory Data"),
    "journeyDurationMin": ("journeyDurationMin", "Journey Duration (min)"),
    "firstBpTime": ("firstBpTime", "First Boarding Point Time"),
    "doj": ("doj", "Date of Journey"),
    "rescheduleTime": ("rescheduleTime", "Reschedule Time"),
    "standardBpName": ("standardBpName", "Boarding Point"),
    "standardBpIdentifier": ("standardBpIdentifier", "Boarding Point ID"),
    "standardDpName": ("standardDpName", "Dropping Point"),
    "standardDpIdentifier": ("standardDpIdentifier", "Dropping Point ID"),
    "bpCount": ("bpCount", "Boarding Points Count"),
    "dpCount": ("dpCount", "Dropping Points Count"),
    "locationSearchParams": ("locationSearchParams", "Location Search Params"),
    "maxSeatsPerTransaction": ("maxSeatsPerTransaction", "Max Seats per Transaction"),
    "availableWindowSeats": ("availableWindowSeats", "Available Window Seats"),
    "availableSingleSeats": ("availableSingleSeats", "Available Single Seats"),
    "availableSeats": ("availableSeats", "Available Seats"),
    "totalSeats": ("totalSeats", "Total Seats"),
    "availableAisleSeats": ("availableAisleSeats", "Available Aisle Seats"),
    "availableUpperSeats": ("availableUpperSeats", "Available Upper Seats"),
    "availableLowerSeats": ("availableLowerSeats", "Available Lower Seats"),
    "busImageCount": ("busImageCount", "Bus Image Count"),
    "totalRatings": ("totalRatings", "Total Ratings"),
    "numberOfReviews": ("numberOfReviews", "Number of Reviews"),
    "busScore": ("busScore", "Bus Score"),
    "perzScore": ("perzScore", "Personalized Score"),
    "fareList": ("fareList", "Fare List"),
    "vendorCurrency": ("vendorCurrency", "Currency"),
    "campaignType": ("campaignType", "Campaign Type"),
    "isFlexiOperator": ("isFlexiOperator", "Flexi Operator"),
    "cheaperThanTerminal": ("cheaperThanTerminal", "Cheaper Than Terminal"),
    "amenities": ("amenities", "Amenities"),
    "isRescheduled": ("isRescheduled", "Rescheduled"),
    "rs555": ("rs555", "Is Primo"),
    "redDeal_Offer_is_available": ("redDeal_Offer_is_available", "Red Deal Available"),
    "discount_is_available": ("discount_is_available", "Discount Available"),
    "isRTC": ("isRTC", "RTC Bus")
}


def get_display_fields(parameters):
    fields = []

    # Always include mandatory fields
    fields.extend(MANDATORY_FIELDS)

    # Add parameter-specific fields
    for param in parameters:
        if param in PARAMETER_FIELD_MAP:
            field = PARAMETER_FIELD_MAP[param]
            if field not in fields:
                fields.append(field)

    return fields

display_fields = get_display_fields(parameters)

if not results:
    print("No results found for the given query.")
else:
    print(f"Found {len(results)} result(s) based on your query:\n")
    for result in results:
        for key, label in display_fields:
            # Nested keys support (like inventoryData.sourceName)
            if "." in key:
                keys = key.split(".")
                value = result
                for k in keys:
                    value = value.get(k, {}) if isinstance(value, dict) else {}
                if not value:
                    value = "N/A"
            else:
                value = result.get(key, "N/A")

            # Fare handling
            if key == "fareList":
                fare = result.get("fareList", [None])[0]
                value = f"{fare} INR" if fare is not None else "N/A"

            # Boolean handling
            elif isinstance(value, bool):
                value = "Yes" if value else "No"

            # Default handling
            elif value is None:
                value = "N/A"

            print(f"{label}: {value}")

        print("-" * 50)



if __name__ == "__main__":
    user_query = "departure on 15th Dec 2025 and ratings above 4.0"
    handle_query(user_query)