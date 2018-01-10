
# coding: utf-8

# # 3MV Data Processing
# ### LGR/ABB

import shutil,os,csv
import pandas as pd
import numpy as np
from datetime import datetime as dt

#scaling factor for waypoint amplitude
scale = 5

#threshold concentration value
ppm_thresh = 3

#while loop condition
looper = 1

while looper == 1:
    print('-----------------------------------------------------------------')

    #prompt user for filepath for 'data.csv' file
    filepath = input('What is the filepath of your data file? ')
    print('-----------------------------------------------------------------')

    #merged files will process differently (header is one row down)
    pandas_type = input('Is this an unmerged file (y/n)? ')
    if pandas_type.lower() == 'y' or pandas_type.lower() == 'yes' or pandas_type == "":
        heading = 0
    else:
        heading = 1
    print('-----------------------------------------------------------------')

    #extract potential folder name from file path
    split_filepath = filepath.split('\\')
    foldername = split_filepath[-1]

    #prompt user for folder name
    folder_type = input("Is '"+foldername+"' an acceptable folder name (y/n)? ")
    if folder_type.lower() == 'y' or folder_type.lower() == 'yes' or folder_type == "":
        True
    else:
        foldername = input("What would you like to name your folder? ")
    print('-----------------------------------------------------------------')

    #create kml file names
    kml_name = foldername+" CV"
    above_kml_name = kml_name + " Above"+str(ppm_thresh)+"ppm"

    #read in raw data csv   
    rawdata = filepath+'\\data.csv'
    df = pd.read_csv(rawdata,header=heading,low_memory=False)

    #delete empty rows splitting merged drive package data
    empty_values = np.where(pd.isnull(df['Time']))
    split_rows = np.unique(empty_values[0])

    for row in split_rows:
        df = df.drop(row)
        df = df.drop(row+1)
        
    #extract relevant columns into lists
    methane = [float(ppm) for ppm in df["[CH4]_ppm"].tolist()]
    amplitude = [ppm*scale for ppm in methane]

    ethane = [float(ppm) for ppm in df["[C2H6]_ppm"].tolist()]
    #ethane_amp = [ppm*scale for ppm in ethane]

    time_ = df["Time"].tolist()
    lat = df["Latitude (deg)"].tolist()
    long = df["Longitude (deg)"].tolist()
    temp = [float(temperature) for temperature in df["Temperature (C)"].tolist()]
    wind = [float(value)*2.23694 for value in df['Wind Speed (m/s)'].tolist()]

    #parse the date-time data
    time = []

    #let's assume canvassing was completed in the same day,
    #so we will assign the 'date' only once, outside of the loop
    date_time = dt.strptime(time_[0],"%m/%d/%Y %H:%M:%S.%f")
    date = date_time.strftime("%m/%d/%y")

    #number of data points or 'length' of data
    len_of_data = len(methane)

    #kml parameters
    madeby = 'SoCalGas, Sungwon Byun'
    icon = 'http://maps.google.ca/mapfiles/kml/pal2/icon26.png'
    text = '<![CDATA[<div style="font-family:Arial,sans-serif; min-width:200px;"><h3>$[name]</h3> <div style="margin-top:8px;">$[description]</div></div>]]>'
    hotSpot = 'x="0.5" y="0.5" xunits="fraction" yunits="fraction"'
    width = '0.3' #width of waypoint in GE

    #assign octa-decimal colors
    red = 'ff0000ff'
    green = 'ff73e600'

    kml_file = kml_name+'.kml'
    above_kml_file = above_kml_name+'.kml'   

    #open both csv's to begin writing in
    with open(kml_file,'w') as csv:
        with open(above_kml_file,'w') as csv3:
            csv.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
            csv.write('<Folder>\n<name>'+kml_name+'</name>\n<Document>\n<name>'+kml_name+'</name>\n<visibility>0</visibility>\n<Snippet maxLines="2">'+madeby+'</Snippet>\n<StyleMap id="gv_waypoint">\n<Pair>\n<key>normal</key>\n<styleUrl>#gv_waypoint_normal</styleUrl>\n</Pair>\n<Pair>\n<key>highlight</key>\n<styleUrl>#gc_waypoint_highlight</styleUrl>\n</Pair>\n</StyleMap>\n')
            csv.write('<Style id="gv_waypoint_normal">\n<IconStyle>\n<scale>0.25</scale>\n<Icon>\n<href>'+icon+'</href>\n</Icon>\n<hotSpot '+hotSpot+'/>\n</IconStyle>\n<LabelStyle>\n<scale>0</scale>\n</LabelStyle>\n<BalloonStyle>\n<text>'+text+'</text>\n</BalloonStyle>\n</Style>\n')
            csv.write('<Style id="gv_waypoint_normal">\n<IconStyle>\n<scale>0.3</scale>\n<Icon>\n<href>'+icon+'</href>\n</Icon>\n<hotSpot '+hotSpot+'/>\n</IconStyle>\n<LabelStyle>\n<scale>0</scale>\n</LabelStyle>\n<BalloonStyle>\n<text>'+text+'</text>\n</BalloonStyle>\n</Style>\n')
            csv.write('<Style id="gv_legend">\n<IconStyle>\n<Icon>\n<href>http://maps.google.com/mapfiles/kml/pal2/icon26.png</href>\n</Icon>\n</IconStyle>\n</Style>\n')
            csv.write('<Folder id="Waypoints">\n<visibility>0</visibility>\n')
            
            csv3.write('<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
            csv3.write('<Folder>\n<name>'+kml_name+' Above '+str(ppm_thresh)+' ppm</name>\n<Document>\n<name>'+kml_name+' Above '+str(ppm_thresh)+' ppm</name>\n<visibility>0</visibility>\n<Snippet maxLines="2">'+madeby+'</Snippet>\n<StyleMap id="gv_waypoint">\n<Pair>\n<key>normal</key>\n<styleUrl>#gv_waypoint_normal</styleUrl>\n</Pair>\n<Pair>\n<key>highlight</key>\n<styleUrl>#gc_waypoint_highlight</styleUrl>\n</Pair>\n</StyleMap>\n')
            csv3.write('<Style id="gv_waypoint_normal">\n<IconStyle>\n<scale>0.25</scale>\n<Icon>\n<href>'+icon+'</href>\n</Icon>\n<hotSpot '+hotSpot+'/>\n</IconStyle>\n<LabelStyle>\n<scale>0</scale>\n</LabelStyle>\n<BalloonStyle>\n<text>'+text+'</text>\n</BalloonStyle>\n</Style>\n')
            csv3.write('<Style id="gv_waypoint_normal">\n<IconStyle>\n<scale>0.3</scale>\n<Icon>\n<href>'+icon+'</href>\n</Icon>\n<hotSpot '+hotSpot+'/>\n</IconStyle>\n<LabelStyle>\n<scale>0</scale>\n</LabelStyle>\n<BalloonStyle>\n<text>'+text+'</text>\n</BalloonStyle>\n</Style>\n')
            csv3.write('<Style id="gv_legend">\n<IconStyle>\n<Icon>\n<href>http://maps.google.com/mapfiles/kml/pal2/icon26.png</href>\n</Icon>\n</IconStyle>\n</Style>\n')
            csv3.write('<Folder id="Waypoints">\n<visibility>0</visibility>\n')
        
            last_progress = 0
            print('Processing all data... Please wait...')
            print('-----------------------------------------------------------------')
            print('Progress: 0%')

            #begin for-loop for each data point
            for count in range(len_of_data):
                
                #progress counter
                progress = (count/len_of_data)*100
                if progress % 5 < 0.5:
                    progress = round(progress)
                    if progress != last_progress:
                        progress_counter = 'Progress: '+str(progress)+'%'
                        print(progress_counter)
                last_progress = progress
                
                #date_time and temp_time are temporary variables the for loop.
                #this loop will parse the date-time data into separate
                date_time = dt.strptime(time_[count],"%m/%d/%Y %H:%M:%S.%f")
                temp_time = date_time.strftime("%I:%M:%S.%f")[:-3]
                meridiem = date_time.strftime("%p")
                temp_time = temp_time + " " + meridiem
                time.append(temp_time)

                #assign current-loop values to variables (for convenience)
                meth = str(round(methane[count],3))
                eth = str(round(ethane[count],3))
                wind_ = str(round(wind[count],3))
                temp_ = str(round(temp[count],3))
                long_ = str(long[count])
                lat_ = str(lat[count])
                amplitude_ = str(amplitude[count])
                    
                #color-code
                if methane[count] < ppm_thresh:
                    color = green
                else:
                    color = red
                    #html for each point
                    csv3.write('<Placemark>\n<name>'+meth+' ppm</name>\n<visibility>0</visibility>\n<description><![CDATA['+time[count]+' <br> CH4 = '+meth+' ppm <br> C2H6 = '+eth+' ppm <br> Wind speed = '+wind_+' mph <br> Temperature = '+temp_+'°C]]></description>\n<styleUrl>#gv_waypoint</styleUrl>\n<Style>\n<IconStyle>\n<color>'+color+'</color>\n</IconStyle>\n<LabelStyle>\n<color>'+color+'</color>\n</LabelStyle>\n<LineStyle>\n<color>'+color+'</color>\n<width>'+width+'</width>\n</LineStyle>\n</Style>\n<Point>\n<extrude>1</extrude>\n<altitudeMode>relativeToGround</altitudeMode>\n<coordinates>'+long_+','+lat_+','+amplitude_+'</coordinates>\n</Point>\n</Placemark>\n')
        
                #html for each point
                csv.write('<Placemark>\n<name>'+meth+' ppm</name>\n<visibility>0</visibility>\n<description><![CDATA['+time[count]+' <br> CH4 = '+meth+' ppm <br> C2H6 = '+eth+' ppm <br> Wind speed = '+wind_+' mph <br> Temperature = '+temp_+'°C]]></description>\n<styleUrl>#gv_waypoint</styleUrl>\n<Style>\n<IconStyle>\n<color>'+color+'</color>\n</IconStyle>\n<LabelStyle>\n<color>'+color+'</color>\n</LabelStyle>\n<LineStyle>\n<color>'+color+'</color>\n<width>'+width+'</width>\n</LineStyle>\n</Style>\n<Point>\n<extrude>1</extrude>\n<altitudeMode>relativeToGround</altitudeMode>\n<coordinates>'+long_+','+lat_+','+amplitude_+'</coordinates>\n</Point>\n</Placemark>\n')
            
            #finish writing csv's
            csv.write('</Folder>\n</Document>\n</Folder>\n</kml>')
            csv3.write('</Folder>\n</Document>\n</Folder>\n</kml>')
            print('Progress: 100%')
     
    print('-----------------------------------------------------------------')
    print("'"+kml_file+"' created.")
    print("'"+above_kml_file+"' created.")

    #Move files with error handling
    try:
        os.mkdir(kml_name)
        print("'"+kml_name+"' folder created.")
        print('-----------------------------------------------------------------')
        shutil.move(kml_file,kml_name)
        print("'"+kml_name+"' >> '"+kml_file+"'")

        shutil.move(above_kml_file,kml_name)
        print("'"+kml_name+"' >> '"+above_kml_file+"'")
        print('-----------------------------------------------------------------')

        shutil.move(kml_name,filepath)
        print('Moved Curtain View (CV) folder to original raw data folder:')
        print("'" + foldername + "' >> '" + kml_name + "'")
        print('-----------------------------------------------------------------')
    except:
        print("Encountered errors moving files/folders")
        print('-----------------------------------------------------------------')

    
    continue_loop = input('Would you like to process more data (y/n)? ')
    if continue_loop.lower() == 'y' or continue_loop.lower() == 'yes' or continue_loop == "":
        looper = 1
    else:
        looper = 0

print('-----------------------------------------------------------------')