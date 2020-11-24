def prepare_rules():
    types_mapping = {}
    types_mapping["grocery"] = ["lidl", "rewe", "edeka", "aldi"]

    types_mapping["fashion"] = ["zalando", "h&m"]

    types_mapping["shopping"] = ["amazon", "decathlon", "mediamarkt"]
    types_mapping["travel"] = [
        "easyjet",
        "lufthansa",
        "booking.com",
    ]

    types_mapping["rent"] = ["landlord"]
    types_mapping["grocery"].append("rossmann")
    types_mapping["salary"] = ["salary"]

    return types_mapping
