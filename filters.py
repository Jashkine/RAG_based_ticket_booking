
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
    if "isLiveTrackingAvailable" in parameters:
        results = [
            e for e in results
            if e.get("isLiveTrackingAvailable") == parameters["isLiveTrackingAvailable"]
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

    if "isFlexiOperator" in parameters:
        results = [
            e for e in results
            if e.get("isFlexiOperator") is not None
            and e.get("isFlexiOperator") == parameters["isFlexiOperator"]
        ]

    # -------- RED DEAL --------
    if "redDeal_Offer_is_available" in parameters:
        results = [
            e for e in results
            if e.get("redDeal_Offer_is_available") is not None
            and e.get("redDeal_Offer_is_available") == parameters["redDeal_Offer_is_available"]
        ]

    # -------- DISCOUNT --------
    if "discount_is_available" in parameters:
        results = [
            e for e in results
            if e.get("discount_is_available") is not None
            and e.get("discount_is_available") == parameters["discount_is_available"]
        ]

    # -------- RTC BUS --------
    if "isRTC" in parameters:
        results = [
            e for e in results
            if e.get("isRTC") is not None
            and e.get("isRTC") == parameters["isRTC"]
        ]

    # -------- RESCHEDULED --------
    if "isRescheduled" in parameters:
        results = [
            e for e in results
            if e.get("isRescheduled") is not None
            and e.get("isRescheduled") == parameters["isRescheduled"]
        ]

    # -------- MTICKET --------
    if "isMticketEnabled" in parameters:
        results = [
            e for e in results
            if e.get("isMticketEnabled") is not None
            and e.get("isMticketEnabled") == parameters["isMticketEnabled"]
        ]

    # -------- FLEXI CANCELLATION --------
    if "isPartialCancellationAllowed" in parameters:
        results = [
            e for e in results
            if e.get("isPartialCancellationAllowed") is not None
            and e.get("isPartialCancellationAllowed") == parameters["isPartialCancellationAllowed"]
        ]

    # -------- CHEAPER THAN TERMINAL --------
    if "cheaperThanTerminal" in parameters:
        results = [
            e for e in results
            if e.get("cheaperThanTerminal") is not None
            and e.get("cheaperThanTerminal") == parameters["cheaperThanTerminal"]
        ]

        # -------- AVAILABLE WINDOW SEATS --------
    if "availableWindowSeats" in parameters:
        results = [
            e for e in results
            if e.get("availableWindowSeats") is not None
            and e.get("availableWindowSeats") >= parameters["availableWindowSeats"]
        ]

    # -------- AVAILABLE SINGLE SEATS --------
    if "availableSingleSeats" in parameters:
        results = [
            e for e in results
            if e.get("availableSingleSeats") is not None
            and e.get("availableSingleSeats") >= parameters["availableSingleSeats"]
        ]

    # -------- AVAILABLE SEATS --------
    if "availableSeats" in parameters:
        results = [
            e for e in results
            if e.get("availableSeats") is not None
            and e.get("availableSeats") >= parameters["availableSeats"]
        ]

    # -------- AVAILABLE AISLE SEATS --------
    if "availableAisleSeats" in parameters:
        results = [
            e for e in results
            if e.get("availableAisleSeats") is not None
            and e.get("availableAisleSeats") >= parameters["availableAisleSeats"]
        ]

    # -------- AVAILABLE UPPER SEATS --------
    if "availableUpperSeats" in parameters:
        results = [
            e for e in results
            if e.get("availableUpperSeats") is not None
            and e.get("availableUpperSeats") >= parameters["availableUpperSeats"]
        ]

    # -------- AVAILABLE LOWER SEATS --------
    if "availableLowerSeats" in parameters:
        results = [
            e for e in results
            if e.get("availableLowerSeats") is not None
            and e.get("availableLowerSeats") >= parameters["availableLowerSeats"]
        ]


    results.sort(key=lambda x: x.get("totalRatings", 0), reverse=True)
    return results
