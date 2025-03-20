class Node:
    def __init__(self, label, properties):
        self.label = label
        self.properties = properties

class Relationship:
    def __init__(self, start_node, end_node, type):
        self.start_node = start_node
        self.end_node = end_node
        self.type = type

trip_node = Node("Trip", [
    "trip_duration",
    "rideable_type"
])

station_node = Node("Station", [
    "station_id",
    "station_name",
    "latitude",
    "longitude",
    "city",
    "landmark",
    "dpcapacity"
])

rider_node = Node("Rider", [
    "usertype",
    "gender",
    "age"
])

time_node = Node("Time", [
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "second"
])

starts_at = Relationship(trip_node, station_node, "STARTS_AT")
ends_at = Relationship(trip_node, station_node, "ENDS_AT")
taken_by = Relationship(trip_node, rider_node, "TAKEN_BY")
occurs_on = Relationship(trip_node, time_node, "OCCURS_ON")

print("Nodes:")
for node in [trip_node, station_node, rider_node, time_node]:
    print(f" {node.label}: {', '.join(node.properties)}")

print("\nRelationships:")
for rel in [starts_at, ends_at, taken_by, occurs_on]:
    print(f" ({rel.start_node.label})-[{rel.type}]->({rel.end_node.label})")