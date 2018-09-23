import sys
import json
from ComputeLTV import Ingest,TopXSimpleLTVCustomers

if len(sys.argv)!=3:
     print "Invalid Command"
     print "command to call the process:  python wrapper.py 10 /tmp/input/events.dat "
     print 'where argument 1 is TopxcustomersReturn count and argument 2 is Input events data file name with directory structure'
     exit(1)

eventsFilename=sys.argv[2]
TopXCustomers=int(sys.argv[1])



if TopXCustomers < 0 or  TopXCustomers == 0 :
	print 'Invalid TopXcustomercount: Enter a valid Number like 10 to get the SimpleLTV calculations for Top 10 Customers'
	exit(1)

#Loading the Input Events json data into the eventsData for further LTV calculations
with open (eventsFilename) as eventsData:
    eventsData=json.load(eventsData)
#intialising eventsdatadict and passing them to ingestmethod for laoding with the events collected at sfly websites.
eventsdatadict={}

# Ingest(events,eventsDataDict) - This method is used for ingesting the data into the data dictionary eventsDataDict. Accepts two parameters events json file and empty data dictionary eventsDataDict.
# After sucessfully ingesting the data, the method returns back the eventsDataDict as an input to the next method for further computing the simpleLTV value.
eventsdatadict= Ingest(eventsData,eventsdatadict)


#TopXSimpleLTVCustomers(topXcustomers, eventsdatadict): - This Method is used for calcuating the simplelTV values for all the customers and
# finally writes the TOP10 Customers simplelTV value into the file in the format /tmp/output/YYYYMMDD_YYYYMMDDHHMMSS_SimpleLTV_TOP10_Customers.dat
TopXSimpleLTVCustomers(TopXCustomers,eventsdatadict)

