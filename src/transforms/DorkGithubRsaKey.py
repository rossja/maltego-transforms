# -*- coding: utf-8 -*-

# import the relevant objects from the maltego_trx library
from maltego_trx.entities import Website
from maltego_trx.maltego import UIM_PARTIAL
from maltego_trx.transform import DiscoverableTransform

# import the things we need to perform the Google search, and process results
import requests
from bs4 import BeautifulSoup

# create the class for our transform
class DorkGithubRsaKey(DiscoverableTransform): 
    """
    Find exposed RSA Private Keys in Github that are associated with a given search term
    """
    
    @classmethod
    def create_entities(cls, request, response):
        """
        Processes the Maltego request and returns the formatted data requested
        """
        search_term = request.Value

        try:
            hits = cls.scrape(search_term) # execute the scrape function and save the results
            if hits:
                # iterate through the hits dictionary and create an entity for each result
                for website_title,website_url in hits.items():
                    response.addEntity( Website, "%s:%s" % (website_title, website_url) )
            else:
                # send a message back to the Maltego user interface so the user knows there were no results
                response.addUIMessage("The provided search term did not result in any hits")
        except Exception as e:
            # send a message to the Maltego user interface with error information
            response.addUIMessage("An error occurred performing the search query: %s" % (e), messageType=UIM_PARTIAL)

    @staticmethod
    def scrape(search_term):
        """ 
        Performs a Google search targeting RSA Private keys in Github. Returns a dictionary of Github file titles, and the associated URL.
        """
        
        """ 
        Example of search output we are looking to parse in the results:
            <div class="kCrYT">
                <a href="/url?q=https://github.com/Shekharrajak/Blood-bank-S-W-intern-sample-codes/blob/master/mysql-connector-java-5.1.35/src/testsuite/ssl-test-certs/mykey.pem&amp;sa=U&amp;ved=2ahUKEwjm1YPent3kAhXMTxUIHQC4CLkQFjACegQICRAB&amp;usg=AOvVaw3sbCLKYBGDno8mBAo8NyaN">
                    <div class="BNeawe vvjwJb AP7Wnd">
                        Blood-bank-S-W-intern-sample-codes/mykey.pem at master ...
                    </div>
                    <div class="BNeawe UPmit AP7Wnd">
                        https://github.com > blob › master › src › testsuite › ssl-test-certs › mykey
                    </div>
                </a>
            </div>
        """
        
        # set the Google search URL
        search_url = 'https://www.google.com/search?q="' + search_term + '"+site:github.com+-site:gist.github.com+-inurl:issues+-inurl:wiki+-filetype:markdown+-filetype:md+"-----BEGIN+RSA+PRIVATE+KEY-----"'

        hits = {}                                       # create an empty dictionary to hold results       
        content = requests.get(search_url).text         # make the search request
        soup = BeautifulSoup(content, "html5lib")       # store the result from the search

                                                        # parse the results:
        for link in soup.select(".kCrYT > a"):          # use a css4 selector to find the links we want
            hit = link.get('href')                      # get the URl from the link
            href = hit.replace('/url?q=','')            # remove Google click tracking "feature" to get the target URL
            titleDiv = link.findChild('div')            # find the first div after the link, and use that text as the page title
            hits[titleDiv.text] = href                  # add the title and href to the 'hits' dictionary
        return hits                                     # return the results, as the hits dictionary
