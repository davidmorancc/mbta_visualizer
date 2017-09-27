from google.transit import gtfs_realtime_pb2
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
		print "Latitude:\t",entity.vehicle.position.latitude
		print "Longitude:\t",entity.vehicle.position.longitude
		print "Bearing:\t",entity.vehicle.position.bearing
		print "Timestamp:\t",entity.vehicle.timestamp

	
	
	