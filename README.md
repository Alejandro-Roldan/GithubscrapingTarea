A GITHUB CRAWLER THAT IMPLEMENTS THE GITHUB SEARCH AND RETURNS ALL THE
LINKS FROM THE SEARCH RESULT.

``` python >= 3.9.6 ```
``` beautifulsoup4 >= 4.9.3 ```
``` requests >= 2.26.0 ```

Usage:
```python
	from githubscraping import scrapeMain

	output = scrapeMain('/path/to/input/json', '/path/to/output/json')
	# print(output)

```
	


Input must be a json file of the form:
```json
	{
		"keywords": [
		  "openstack",
		  "nova",
		  "css"
		],
		"proxies": [
		  "202.14.80.2:3128",
		  "116.203.23.252:3128"
		],
		"type": "Repositories"
	}

```
	
Output will be a json file with a list of urls to the found repositories.
When searching for repositories it will also have the extra data of owner
and languages (and percentage) used in the repository

Free Proxies are slow and unreliable. If they can't connect and give an
error: try again.


You can find the test results inside ./htmlcov

To re-run the tests make sure to have coverage python module installed
``` pip install coverage ```

and then run
```
	$ cd /path/to/Githubscraping

	$ coverage run githubscraping_test.py

	$ coverage report

	$ coverage html

```

Proxies may fail or hang, failing the first 2 tests that use them
Retry running
