# contains functions that query the RESTful interface of the conference corpus
import requests
from tabulate import tabulate


def test():
    r = requests.get('https://conferencecorpus.bitplan.com/eventseries/WEBIST?format=json')
    print(r.json().keys())

    response = requests.get('https://conferencecorpus.bitplan.com/eventseries/HPCC?format=json')
    if response:
        print('Success!')
    else:
        print('An error has occurred.')
    print(type(response.json()))
    print(response.json().keys())

    print(response.json())
    print(tabulate(response.json(), headers="keys"))

    print(response.json()['dblp'])
    print(tabulate(response.json()['dblp'], headers="keys"))


# returns the query for the restful interface for the given data source as a list of dicts; input is an acronym
# if the request fails it returns and prints 'error'
# if the given datasource is not present it returns and prints 'source not available'
def getdblp(input:str):
    url = 'https://conferencecorpus.bitplan.com/eventseries/ßß?format=json'
    url = url.replace('ßß', input)
    response = requests.get(url)
    if response:
        print('Success!')
        if 'dblp' in response.json():
            return response.json()['dblp']
        else:
            print('source \'dblp\' not available')
            return 'source not available'
    else:
        print('An error has occurred.')
        return 'error'


# returns the query for the restful interface for the given data source as a list of dicts; input is an acronym
# if the request fails it returns and prints 'error'
# if the given datasource is not present it returns and prints 'source not available'
def getconfref(input:str):
    url = 'https://conferencecorpus.bitplan.com/eventseries/ßß?format=json'
    url = url.replace('ßß', input)
    response = requests.get(url)
    if response:
        print('Success!')
        if 'confref' in response.json():
            return response.json()['confref']
        else:
            print('source \'confref\' not available')
            return 'source not available'
    else:
        print('An error has occurred.')
        return 'error'


# returns the query for the restful interface for the given data source as a list of dicts; input is an acronym
# if the request fails it returns and prints 'error'
# if the given datasource is not present it returns and prints 'source not available'
def getcrossref(input:str):
    url = 'https://conferencecorpus.bitplan.com/eventseries/ßß?format=json'
    url = url.replace('ßß', input)
    response = requests.get(url)
    if response:
        print('Success!')
        if 'crossref' in response.json():
            return response.json()['crossref']
        else:
            print('source \'crossref\' not available')
            return 'source not available'
    else:
        print('An error has occurred.')
        return 'error'


# returns the query for the restful interface for the given data source as a list of dicts; input is an acronym
# if the request fails it returns and prints 'error'
# if the given datasource is not present it returns and prints 'source not available'
def getwikicfp(input:str):
    url = 'https://conferencecorpus.bitplan.com/eventseries/ßß?format=json'
    url = url.replace('ßß', input)
    response = requests.get(url)
    if response:
        print('Success!')
        if 'wikicfp' in response.json():
            return response.json()['wikicfp']
        else:
            print('source \'wikicfp\' not available')
            return 'source not available'
    else:
        print('An error has occurred.')
        return 'error'


# returns the query for the restful interface for the given data source as a list of dicts; input is an acronym
# if the request fails it returns and prints 'error'
# if the given datasource is not present it returns and prints 'source not available'
def getgnd(input:str):
    url = 'https://conferencecorpus.bitplan.com/eventseries/ßß?format=json'
    url = url.replace('ßß', input)
    response = requests.get(url)
    if response:
        print('Success!')
        if 'gnd' in response.json():
            return response.json()['gnd']
        else:
            print('source \'gnd\' not available')
            return 'source not available'
    else:
        print('An error has occurred.')
        return 'error'


# returns the query for the restful interface for the given data source as a list of dicts; input is an acronym
# if the request fails it returns and prints 'error'
# if the given datasource is not present it returns and prints 'source not available'
def getwikidata(input:str):
    url = 'https://conferencecorpus.bitplan.com/eventseries/ßß?format=json'
    url = url.replace('ßß', input)
    response = requests.get(url)
    if response:
        print('Success!')
        if 'wikidata' in response.json():
            return response.json()['wikidata']
        else:
            print('source \'wikidata\' not available')
            return 'source not available'
    else:
        print('An error has occurred.')
        return 'error'


# returns the query for the restful interface for all outsources as a dict so we don't ask the interface for each source
# if the request fails it returns and prints 'error'
# Important: we need to check whether our desired source is present in the response like in the functions above
def getall(input:str):
    url = 'https://conferencecorpus.bitplan.com/eventseries/ßß?format=json'
    url = url.replace('ßß', input)
    response = requests.get(url)
    if response:
        print('Success!')
        return response.json()
    else:
        print('An error has occurred.')
        return 'error'
