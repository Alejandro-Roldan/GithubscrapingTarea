#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import random


###############################################################################
#
# A GITHUB CRAWLER THAT IMPLEMENTS THE GITHUB SEARCH AND RETURNS ALL THE
# LINKS FROM THE SEARCH RESULT.
#
# Minimal resources. Main bottleneck is internet connection
#
#   Usage:
#    from githubscraping import scrapeMain
#
#    output = scrapeMain('/path/to/input/json', '/path/to/output/json')
#    # print(output)
#
#
#   Input must be a json file of the form:
#    {
#     "keywords": [
#       "openstack",
#       "nova",
#       "css"
#     ],
#     "proxies": [
#       "202.14.80.2:3128",
#       "116.203.23.252:3128"
#     ],
#     "type": "Repositories"
#    }
#
#   Output will be a json file with a list of urls to the found repositories.
#   When searching for repositories it will also have the extra data of owner
#   and languages (and percentage) used in the repository
#
###############################################################################

#
# IMPORTANT: using the free proxies is as unreliable as you might expect:
# unreachable, slow...
#


#############
# FUNCTIONS #
#############

def jsonInput(input_file):
    ''' Parse input data into a dict '''
    with open(input_file, 'r') as file:
        data = json.load(file)
        data['type'] = data['type'].lower()

    return data

def jsonOutput(output_file, json_string):
    ''' Save output to json '''
    with open(output_file, 'w') as file:
        file.write(json_string)

def urlCreate(query, se_type):
    ''' Create URL from the keywords and the type '''
    # Create string from list of queried items
    query_str = '+'.join(query)
    # Create URL
    url = 'https://github.com/search?q=' + query_str + '&type=' + se_type

    return url

def proxier(proxy_lst):
    '''
        Select a random proxy from the list of provided proxies.
        Create the structure that requests uses for proxies.
        Return None if no proxy.
    '''
    if proxy_lst:
        # Get random item from the list
        rnd_proxy = random.choice(proxy_lst)

        # Request recent versions bug:
        # Need to add http:// or https:// to the proxies to work
        proxy = {
                    'http': 'http://' + rnd_proxy,
                    'https': 'http://' + rnd_proxy
                }
    # If list empty/no list: proxy is None
    else:
        proxy = None

    return proxy

def searchScrapper(url, se_type, proxy_lst):
    # Select proxy
    proxy = proxier(proxy_lst)

    # Access the page
    rsp=requests.get(url, proxies=proxy, stream=True)

    # IP used For Debugging, to make sure youre using a proxy
    #ip_msg = 'IP used: ' + str(rsp.raw._connection.sock.getpeername())
    #print(ip_msg)
    
    # Proccess the html
    soup = BeautifulSoup(rsp.content, 'html.parser')

    # Different searches for different types, since the returning list items
    # don't use the same structure
    # Repositories
    if se_type == 'repositories':
        searched = soup.find('ul', attrs={'class': 'repo-list'})
        items = searched.find_all('a', attrs={'class': 'v-align-middle'})
    # Issues
    elif se_type == 'issues':
        searched = soup.find('div', attrs={'class': 'issue-list'})
        items = searched.find_all('a', attrs={'class': 'Link--muted text-bold'})
    # Wikis
    elif se_type == 'wikis':
        searched = soup.find('div', attrs={'id': 'wiki_search_results'})
        divs = searched.find_all('div', attrs={'class': 'f4 text-normal'})
        items = []
        for div in divs:
            items.append(div.find('a'))

    # Loop the 'a' tags to get the urls
    to_json_list = []
    for item in items:
        got_url = item.get('href')
        # Format URL
        full_url = 'https://github.com' + got_url

        # Extra Information when searching repositories
        if se_type == 'repositories':
            # Get repository owner
            owner = got_url.split('/')[1]
            # Get language stats
            lan_stats = statScrapper(full_url, proxy)
            # Append to list for json output
            to_json_list.append({'url': full_url,
                                    'extra': {'owner': owner,
                                                'language_stats': lan_stats}
                                                })
        else:
            # Append to list for json output
            to_json_list.append({'url': full_url})

    json_string = json.dumps(to_json_list, indent=4)

    return json_string

def statScrapper(url, proxy):
    ''' Get the extra information about language percentages used in repo '''
    # Request
    rsp=requests.get(url, proxies=proxy)
    # Parse html
    soup = BeautifulSoup(rsp.content, 'html.parser')

    # Find the languages bar
    spans = soup.find_all('span', attrs={'class': 'Progress-item',
                                        'data-view-component': "true"}
                            )
    stat_dict = {}
    for span in spans:
        try:
            # Get the item value and split it into vars
            lang, percent = span['aria-label'].split(' ')
            # Save to dict
            # String to float because the target example had it as float
            stat_dict[lang] = float(percent)
        # For 'span' that dont have that item (what we looking for), pass
        except KeyError:
            pass

    return stat_dict

def scrapeMain(input_json, output_json):
    '''
        Main Function, arguments input and output json file path. Easy of use:
            * Takes input json and parsesd the data
            * Creates the url from the input
            * Does the actual scraping
            * Saves to output json
            * Return the json string
    '''
    # Open input json
    data = jsonInput(input_json)
    # Create URL
    url = urlCreate(data['keywords'], data['type'])
    # Call to Scrape
    json_string = searchScrapper(url, data['type'], data['proxies'])
    # Save output
    jsonOutput(output_json, json_string)

    return json_string


########
# MAIN #
########

## ADDED AN EXTRA UTILITY WITH A COMMAND LINE ARGUMENT PARSER
if __name__ == '__main__':
    import argparse

    # Call the argument parse object
    parser = argparse.ArgumentParser()
    # Define the arguments
    # Optional argument, json
    parser.add_argument('-j', '--json', help='Path to an input json file. \
                        If used takes precedence over values specified with \
                        arguments', type=str)
    # Optional argument, output
    parser.add_argument('-o', '--output', help='Path to where to save the \
                        output.', type=str)
    # Optional argument, query, takes indefinite number of values
    parser.add_argument('-q', '--query', help='Keywords to search for.',
                        nargs='*', type=str)
    # Optional argument, type, limited choices
    parser.add_argument('-t', '--type', help='Search for type.',
                        choices=('repositories', 'issues', 'wikis'), type=str)
    # Optional argument, proxy, takes indefinite number of values
    parser.add_argument('-p', '--proxy', help='A list of proxies to use.',
                        nargs='*', type=str)

    '''
        usage: githubscraping.py [-h] [-j JSON] [-o OUTPUT] [-q [QUERY ...]]
                                 [-t {repositories,issues,wikis}]
                                 [-p [PROXY ...]]

        optional arguments:
          -h, --help            show this help message and exit
          -j JSON, --json JSON  Path to an input json file. If used takes
                                precedence over values specified with arguments
          -o OUTPUT, --output OUTPUT
                                Path to where to save the output.
          -q [QUERY ...], --query [QUERY ...]
                                Keywords to search for.
          -t {repositories,issues,wikis}, --type {repositories,issues,wikis}
                                Search for type.
          -p [PROXY ...], --proxy [PROXY ...]
                                A list of proxies to use.
    '''

    args = parser.parse_args()

    if args.json:
        data = jsonInput(args.json)
        args.query = data['keywords']
        args.proxy = data['proxies']
        args.type = data['type']

    url = urlCreate(args.query, args.type)

    json_string = searchScrapper(url, args.type, args.proxy)
    print(json_string)
    if args.output:
        jsonOutput(args.output, json_string)
