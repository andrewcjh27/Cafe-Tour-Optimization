# Cafe Tour Optimizer

Finds the shortest walking route through a set of cafes using exact TSP (Traveling Salesman Problem) solving with bitmask DFS and haversine distance calculation.

## Overview

Given a list of cafes with GPS coordinates, the optimizer computes the shortest open path visiting all locations. It uses the haversine formula for accurate Earth-surface distances and an exact branch-and-bound DFS solver with bitmask state tracking.

## Features

- Haversine distance calculation between GPS coordinates
- Full distance matrix construction
- Exact shortest-path solver using DFS with pruning
- Formatted output with automatic unit conversion (m/km)
- Demo with real Seoul cafe coordinates

## Tech Stack

- Python 3.9+
- No external dependencies (stdlib only)

## Usage

```bash
python cafe_tour_optimizer.py
```

The demo optimizes routes for 5 and 7 Seoul cafes and validates haversine accuracy against known distances (Seoul-Busan, Seoul-Tokyo).
