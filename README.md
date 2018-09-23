# sflydwh
This repository contains the python programs to calculate the Simple LTV for customer events collected at sfly websites

After analyisng the requirements, As a first step , based on the events collected i have started with the data modelling step and below are the design decisions for the same. 



Design Decision#1: Build a A single event table for all the event types collected at sfly websites.

Problem statement: Events types ( Customer,site_visit,image,order) collected at sfly websites needs to stored in a efficents and flexible Data model which will futher used for computing Simpleltv values for the customers. 

Design Solution: 
1. A single event table
2. The table contains the common attributes as keys. (customer_id,event_timestamp and event_type). 
3. As the Type of events grow, event table will be the single source for all calculations and can accomadate new events
4. new attributes can be added in JSON 




Design Decision#2: Build a A single event table for ingestion  - Dictionary,list data structures

Problem statement: Events types ( Customer,site_visit,image,order) collected at sfly websites needs to stored in efficent Data structure which has in-memory processing capabilities. 

Design solution: 

For the Ingestion, single eventdata dictionary data structure will be used to ingest all type of events collected at the sfly websites. 

Data model for eventsdata dictionary to ingest different events: 
Dictionary[key]   = List[values]
eventsdatadict[customer_id, event_time, event_type]  = List [ attributes of event ]

where customer_id is the customer's unique id to represent a customer 
event_time  is the timetstamp where the event is collected 
event_type - type of the event like customer,order,site_visit and image 

Definition for each events ingetsted into eventsdatadict dictionary  : 
Customer: eventsdatadict[customer_id, event_time, event_type]  = List [customer_id, event_time, event_type,verb,last_name,adr_city and adr_state]

Site_visit : eventsdatadict[customer_id, event_time, event_type]  = List [customer_id, event_time, event_type,verb,key(page_id), number_of_vists]
where in the python program, for each site_visit event, the python program defaults to a value of 1 for further computing the number of visits. 

order : eventsdatadict[customer_id, event_time, event_type]  = List [customer_id, event_time, event_type,verb,key(order_id), dollar_amount]
for dollar amount, while ingestion the python programs does a transformation to extract only the  dollar amounts (float data type) for further computing the total dollar amount of a customer. 

image : eventsdatadict[customer_id, event_time, event_type]  = List [customer_id, event_time, event_type,verb,key(image_id), camera_make,camera_model]
for dollar amount, while ingestion the python programs does a transformation to extract only the  dollar amounts (float data type) for further computing the total dollar amount of a customer. 

Assumptions: 

1. Whenever the customer visits sfly website, there will be customer and site_visit event created and sent for ingestion irrespective of the he makes an order/uploads a image.
2.Inline with above assumption, an order/Image upload event must have a coresponding customer/site_visit event. 
3. whenever the customer just visits sfly website and does not make an order/image upload, an order/image is not created and inline with our desing assumptions for the ingetsion module. 




Design Decision#3: Build a Dictionary for Simple LTV calcuation 

Problem statement: TOP 10 customers simpleLTV calcuations need to be calculated in efficent and in-memory Data structure. 

Design solution: 

For the Simple LTV, single "ltvdict" dictionary data structure will be created by extarcting the events information ingested into the eventsdatadict ingestion dictionary. Time complexity to build the "ltvdict" dictionary is O(N) and Space complexity is O(1) since we intialise the dictionary before computation. 

Definition for "ltvdict"  dictionary  :

ltvdict[customer_id]  = List [ Total_Number_of_Site_visits, Total_Dollar_amount, SimpleLTV, timeframe ]

where Total_Number_of_Site_visits is the total number of visits by the customer ingested into event data dictionary. Total_Number_of_Site_visits will be computed by incrementing by value of 1 for each customer visit in the python program. 

Total_Dollar_amount is the total Dollar amount spent by the customer ingested into event data dictionary. Total_Dollar_amount will be computed by summing up the dollar amounts in each order event the customer has placed.

SimpleLTV is the 52(Total_Number_of_Site_visits * Total_Dollar_amount ) * t. SimpleLTV is calculated after the ltvdict data dictionary for each customer is populated with the Total_Number_of_Site_visits and Total_Dollar_amount. 

