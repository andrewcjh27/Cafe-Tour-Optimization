import math
import time
from typing import TypedDict


class Point(TypedDict):
    id: str
    name: str
    lat: float
    lng: float


def haversine_distance_km(a: Point, b: Point) -> float:
    earth_radius_km = 6371
    d_lat = math.radians(b["lat"] - a["lat"])
    d_lng = math.radians(b["lng"] - a["lng"])
    lat1 = math.radians(a["lat"])
    lat2 = math.radians(b["lat"])

    sin_lat = math.sin(d_lat / 2)
    sin_lng = math.sin(d_lng / 2)
    step = sin_lat ** 2 + math.cos(lat1) * math.cos(lat2) * sin_lng ** 2
    arc = 2 * math.atan2(math.sqrt(step), math.sqrt(1 - step))

    return earth_radius_km * arc


def build_distance_matrix(points: list[Point]) -> list[list[float]]:
    return [
        [0.0 if i == j else haversine_distance_km(points[i], points[j])
         for j in range(len(points))]
        for i in range(len(points))
    ]


def solve_shortest_open_path(distance_matrix: list[list[float]]) -> dict:
    size = len(distance_matrix)
    best = {"distance": float("inf"), "order": []}

    def dfs(order: list[int], used_mask: int, distance_so_far: float):
        if distance_so_far >= best["distance"]:
            return
        if len(order) == size:
            best["distance"] = distance_so_far
            best["order"] = order[:]
            return
        for idx in range(size):
            if used_mask & (1 << idx):
                continue
            additional = distance_matrix[order[-1]][idx] if order else 0
            order.append(idx)
            dfs(order, used_mask | (1 << idx), distance_so_far + additional)
            order.pop()

    dfs([], 0, 0)
    return {"order": best["order"], "total_distance_km": best["distance"]}


def format_distance(km: float) -> str:
    if not math.isfinite(km):
        return "-"
    if km < 1:
        return f"{round(km * 1000)} m"
    return f"{km:.1f} km" if km >= 10 else f"{km:.2f} km"


def optimize_route(cafes: list[Point]) -> dict:
    if not isinstance(cafes, list) or len(cafes) < 2:
        raise ValueError("At least 2 points are required to optimize a route.")

    distance_matrix = build_distance_matrix(cafes)
    solved = solve_shortest_open_path(distance_matrix)

    ordered_stops = [cafes[i] for i in solved["order"]]
    leg_distances_km = [
        distance_matrix[solved["order"][i - 1]][solved["order"][i]]
        for i in range(1, len(solved["order"]))
    ]

    return {
        "ordered_stops": ordered_stops,
        "leg_distances_km": leg_distances_km,
        "total_distance_km": solved["total_distance_km"],
    }


if __name__ == "__main__":
    print("=== Cafe Tour Route Optimizer — Demo ===\n")

    seoul_cafes = [
        {"id": "1", "name": "Blue Bottle Samcheong",  "lat": 37.5802, "lng": 126.9827},
        {"id": "2", "name": "Fritz Coffee Mapo",      "lat": 37.5563, "lng": 126.9237},
        {"id": "3", "name": "Anthracite Hapjeong",    "lat": 37.5499, "lng": 126.9131},
        {"id": "4", "name": "Cafe Onion Seongsu",     "lat": 37.5445, "lng": 127.0566},
        {"id": "5", "name": "Terrace Coffee Yeonnam", "lat": 37.5662, "lng": 126.9249},
    ]

    print("Demo 1: 5 Seoul cafes")
    print("Input order:")
    for i, c in enumerate(seoul_cafes):
        print(f"  {i + 1}. {c['name']}  ({c['lat']}, {c['lng']})")

    t1 = time.time()
    result1 = optimize_route(seoul_cafes)
    ms1 = round((time.time() - t1) * 1000)

    print(f"\nOptimized route ({ms1} ms):")
    for i, stop in enumerate(result1["ordered_stops"]):
        leg = "Start" if i == 0 else format_distance(result1["leg_distances_km"][i - 1])
        print(f"  {i + 1}. {stop['name']}  [{leg}]")
    print(f"  Total distance: {format_distance(result1['total_distance_km'])}")

    large_tour = [
        {"id": "a", "name": "Cafe A (Gangnam)",    "lat": 37.4979, "lng": 127.0276},
        {"id": "b", "name": "Cafe B (Hongdae)",    "lat": 37.5563, "lng": 126.9237},
        {"id": "c", "name": "Cafe C (Itaewon)",    "lat": 37.5345, "lng": 126.9946},
        {"id": "d", "name": "Cafe D (Jamsil)",     "lat": 37.5133, "lng": 127.1001},
        {"id": "e", "name": "Cafe E (Myeongdong)", "lat": 37.5636, "lng": 126.9869},
        {"id": "f", "name": "Cafe F (Bukchon)",    "lat": 37.5826, "lng": 126.9831},
        {"id": "g", "name": "Cafe G (Yeouido)",    "lat": 37.5219, "lng": 126.9245},
    ]

    print("\n\nDemo 2: 7 cafes (max allowed by UI)")
    t2 = time.time()
    result2 = optimize_route(large_tour)
    ms2 = round((time.time() - t2) * 1000)

    print(f"Optimized route ({ms2} ms):")
    for i, stop in enumerate(result2["ordered_stops"]):
        leg = "Start" if i == 0 else format_distance(result2["leg_distances_km"][i - 1])
        print(f"  {i + 1}. {stop['name']}  [{leg}]")
    print(f"  Total distance: {format_distance(result2['total_distance_km'])}")

    print("\n\nDemo 3: Haversine distance check")
    seoul = {"lat": 37.5665, "lng": 126.9780}
    busan = {"lat": 35.1796, "lng": 129.0756}
    tokyo = {"lat": 35.6762, "lng": 139.6503}
    print(f"  Seoul → Busan: {format_distance(haversine_distance_km(seoul, busan))}  (actual ~325 km)")
    print(f"  Seoul → Tokyo: {format_distance(haversine_distance_km(seoul, tokyo))}  (actual ~1,160 km)")

    print("\nDone.")
