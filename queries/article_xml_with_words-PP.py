'''
This module returns the full XML of the articles that contain
a given regular expression.
'''

import re
from lxml import etree  # pylint: disable=all


def do_query(issues, interesting_words_file, _log):
    '''
    Get the count of specific words of interest by year
    '''
    # Get the list of words to search for
    regex_string = r'\b('
    first = True
    for word in list(open(interesting_words_file)):
        if not first:
            regex_string = regex_string + r'|'
        regex_string = regex_string + word.strip()
        first = False
    regex_string = regex_string + r')\b'

    interesting_words = re.compile(regex_string, re.I | re.U)

    # Map each article in each "issue" (that is, an xml file) to a year of publication:
    articles = issues.flatMap(lambda issue: issue.articles)
    year_article = articles.map( lambda article : (article.date.year, article) )

    # Add 1 record for each word that appears in each article in each year
    #article_test= articles.take(1)
    #print("PRINT ARTICLE DATE YEAR %s!!!!" % article_test.date.year)
    #year_article_test = year_article.take(1)
    #print("PRINT YEAR ARTICLE %s!!!!" % year_article_test)
    interest = year_article.flatMap(lambda (year, article):
					    check_text(year, article, interesting_words))

    # Group elements by year
    interesting_by_year = interest \
        .groupByKey() \
	.map(lambda (year, data): (year, list(data))) \
        .collect()
        #.map(lambda (year, data): (year, list(data))) \
    return interesting_by_year


def check_text(year, article, interesting_words):
    '''
    Catch articles that match the given regex
    '''
    if interesting_words.search(article.words_string) is not None:
        #return [(year, article.title)]
        #return [(year, article.content)]
	return [(year,  article.content)]
    return []