timeframe is the number of weeks (SimpleLTV) for the customer events ingested into the event data dictionary. timeframe is caclauted by passing the max event timestamp and min event timestamp of the customer event type and number of weeks is computed. For week calculation monday to monday is considered as one week. 


Once the above dictionary is computed, the dictionary is transformed into a list (ltvfinallist)  and the list is sorted based on the SimpleLTV values in ascending order and last 10 elements (highest simplelTV)  is retrived from the list and written into the file. 





Technical Design specifactions: 

Wrapper.py  - Entry point for the ingestion of the events and calcuating the SimpleLTV values
steps to call Wrapper.py :
python wrapper.py 10 /tmp/input/events.dat 
where argument 1 is TopxcustomersReturn count
where argument 2 is Input events data file name with directory structure

before calling the python program, Please create the following directories in your Mac machine/Linux environment

1. create /tmp/input/ and download the events.dat file from github  i have uploaded and 
2. create /tmp/output and once the python program finishes - the final ouput file containing the Top 10 simpleltv calculations will be created in this directory in the format YYYYMMDD_YYYYMMDDHHMMSS_SimpleLTV_TOP10_Customers.dat

Exceptions handled: 
1. Input argument check - need to pass TopxcustomersReturn and input events data file to be ingested. 
2. Topxcustomer count should be greater than zero or not equal to 0

Methods called in the Wrapper.py: 

1. Ingest(events,eventsDataDict) - This method is used for ingesting the data into the data dictionary eventsDataDict. Accepts two parameters events json file and empty data dictionary eventsDataDict. 

After sucessfully ingesting the data, the method returns back the eventsDataDict as an input to the next method for further computing the simpleLTV value. 

2. TopXSimpleLTVCustomers(topXcustomers, eventsdatadict): - This Method is used for calcuating the simplelTV values for all the customers and finally writes the TOP10 Customers simplelTV value into the file in the format /tmp/output/YYYYMMDD_YYYYMMDDHHMMSS_SimpleLTV_TOP10_Customers.dat

Method spec: 
1. accepts the topXcustomerscount (10) and eventsdatadict data dictionary which contains the data ingested. 
2. Intialises a empty dictionary ltvdict ltvdict[customer_id]  = List [ Total_Number_of_Site_visits, Total_Dollar_amount, SimpleLTV, timeframe ]
3. Calls the method computeWeek(maxdate,mindate) to compute the duration of weeks which is max(event_timestamp) - min(event_timestamp) 
4. Computes the Total_number of visits by iterating through the site_visit event in the eventsdatadict data dictionary   and computing the total number of visits for each customer by incrementing the Total_number of visits values in the ltvdict[customer_id][0] ltv dictionary.
5.Computes the Total_Dollar_amount by iterating through the Order event in the eventsdatadict data dictionary   and computing the total dollar amount spent by each customer by summing up the dollar amount values in the ltvdict[customer_id][1] ltv dictionary.
6. Once step 4 and 5 is completed in brute force techinque, the simpleLTv is calculated by iterating through the ltvdict dictionary and the formula 52(Total_Number_of_Site_visits * Total_Dollar_amount) * t is calcuated for each customer_id key in the dictionary ltvdict[customer_id][2] = 52 * ltvdict[customer_id][1] * ltvdict[customer_id][0] * t

7.Once all the values are computed within the ltvdict dictionary , the dictinary is transformed into a list list[customer_id, Total_Number_of_Site_visits,Total_Dollar_amount,simpleLTV,Duration ) 
and the list is sorted by the simpleLTV value in ascending order and last 10 elements is sliced from the list and write method
WriteTopX(ltvfinallist,topXcustomers) is invoked to write the final top10simpleltv customers into the file in the /tmp/output/YYYYMMDD_YYYYMMDDHHMMSS_SimpleLTV_TOP10_Customers.dat


Unit tests: 

Unittest.py - steps to call
python Unittest.py  
1.Unit test for Compute weeks method.
2. unit tests for ingetsion method
3. unit test for sort method. 
4. Unit test for write method. 
















