API_KEY = "FE436489-3962-4ECF-93CE-39F925E14EAA"

#Import the gtfs-kit module
import gtfs_kit as gk
from pathlib import Path

#Declare the directory path for the GTFS zip file
path = Path(r"dabus.zip")

#Read the feed with gtfs-kit
feed = (gk.read_feed(path, dist_units='km'))

#Search for errors and warnings in the feed
# x = feed.validate()

vehicle_ids = feed.trips['trip_id'].unique()

# Print all the vehicle IDs
print("Vehicle IDs:")
print(vehicle_ids)
print("Length vehicle_ids", len(vehicle_ids))

# Extract the routes from the 'routes' dataframe
routes = feed.routes

# Print all the routes
# print("Routes:")
# print(routes)
# print("Length routes: ", len(routes))

# print(routes[['route_id', 'route_short_name', 'route_long_name']])

route_short_name = "2"
route = feed.routes[feed.routes['route_short_name'] == route_short_name]

# Check if the route was found
if route.empty:
    print(f"No route found with route_short_name {route_short_name}.")
else:
    # Get the route_id
    route_id = route.iloc[0]['route_id']

    # Filter the trips dataframe for trips associated with this route_id
    trips = feed.trips[feed.trips['route_id'] == route_id]

    # Join the trips with stop times to get the full schedule
    schedule = feed.stop_times.merge(trips, on='trip_id')

    # Sort the schedule by trip_id and stop_sequence to get the order of stops
    schedule = schedule.sort_values(by=['trip_id', 'stop_sequence'])

    num_scheduled_arrivals = schedule.shape[0]

    # Print the number of scheduled arrivals
    print(f"Number of scheduled arrivals for route {route_short_name} (route_id: {route_id}): {num_scheduled_arrivals}")

    # Print the schedule
    print(f"Schedule for route {route_short_name} (route_id: {route_id}):")
    print(schedule[['trip_id', 'stop_id', 'arrival_time', 'departure_time', 'stop_sequence']])

    # save schedule[['trip_id', 'stop_id', 'arrival_time', 'departure_time', 'stop_sequence']] to csv
    schedule[['trip_id', 'stop_id', 'arrival_time', 'departure_time', 'stop_sequence']].to_csv(route_short_name + "-schedule.csv", index=False)

# # Print the route_id(s) for the given route_short_name
# print(f"Route ID(s) for route_short_name {route_short_name}:")
# print(route[['route_id', 'route_short_name', 'route_long_name']])