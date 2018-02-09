# test_netAngels
test

# Common comments
1. Implemented as a web-service with a web-client and api.
2. Selected simple shorting link method (not specified in the task)
3. Unit testing was not applied (there is not in the task and too simple task).
4. Deploy work was not performed (not specified in the task).
5. A pre-installed MySQL Server 5.5 database was used: 
	to migrate models and working with db, you need to have a db available according with settings.py:

# Test data for db
You can fill db by pressing button "Fill with test links" on main menu of web-client application.

# For api using
You can make link shorter by sending POST request to /api/v1/code/ with body like {"url": "http://long_link.com"}
>> In response you got data like {"hash": "156464512"}
P.S.: This api POST request reversable
