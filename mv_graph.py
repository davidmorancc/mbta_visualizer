#!/usr/bin/env python
#########################################################################################
#	mv_graph																			#
#  	This utility runs the airport utility included on OSX and parses the output to		#
#	include mac, ssid, and rssi															#
#########################################################################################

#sets the bg color
background_color 	= '#000000'
#default color table
color_table = 'orange'

#sets the color tables
color_table_orange = ['#e8b999','#e8a87b','#e89960','#e88846','#e87424','#e86b15']
color_table_blue = ['#004490','#104c90','#205490','#305e90','#406490','#506d90']
color_table_red = ['#e00d0c','#e02726','#e04948','#e06766','#e08080','#e09b9b']
color_table_green = ['#008445','#12824d','#258155','#38815e','#4f7f68','#5f7e6f']

import matplotlib.pyplot as plt
from mv_database import database_get_latest_vehicle
import os
import time
import random, sys,  getopt
import numpy as np
from matplotlib.animation import FuncAnimation

lat 	= []
lon 	= []
rssi 	= []

route 	= ''

fig, ax = plt.subplots()
fig.set_tight_layout(True)
plots = ax.scatter(0,0)

#parse out our command line arguments
def parse_arg(argv):
	global route
	global color_table
	route = '%'
	try:
		opts, args = getopt.getopt(argv,"h:r:c",["help","route=","color="])
	except getopt.GetoptError:
		print 'mv_graph.py --route=<routeid>[,<routeid2>,...]'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'wmv_graph.py --route=<routeid>[,<routeid2>,...]'
			sys.exit()
		elif opt in ("-r", "--route"):
			route = arg	
		elif opt in ("-c", "--color"):
			color_table = arg	

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

#gets the color for the specified strength based on the color_table specified in the options or arguments
def get_colortable(color_number):
	if color_table == 'orange':	
		return color_table_orange[color_number]
	if color_table == 'green':	
		return color_table_green[color_number]
	if color_table == 'blue':	
		return color_table_blue[color_number]
	if color_table == 'red':	
		return color_table_red[color_number]		

def get_line_color(rssi):
	rssi = abs(mean(rssi))
	
	if rssi <= 50:
		line_color = get_colortable(0)
	elif rssi <= 60:
		line_color = get_colortable(1)
	elif rssi <= 70:
		line_color = get_colortable(2)
	elif rssi <= 80:
		line_color = get_colortable(3)
	elif rssi <= 90:
		line_color = get_colortable(4)
	elif rssi <= 100:
		line_color = get_colortable(5)
		
	return line_color
	
def update(age):

	global plots
	lat = []
	lon = []
	#get a list of all seen macs
	for vehicle in database_get_latest_vehicle(route,age):

		#get all the log entries for a single mac
		lat.append(vehicle[6])
		lon.append(vehicle[7])
		print "PLOTTING - Vehicle ID: ",vehicle[2]
	plots.remove()		
	#take the lat and long lists and plot them
	plots = ax.scatter(lon, lat, color = '#406490', alpha = 0.4)
	
	print "LOOP: ",age
	return plots

if __name__ == "__main__":
	#parse the arguments
	parse_arg(sys.argv[1:])

	fig = plt.figure(facecolor = background_color)
	ax = plt.Axes(fig, [0., 0., 1., 1.], )
	ax.set_aspect('equal')
	ax.set_axis_off()
	fig.add_axes(ax)
	
	print "Route set to:",route,"\tColor set to:",color_table

	#added the two stage skip
	anim = FuncAnimation(fig, update, frames=np.arange(1, 2880), interval=16)
	#plt.show()
	
	#create the graph and save
	timestamp = int(time.time())
	filename = 'output/mv_' + str(timestamp) +'.mp4'
	anim.save(filename, dpi=500, writer='ffmpeg')
	
	print "Route set to:",route,"\tColor set to:",color_table
	
	#opens the file we just created in the os default program
	print "Opening File..."
	os.system("open "+filename)

	#create the graph and save
	#timestamp = int(time.time())
	#filename = 'output/wifi_tracks_' + str(timestamp) +'.png'
	#plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=1000)

	#opens the file we just created in the os default program
	#print "Opening File..."
	#os.system("open "+filename)

