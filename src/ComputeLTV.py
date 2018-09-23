

from datetime import datetime, timedelta

# Ingest(events,eventsDataDict) - This method is used for ingesting the data into the data dictionary eventsDataDict. Accepts two parameters events json file and empty data dictionary eventsDataDict.
# After sucessfully ingesting the data, the method returns back the eventsDataDict as an input to the next method for further computing the simpleLTV value.
def Ingest(events,eventsDataDict):
    for i in events:

        if i['type'] == 'CUSTOMER':
            customer_id = i['key']
            event_time = i['event_time']
            event_type = 'CUSTOMER'

            eventsDataDict[customer_id, event_time, event_type] = [customer_id, event_time, event_type, i['verb'], i['last_name'],
                                                         i['adr_city'], i['adr_state']]

        elif i['type'] == 'SITE_VISIT':
            customer_id = i['customer_id']
            event_time = i['event_time']
            event_type = 'SITE_VISIT'
            eventsDataDict[customer_id, event_time, event_type] = [customer_id, event_time, event_type, i['verb'], i['key'], '1']

        elif i['type'] == 'IMAGE':
            customer_id = i['customer_id']
            event_time = i['event_time']
            event_type = 'IMAGE1'
            eventsDataDict[customer_id, event_time, event_type] = [customer_id, event_time, event_type, i['verb'], i['key'],
                                                         i['camera_make'], i['camera_model']]

        elif i['type'] == 'ORDER':
            customer_id = i['customer_id']
            event_time = i['event_time']
            event_type = 'ORDER'
            #the dollar amount in the event is 12.34 USD. hence the split function is applied on the dollar_amount field and only the float amount is retrieved from events.
            dollar_amount = i['total_amount'].split(" ")[0]
            eventsDataDict[customer_id, event_time, event_type] = [customer_id, event_time, event_type, i['verb'], i['key'],
                                                         dollar_amount]

        else:
            print ( "Warning: New events are being Ingested or Incorrect event types are present in the file !. Please check ")
    return eventsDataDict



def computeWeek(maxdate,mindate):
 #max event_timestamp from each customer_id call while intialising the dictionary ltvdict
 maxDate =   datetime.strptime( maxdate, '%Y-%m-%dT%H:%M:%S.%fZ').date()
 #min event_timestamp from each customer_id call while intialising the dictionary ltvdict
 minDate=   datetime.strptime(mindate, '%Y-%m-%dT%H:%M:%S.%fZ').date()
 #calculating the monday from the max date and min dates
 monday2 = (maxDate - timedelta(days=maxDate.weekday()))
 monday1 = (minDate - timedelta(days=minDate.weekday()))
 num_of_weeks = (monday2 - monday1).days / 7
 if  num_of_weeks == 0 or num_of_weeks == 1 :
     return '1' + 'week'
 else:
     return  str ((monday2 - monday1).days / 7 ) + 'weeks'


