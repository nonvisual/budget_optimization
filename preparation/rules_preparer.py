def prepare_rules():
    types_mapping = {}
    types_mapping["grocery"] = [
        "lidl",
        "rewe",
        "edeka",
        "aldi",
        "netto",
        "dm",
        "kaufland",
        "penny",
        "carrefour",
        "intermarche",
        "rossmann",
    ]

    types_mapping["fashion"] = [
        "zalando",
        "h+m",
        "tk maxx",
        "primark",
        "tezenis",
        "uniqlo",
        "ernstings",
        "relay",
    ]

    types_mapping["shopping"] = [
        "amazon",
        "decathlon",
        "media markt",
        "mac geiz",
        "woolworth",
        "kik",
        "saturn",
        "fielmann",
    ]
    types_mapping["travel"] = [
        "easyjet",
        "lufthansa",
        "booking.com",
        "airbnb",
        "france",
    ]

    types_mapping["rent"] = ["landlord", "mietforderung", "miete"]
    types_mapping["grocery"].append("rossmann")
    types_mapping["income"] = ["salary", "lohn/gehalt"]

    types_mapping["pharmacy"] = ["apotheke"]
    types_mapping["utility"] = [
        "telecom",
        "energie",
        "neflix",
        "maxxim",
        "vodafone",
        "rundfunk",
        "versicherung",
    ]
    types_mapping["credit_card"] = ["kreditkarte"]
    types_mapping["transportation"] = ["bvg", "bahn"]
    types_mapping["withdrawal"] = ["commerzbank "]

    types_mapping["restaurants"] = ["lieferando", "restaurant", "gasthaus"]
    return types_mapping
