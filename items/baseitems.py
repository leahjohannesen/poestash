def get_base_query():
    return {
        "query": {
            "status": { "option": "online" },
            "type": None,
            "stats": [
                {
                    "type": "and",
                    "filters": [],
                },
            ],
        },
        "sort": { "price" : "asc" },
    }