def TopXSimpleLTVCustomers(topXcustomers, eventsdatadict):
    ltvdict = {}
    t=10;


  #intialises the empty dictionary ltvdict and iterates through event data dictionary for customer event type and creates the dictionary ltvdict with dict[customer_id] = list[event_timestamp].
    #after this step, dict ltvdict is re-intialised with values [0, 0.0, 0.0, computeWeek(max(ltvdict[customer_id]), min(ltvdict[customer_id]))]. the above step of
    #  populating  all the event timestamps is needed to compute the max and min event timestamps for each customer_id key and finally the duration by calling the function computeweek (max,min)

    for i in eventsdatadict:
        if i[2] == "CUSTOMER":
            customer_id = eventsdatadict[i][0]
            ltvdict[customer_id] = ltvdict.get(customer_id, []) + [eventsdatadict[i][1]]

    # print ltvdict - sample output
    # { u'96f55c7d8f70': [u'2017-01-07T12:46:46.384Z'], u'96f55c7d8f42': [u'2017-01-06T12:46:46.384Z'], u'96f55c7d8f62': [u'2017-01-07T12:46:46.384Z'],
    # u'96f55c7d8f54': [u'2017-02-07T12:46:46.384Z', u'2017-01-08T12:46:46.384Z', u'2017-01-07T12:46:46.384Z'] }

    for customer_id in ltvdict:
        ltvdict[customer_id] = [0, 0.0, 0.0, computeWeek(max(ltvdict[customer_id]), min(ltvdict[customer_id]))]

    # print ltvdict - sample output
    # {u'96f55c7d8f70': [0, 0.0, 0.0,'1week'], u'96f55c7d8f42': [0, 0.0, 0.0,'1week'], u'96f55c7d8f62': [0, 0.0, 0.0, 1week']}





    # Computes the Total_number of visits by iterating through the site_visit event in the eventsdatadict data dictionary and computing the total number of visits for each customer
    # by incrementing the Total_number of visits values in the ltvdict[customer_id][0] ltv dictionary.
    # Computes the Total_Dollar_amount by iterating through the Order event in the eventsdatadict data dictionary and computing the total dollar amount spent
    # by each customer by summing up the dollar amount values in the ltvdict[customer_id][1] ltv dictionary.

    for i in eventsdatadict:
        if i[2] == "SITE_VISIT":
            customer_id = eventsdatadict[i][0]
            number_of_visits = int(eventsdatadict[i][5])
            ltvdict[customer_id][0] = ltvdict[customer_id][0] + number_of_visits

        elif i[2] == "ORDER":
            customer_id = eventsdatadict[i][0]
            dollar_amount_spent = eventsdatadict[i][5]
            ltvdict[customer_id][1] = ltvdict[customer_id][1] + float(dollar_amount_spent)


    #print ltvdict
    # sample output after populating dollar amounts + total visit + timeframes for each customer
    # { u'96f55c7d8f56': [1, 5.1, 0.0, '1 week'], u'96f55c7d8f48': [1, 12.34, 0.0, '1 week'], u'96f55c7d8f54': [3, 23.14, 0.0, '5 weeks'], u'96f55c7d8f60': [1, 2.3, 0.0, '1 week']}
    # [[u'96f55c7d8f54', 3, 23.14, 36098.4, '5 weeks']}




   #Once above steps is completed in brute force techinque, the simpleLTv is calculated by iterating through the ltvdict dictionary and the formula 52(Total_Number_of_Site_visits * Total_Dollar_amount) * t is calcuated for
   # each customer_id key in the dictionary ltvdict[customer_id][2] = 52 * ltvdict[customer_id][1] * ltvdict[customer_id][0] * t
    for i in ltvdict:
        customer_id = i;
        ltvdict[customer_id][2] = 52 * ltvdict[customer_id][1] * ltvdict[customer_id][0] * t

    # print ltvdict
    # sample output after populating dollar amounts + total visit + Finaltv + timeframes for each customer
    # {u'96f55c7d8f56': [1, 5.1, 2652.0, '1 week'], u'96f55c7d8f48': [1, 12.34, 6416.799999999999, '1 week'], u'96f55c7d8f54': [3, 23.14, 36098.4, '5 weeks'], u'96f55c7d8f60': [1, 2.3, 1196.0, '1 week']}}


   #Once all the values are computed within the ltvdict dictionary , the dictinary is transformed into a list list[customer_id, Total_Number_of_Site_visits,Total_Dollar_amount,simpleLTV,Duration ) and
   # the list is sorted by the simpleLTV value in ascending order
  # and last 10 elements is sliced from the list and write method WriteTopX(ltvfinallist,topXcustomers) is invoked

    ltvfinallist = []

    for i in ltvdict:
        ltvfinallist.append([i, ltvdict[i][0], ltvdict[i][1], ltvdict[i][2], ltvdict[i][3]])


  #calls the SortGetTopX method to sort the list by simpleltv calculation and retrieve only top10 using the topXcustomers
    ltvfinallist = SortGetTopX(ltvfinallist, topXcustomers)
 # calls the WriteTopX method to write the final ouput into /tmp/output/YYYYMMDD_YYYYMMDDHHMMSS_SimpleLTV_TOP10_Customers.dat directory
    writestatus = WriteTopX(ltvfinallist,topXcustomers)
    print writestatus




def SortGetTopX(TopXCustomerList,topXcustomers):
    def getKey(item):
        return item[3]
    #this step sorts the list using simpleltv value
    TopXCustomerList = sorted(TopXCustomerList, key=getKey)
    ##this step slices last 10 which is the top 10 customers with highest simpleLTV
    TopXCustomerList= TopXCustomerList[-topXcustomers:]
    return TopXCustomerList


def WriteTopX(TopXCustomerList,topXcustomers):
    import datetime
    import time
    ts = time.time()
    currentDate = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')
    currenttimestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

    topXLTVCustomers = str(currentDate) + "_" + str(currenttimestamp) + "_SimpleLTV_TOP" + str(
        topXcustomers) + "_Customers.dat"

    #printing and writng the TOP10 simpleLTV customer details ltvfinallist

    f = open("/tmp/output/"+ topXLTVCustomers, "w")
    f.write("Customer_Id,Number_Of_Visits,Total_Order_amount, SimpleLTV, Duration\n")

    for i in range(len(TopXCustomerList)):
        f.write(str(TopXCustomerList[i][0]) + "," + str(TopXCustomerList[i][1]) + "," + str(TopXCustomerList[i][2]) + "," + str(TopXCustomerList[i][3]) + "," + str(TopXCustomerList[i][4])+ "\n");
    return  "\n\n\nTop" + str(topXcustomers) + " highest SimpleLTV customer report is complete and available in the directory /tmp/output/" + str(topXLTVCustomers) + " for your review"
