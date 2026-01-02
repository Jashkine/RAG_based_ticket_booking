def get_display_fields(parameters, mandatory_fields, field_map):
    fields = list(mandatory_fields)
    for param in parameters:
        if param in field_map and field_map[param] not in fields:
            fields.append(field_map[param])
    return fields

def display_results(results, display_fields):
    if not results:
        print("No results found for the query.")
        return

    for result in results:
        for key, label in display_fields:
            value = result
            if "." in key:
                for k in key.split("."):
                    value = value.get(k, {}) if isinstance(value, dict) else {}
                if not value:
                    value = "N/A"
            else:
                value = result.get(key, "N/A")
            # Boolean handling
            if isinstance(value, bool):
                value = "Yes" if value else "No"
            # Fare handling
            if key == "fareList":
                value = f"{(result.get('fareList') or [None])[0]} INR" if result.get("fareList") else "N/A"
            print(f"{label}: {value}")
        print("-" * 50)
