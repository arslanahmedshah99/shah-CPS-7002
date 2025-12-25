import pandas as pd
import os

ROUTES_CSV = 'data/routes.csv'

def load_routes():
    if os.path.exists(ROUTES_CSV):
        df = pd.read_csv(ROUTES_CSV)
        df['distance_m'] = pd.to_numeric(df['distance_m'], errors='coerce')
        df['accessible'] = df['accessible'].astype(str).str.lower() == 'true'
        return df
    return pd.DataFrame(columns=['id', 'start_location', 'end_location', 'distance_m', 'accessible'])

df = load_routes()

# Test with different locations
test_cases = [
    ('Gym', 'Library'),
    ('Library', 'Cafeteria'),
    ('Cafeteria', 'Lecture Hall A')
]

for start, end in test_cases:
    route = df[
        ((df['start_location'] == start) & (df['end_location'] == end)) |
        ((df['start_location'] == end) & (df['end_location'] == start))
    ]
    print(f'Routes between {start} and {end}: {len(route)}')
    if not route.empty:
        shortest_route = route.loc[route['distance_m'].idxmin()]
        print(f'  Shortest: {shortest_route["distance_m"]} meters, Accessible: {shortest_route["accessible"]}')
    else:
        print('  No routes found')
    print()