from google.transit import gtfs_realtime_pb2
from database import database_insert
from database import database_close
from database import database_commit

import urllib


feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.urlopen('http://developer.mbta.com/lib/GTRTFS/Alerts/VehiclePositions.pb')
feed.ParseFromString(response.read())


for entity in feed.entity:
	if entity.HasField('vehicle'):
		print "\nVehicle Route:\t",entity.vehicle.trip.route_id
		print "Vehicle Name:\t",entity.vehicle.vehicle.label
		print "Vehicle ID:\t",entity.vehicle.vehicle.id
		print "Direction:\t",entity.vehicle.trip.direction_id
		print "Trip ID:\t",entity.vehicle.trip.trip_id
		print "Trip Start:\t",entity.vehicle.trip.start_date
		print "Latitude:\t",entity.vehicle.position.latitude
		print "Longitude:\t",entity.vehicle.position.longitude
		print "Bearing:\t",entity.vehicle.position.bearing
		print "Timestamp:\t",entity.vehicle.timestamp
		
		database_insert(entity.vehicle.vehicle.id, entity.vehicle.vehicle.label, entity.vehicle.trip.route_id, entity.vehicle.trip.direction_id, entity.vehicle.position.latitude, entity.vehicle.position.longitude, entity.vehicle.position.bearing, entity.vehicle.timestamp, entity.vehicle.trip.start_date, entity.vehicle.trip.trip_id)
		
	database_commit()

database_close()

	
	
	