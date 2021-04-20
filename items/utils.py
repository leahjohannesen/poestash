def get_base_query():
    return {
        "query": {
            "status": { "option": "online" },
            "stats": [
                {
                    "type": "and",
                    "filters": [],
                },
            ],
        },
        "sort": { "price" : "asc" },
    }