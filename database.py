#!/usr/bin/env python
#########################################################################################
#	wt_database																			#
#  	This utility is to handle the database setup and read/writing						#
#	Accepts the command line arguments 'create' and 'empty' to handle setting up a new  #
#	database if the file gets delete and clearing out the database after exporting data #
#########################################################################################

import sqlite3
import sys
import time

connection = sqlite3.connect('db/data.db')
database = connection.cursor()

#function to create a new database and setup the tables
def database_create():	
	#create our table
	database.execute('''CREATE TABLE `vehicle` (
	`id`					INTEGER PRIMARY KEY AUTOINCREMENT,
	`timestamp`				INTEGER,
	`vehicle_id`			TEXT,
	`vehicle_name`			TEXT,
	`vehicle_route`			TEXT,
	`vehicle_direction`		INTEGER,
	`vehicle_lat`			REAL,
	`vehicle_lon`			REAL,
	`vehicle_bearing`		INTEGER,
	`vehicle_timestamp`		INTEGER,
	`vehicle_trip_start`	INTEGER,
	`vehicle_trip_id`		INTEGER
	);''')
	
	#go ahead commit the database
	connection.commit()
	
	print "Created new database and commited"
	
	return
	
#function to empty the database
def database_empty():
	database.execute("DELETE FROM vehicle")
	database.execute("VACUUM")
	connection.commit()
	
	print "Cleared database and commited"
	return

#vehicle_id, vehicle_name, vehicle_route, vehicle_direction, vehicle_lat, vehicle_lon, vehicle_bearing, vehicle_timestamp, vehicle_trip_start, vehicle_trip_id
def database_insert(vehicle_id, vehicle_name, vehicle_route, vehicle_direction, vehicle_lat, vehicle_lon, vehicle_bearing, vehicle_timestamp, vehicle_trip_start, vehicle_trip_id):
	database.execute("INSERT INTO vehicle (timestamp, vehicle_id, vehicle_name, vehicle_route, vehicle_direction, vehicle_lat,	vehicle_lon, vehicle_bearing, vehicle_timestamp, vehicle_trip_start, vehicle_trip_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (time.time(), vehicle_id, vehicle_name, vehicle_route, vehicle_direction, vehicle_lat,vehicle_lon, vehicle_bearing, vehicle_timestamp, vehicle_trip_start, vehicle_trip_id))
	return
	
#commit and close the database	
def database_close():	
	connection.commit()
	connection.close()
	return
	
#commit and close the database	
def database_commit():	
	connection.commit()
	return 
	
#returns a list of all the entries for the given mac address
def database_search_mac(mac, route):
	database.execute("SELECT route,mac,ssid,rssi,lat,long,alt,time FROM log WHERE mac = ? AND route LIKE ?",(mac,route,))
	rows = database.fetchall()
	return rows

#returns a list of all mac addresses found	
def database_get_macs(route):	
	rows = []
	for line in route.split(","):
		database.execute("SELECT DISTINCT mac, '"+line+"' FROM log WHERE route LIKE ?", (line,))
		rows = rows + database.fetchall()
	return rows

def database_get_ssid():	
	database.execute("SELECT count (DISTINCT ssid) FROM log")
	return (database.fetchall()[0][0])

#prints a list of all routes found	
def database_get_routes():	
	database.execute("SELECT DISTINCT route FROM log")
	for route in database.fetchall():
		print route[0]
	return 
	
#returns a list of all ssids found for the route given
def database_get_ssids(route):	
	rows = []
	for line in route.split(","):
		database.execute("SELECT ssid, count(ssid) FROM log WHERE route LIKE ? GROUP BY ssid", (line,))
		rows = rows + database.fetchall()
	return rows

if __name__ == "__main__":
	
	#setup the command line arguments create and empty
	for arg in sys.argv:
		if arg == "create":
			database_create()
		if arg == "empty":
			database_empty()
	database_close()


