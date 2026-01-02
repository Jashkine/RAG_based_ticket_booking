# def filter_by_field(data, key, value, nested=False):
#     result = []
#     for e in data:
#         val = e
#         if nested and "." in key:
#             for k in key.split("."):
#                 val = val.get(k, {}) if isinstance(val, dict) else {}
#             if not val:
#                 val = None
#         else:
#             val = e.get(key, None)
#         if val == value or (isinstance(value, str) and value.lower() in str(val).lower()):
#             result.append(e)
#     return result

# def retrieve_relevant_info(data, parameters):
#     results = data
#     # Filter example: source, destination, travel_date, bus_type, is_ac, is_sleeper
#     if "source" in parameters:
#         results = filter_by_field(results, "source", parameters["source"], nested=True)
#     if "destination" in parameters:
#         results = filter_by_field(results, "destination", parameters["destination"], nested=True)
#     if "travel_date" in parameters:
#         results = filter_by_field(results, "doj", parameters["travel_date"])
#     if "bus_type" in parameters:
#         results = filter_by_field(results, "busType", parameters["bus_type"])
#     if "is_ac" in parameters:
#         results = filter_by_field(results, "isAc", parameters["is_ac"])
#     if "is_sleeper" in parameters:
#         results = filter_by_field(results, "isSleeper", parameters["is_sleeper"])
#     if "ratings_above" in parameters:
#         results = [e for e in results if e.get("totalRatings", 0) >= parameters["ratings_above"]]
#     if "rs555" in parameters:
#         results = filter_by_field(results, "rs555", parameters["rs555"])
#     # Sort by ratings
#     results.sort(key=lambda x: x.get("totalRatings", 0), reverse=True)
#     return results


def retrieve_relevant_info(data, parameters):
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
