import time,datetime
from django.test import TestCase

# Create your tests here.

print(time.time())
a = datetime.datetime.now()
print(time.mktime(a.timetuple()))
