'''
New Zealand Paper Past reformulation of the articles_containing_words.py query
'''

from operator import add
import re

def do_query( issues, interesting_words_file, _log ):
	'''
	Get number of articles which contain a given word a year:
	'''

	# a list of words to search for:
	interesting_words = [re.compile(r'\b' + word.strip() + r'\b', re.I | re.U)
				for word in list(open(interesting_words_file)) ]

	# Map each article in each issue to a year of publication:
	articles = issues.flatMap(lambda issue: issue.articles)
	year_article = articles.map( lambda article : (article.date.year, article) )

	# Add 1 record for each word that appears in each article in each year
	interest = year_article.flatMap(lambda (year, article):
                                [((year, regex.pattern), 1) for regex in
                                 interesting_words if regex.findall(article.content)])

	# Now add sum the year-word counts, and change the format for output
	interesting_by_year = interest \
        			.reduceByKey(add) \
        			.map(lambda (year_word, count): (year_word[0],
                                            (year_word[1].replace(r'\b', ''),
                                            count))) \
        			.groupByKey() \
        			.map(lambda (year, data): (year, list(data))) \
        			.collect()

	return interesting_by_year

