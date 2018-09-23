from datetime import datetime, timedelta
from ComputeLTV import Ingest,TopXSimpleLTVCustomers,computeWeek,WriteTopX


expected_result = "8weeks"
assert computeWeek('2017-03-05T12:46:46.384Z' ,'2017-01-06T12:46:46.384Z') == expected_result
print ("test passed " + "computeWeek('2017-03-05T12:46:46.384Z' ,'2017-01-06T12:46:46.384Z')  ")
expected_result = "10weeks"
assert computeWeek( '2017-03-15T12:46:46.384Z','2017-01-06T12:46:46.384Z') == expected_result
print ("test passed " + "computeWeek('2017-03-15T12:46:46.384Z','2017-01-06T12:46:46.384Z')  ")
expected_result = "11weeks"
assert computeWeek('2017-03-25T12:46:46.384Z','2017-01-06T12:46:46.384Z') == expected_result
print ("test passed " + "computeWeek('2017-03-25T12:46:46.384Z','2017-01-06T12:46:46.384Z')  ")
expected_result = "13weeks"
assert computeWeek( '2017-04-05T12:46:46.384Z','2017-01-06T12:46:46.384Z') == expected_result
print ("test passed" + " computeWeek('2017-04-05T12:46:46.384Z','2017-01-06T12:46:46.384Z')  ")

