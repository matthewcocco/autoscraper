import requests
from urllib import quote
from time import sleep
from random import random, choice
from datetime import datetime
import lxml.html as lh
import csv
import ConfigParser

import lxml._elementpath as DONTUSE  # workaround for Modulefinder when compiling Windows binaries.

__version__ = 1.0
__author__ = "Matthew Cocco"

# somewhat inspired by incolumitas' GoogleScraper.


class Autoscraper():
    '''
    Autoscraper: for automating keyword searches.

    Assumes that you have a "keywords.txt" and "domains.txt"
    in the same directory as the script.

    Default constructor is simply:

    fizz = Autoscraper()

    Reads the keywords, domains, and useragents from the files
    expected to be in the same directory as the script,
    generates a [.csv] file named according to today's date,
    then performs the searches, while writing to the [.csv]
    as it finds results.

    Note that because we don't want to hammer Google with requests,
    there are some built-in random delays, which mean that
    the more keywords you want to search for, the longer
    you should expect execution to take.
    '''

    positions = {}  # empty positions dict, filled by init.
    keywords = []   # empty keywords list, filled by init.

    useragent = 'Mozilla/5.0'  # default harmless useragent,
                               # replaced during init with
                               # a random useragent.

    config = {'engine': 'google.com',  # default config
              'delay': 25}             # to be updated during init

    # default filenames

    useragents_filename = 'useragents.txt'
    domains_filename = 'domains.txt'
    keywords_filename = 'keywords.txt'
    config_filename = 'config.ini'
    csv_filename = datetime.now().strftime('%d-%b-%Y') + ".results.csv"

    # begin functions

    def __init__(self,
                 keywords_filename=keywords_filename,
                 domains_filename=domains_filename):
        '''
        Initializes Autoscraper by reading from config files
        (which should be in the same directory as this script).
        '''

        print("Initializing Autoscraper v%s." % (__version__))  # print() statement is for debugging purposes;
        self.keywords = [keyword.strip() for keyword in open(keywords_filename, 'rb').readlines()]
        self.domains = [domain.strip() for domain in open(domains_filename, 'rb').readlines()]

        # these two lines create lists from lines in the files; the .strip() is to remove the newlines.
        # (because \n adds unnecessary newlines when writing to the csv)

                                              # Uses ConfigParser to load settings from config.ini
        parser = ConfigParser.ConfigParser()  # Creates a ConfigParser
        parser.read(self.config_filename)     # Parses the file

        # and then adds maps values to options in a dictionary, self.config

        for option in parser.options("CONFIG"):
            self.config[option] = parser.get("CONFIG", option)

        # if we haven't already generated a [.csv] for today, then we create one.
        # this assumes that the [.csv] will be opened in Microsoft Excel;
        # if you open this in Libreoffice, the first row might consist solely of 'sep='.

        try:
            with open(self.csv_filename):
                pass
        except IOError:
            print("Record for today not found. Preparing file: %s" % self.csv_filename)  # print() statement is for debugging purposes;
            with open(self.csv_filename, 'wb') as w:
                w.write("sep=,\n")
                csv.writer(w, dialect='excel').writerow(['Keyword', 'First Occurrence', 'Domain', 'Second Occurrence', 'Domain', 'Third Occurrence', 'Domain'])

        # end init

    def execute(self):
        '''
        Searches through Google for each keyword in the currently loaded
        keyword list for any of the domains in the currently loaded domain list.

        Utilizes construct_query to put together the URLs.

        Results are written to the [.csv] as each search/parse is completed.
        '''

        # first, select a random useragent from the useragents filename
        # we'll be using this useragent for all of the searches that follow.
        # >> note that we might also try changing the user agent for every
        #    few searches; not sure if/how this would affect incidence of
        #    google's 'Sorry' message.

        useragent = choice(open(self.useragents_filename, 'rb').readlines())

        print("Useragent chosen: %s" % useragent)  # print() statement is for debugging purposes;

        headers = {'user-agent': useragent}

        # for every keyword in the keyword list, perform a search.

        for keyword in self.keywords:

            print("Searching %s for keyword %s" % (self.config['engine'], keyword))  # print() statement is for debugging purposes;

            # url = self.construct_query(keyword)
            # response = requests.get(url, headers=headers)
            # doc = lh.document_fromstring(response.text)

            # the following is splicing the above three together, which:
            # + constructs the appropriate URL to query Google for a keyword,
            # + fetches the HTML response provided by Google,
            # + converts the HTML response into something easy to parse.

            response = requests.get(self.construct_query(keyword), headers=headers)
            doc = lh.document_fromstring(response.content)

            # WE SHOULD PROBABLY CHECK FOR GOOGLE GIVING US A 'SORRY' MESSAGE HERE
            # AND IF SO, WE SHOULD FLUSH COOKIES AND CHANGE USERAGENT AND WAIT A MINUTE OR THREE

            # links = [element.get('href') for element in doc.xpath("//h3[@class='r']/a")]
            # plain_links = [item.strip('url?q/=').split('&sa')[0] for item in links]

            # the following is a bit complex at first glance, but it's really just
            # splicing the above two lines together, which:
            # + searches the parseable HTML for links of the class 'r',
            # + strips the links of any junk attached to them.

            list_links = [item.strip('url?q/=').split('&sa')[0] for
                          item in [element.get('href') for element in
                                   doc.xpath("//h3[@class='r']/a")]]

            # list_links is just that: a list of links.

            occurrences = []  # create empty list, "occurrences"

            # now that we have a list of links and
            # a list to record occurrences in...
            # for each domain in the list of domains:

            for domain in self.domains:

                # for each link in the list of links...

                for link in list_links:
                    if domain in link:

                        # if the domain is in the link, append a tuple containing
                        # the position and domain of the link to the list of occurrences.

                        position = (list_links.index(link) + 1)
                        print("Link for keyword %s found at position %d" % (keyword, position))  # print() statement is for debugging purposes;
                        occurrences.append((position, domain))

            # only bother with sorting/printing/recording occurrences if there are any

            if (len(occurrences) >= 1):
                row = [keyword] + sorted(occurrences)

                # after constructing a row, which is a list made up of the keyword
                # followed by tuples of each occurrence, append the row to the [.csv].

                self.append_to_csv(row)

            else:
                print("Position for keyword %s not found." % keyword)  # print() statement is for debugging purposes;

                # since the keyword was not found, just append a row with the keyword
                # as a list with only one item (the keyword as a string) to the [.csv],
                # because otherwise the append function will only append the first
                # letter of the string.

                self.append_to_csv([keyword])

            self.pause()  # wait an arbitrary amount of time to avoid triggering Google's 'Sorry' message.

            # end keyword for-loop

        # end execute()

    def construct_query(self, keyword='cats are cute'):
        '''
        Takes a keyword and returns a string containing the URL
        to query google with.

        Processes the keyword to make sure it's safe for URL use.

        Assumes that you want 100 results with personalization off.

        TODO: Support feature for leaving personalization on.
              Support feature for adjusting number of results.
        '''

        # quote(keyword.replace(' ', '+'), safe='+') does a few things.
        # first, keyword.replace(' ', '+') replaces any spaces in the
        # keyword (which could actually be multiple words) with the
        # '+' character, necessary for searching Google.
        # Then, the quote(<...>, safe='+') escapes any other strange
        # characters in the URL, save for instances of '+'.

        return ('http://%s/search?q=%s&pws=0&complete=0&num=100' % (self.config['engine'], quote(keyword.replace(' ', '+'), safe='+')))

    def append_to_csv(self, result):
        '''
        Takes a list (result),
        which should be [
                            string keyword,
                            (integer position, string domain)
                            [, (another position, another domain)...]
                        ]

        Opens the results csv, then appends result (as a new line)
        '''

        row = [result[0]]  # the keyword is the first item in the list to append to the csv.

        # for each of the items in the results list,

        for item in result:
            if (type(item) is tuple) and (len(item) > 1):  # if the item is a tuple whose length is greater than one,
                row.extend([item[0], item[1]])             # extend the row, adding the results.

        print("Appending %s to %s." % (row, self.csv_filename))  # print() statement for debugging purposes;

        csv.writer(open(self.csv_filename, 'ab'), dialect='excel').writerow(row)  # write the row to the [.csv].

    def pause(self, time=config['delay']):
        '''
        Utilizes sleep and random.random() to pause execution of the program when called.
        Arbitrary pause in execution to reduce frequency of hits to google search.

        TODO: Support feature to adjust duration from a config file and/or when called.
              Support adjustment of 'time' by the script when 'Sorry' is detected.
        '''

        # I feel like the following is self-explanatory.

        sleep_time = time + random()*5
        print("Sleeping for " + str(sleep_time) + " seconds.")  # print() statement for debugging purposes;

        sleep(sleep_time)
        print("Done sleeping.\n")  # print() statement for debugging purposes;

testbot = Autoscraper()
testbot.execute()
