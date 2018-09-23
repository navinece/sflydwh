from datetime import datetime, timedelta
from ComputeLTV import Ingest,TopXSimpleLTVCustomers,computeWeek,WriteTopX,SortGetTopX


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

actual_result_list = [ [ '96f55c7d8f50',1,5.1, 3000.0, '1 week'],[ '96f55c7d8f48',1,5.1, 2652.0, '1 week']]
expected_result_list = [ [ '96f55c7d8f50',1,5.1, 3000.0, '1 week']]
assert SortGetTopX(actual_result_list,1) == expected_result_list
print ("test passed " + "SortGetTopX function sorted the list and retrieved Top 1 simpleLTV")

actual_result_list = [ [ '96f55c7d8f50',1,5.1, 3000.0, '1 week'],[ '96f55c7d8f48',1,5.1, 2652.0, '1 week'],[ '96f55c7d8f52',1,5.1, 12652.0, '1 week'] ]
expected_result_list = [ [ '96f55c7d8f50',1,5.1, 3000.0, '1 week'],[ '96f55c7d8f52',1,5.1, 12652.0, '1 week']]
assert SortGetTopX(actual_result_list,2) == expected_result_list
print ("test passed " + "SortGetTopX function sorted the list and retrieved Top 2 simpleLTV")

actual_result_list = [ [ '96f55c7d8f50',1,5.1, 3000.0, '1 week'],[ '96f55c7d8f48',1,5.1, 2652.0, '1 week'],[ '96f55c7d8f52',1,5.1, 12652.0, '1 week'] ]
expected_result_list = [ [ '96f55c7d8f48',1,5.1, 2652.0, '1 week'], [ '96f55c7d8f50',1,5.1, 3000.0, '1 week'],[ '96f55c7d8f52',1,5.1, 12652.0, '1 week']]
assert SortGetTopX(actual_result_list,3) == expected_result_list
print ("test passed " + "SortGetTopX function sorted the list and retrieved Top 3 simpleLTV")

actual_result_list = [ [ '96f55c7d8f52',1,5.1, 12652.0, '1 week'],[ '96f55c7d8f55',1,5.1, 0.0, '1 week'],[ '96f55c7d8f58',1,5.1, 0.0, '1 week'],[ '96f55c7d8f50',1,5.1, 3000.0, '1 week'],[ '96f55c7d8f48',1,5.1, 2652.0, '1 week'] ]
expected_result_list = [ [ '96f55c7d8f55',1,5.1, 0.0, '1 week'],[ '96f55c7d8f58',1,5.1, 0.0, '1 week'], [ '96f55c7d8f48',1,5.1, 2652.0, '1 week'], [ '96f55c7d8f50',1,5.1, 3000.0, '1 week'],[ '96f55c7d8f52',1,5.1, 12652.0, '1 week']]
assert SortGetTopX(actual_result_list,5) == expected_result_list
print ("test passed " + "SortGetTopX function sorted the list and retrieved Top 5 simpleLTV")