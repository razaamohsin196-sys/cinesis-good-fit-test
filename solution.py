"""
Cinesis Good Fit Test solution script.

It extracts the driver profile from the transcript manually based on explicit and implied
statements, then filters and ranks loads by effective rate per mile using haversine distance.
"""

from math import radians, sin, cos, asin, sqrt

R_MILES = 3958.8

CURRENT = {"city": "Dallas, TX", "lat": 32.7767, "lon": -96.7970}
HOME = {"city": "San Antonio, TX", "lat": 29.4241, "lon": -98.4936}

PROFILE = {
    "minimum_rate_per_mile": 2.00,
    "equipment": {"Hotshot", "Gooseneck", "Flatbed"},
    "weight_capacity_lb": 14000,
}

LOADS = [
    {"id": "L01", "origin": "Fort Worth", "olat": 32.7555, "olon": -97.3308, "dest": "Oklahoma City", "dlat": 35.4676, "dlon": -97.5164, "trailer": "Van", "weight": 42000, "price": 620},
    {"id": "L02", "origin": "Houston", "olat": 29.7604, "olon": -95.3698, "dest": "Laredo", "dlat": 27.5306, "dlon": -99.4803, "trailer": "Hotshot", "weight": 11500, "price": 1600},
    {"id": "L03", "origin": "Austin", "olat": 30.2672, "olon": -97.7431, "dest": "Corpus Christi", "dlat": 27.8006, "dlon": -97.3964, "trailer": "Gooseneck", "weight": 14200, "price": 1500},
    {"id": "L04", "origin": "Plano", "olat": 33.0198, "olon": -96.6989, "dest": "Memphis", "dlat": 35.1495, "dlon": -90.0490, "trailer": "Van", "weight": 38000, "price": 1500},
    {"id": "L05", "origin": "Waco", "olat": 31.5493, "olon": -97.1467, "dest": "San Antonio", "dlat": 29.4241, "dlon": -98.4936, "trailer": "Flatbed", "weight": 9800, "price": 640},
    {"id": "L06", "origin": "Shreveport", "olat": 32.5252, "olon": -93.7502, "dest": "Atlanta", "dlat": 33.7490, "dlon": -84.3880, "trailer": "Van", "weight": 46500, "price": None},
    {"id": "L07", "origin": "Tulsa", "olat": 36.1540, "olon": -95.9928, "dest": None, "dlat": None, "dlon": None, "trailer": "Hotshot", "weight": 13400, "price": 1100},
    {"id": "L08", "origin": "Dallas", "olat": 32.7767, "olon": -96.7970, "dest": "McAllen", "dlat": 26.2034, "dlon": -98.2300, "trailer": "Hotshot", "weight": 12600, "price": 1700},
]


def haversine(lat1, lon1, lat2, lon2):
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R_MILES * asin(sqrt(a))


def effective_rate(load):
    deadhead_to_origin = haversine(CURRENT["lat"], CURRENT["lon"], load["olat"], load["olon"])
    loaded_miles = haversine(load["olat"], load["olon"], load["dlat"], load["dlon"])
    deadhead_home = haversine(load["dlat"], load["dlon"], HOME["lat"], HOME["lon"])
    total_miles = deadhead_to_origin + loaded_miles + deadhead_home
    return load["price"] / total_miles


def is_complete(load):
    return load["price"] is not None and load["dest"] and load["dlat"] is not None and load["dlon"] is not None


def is_eligible(load):
    if not is_complete(load):
        return False
    if load["trailer"] not in PROFILE["equipment"]:
        return False
    if load["weight"] > PROFILE["weight_capacity_lb"]:
        return False
    return effective_rate(load) >= PROFILE["minimum_rate_per_mile"]


ranked = sorted(
    ((load["id"], effective_rate(load)) for load in LOADS if is_eligible(load)),
    key=lambda item: item[1],
    reverse=True,
)

for rank, (load_id, rate) in enumerate(ranked[:3], start=1):
    print(rank, load_id, f"{rate:.3f}")
