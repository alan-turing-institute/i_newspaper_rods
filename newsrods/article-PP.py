"""
Object model representation of XML Article.


Module for articles, many of which make up an issue

This is a patch to make New Zealand Paper Past accessible to our queries

The XML schema is different, so we need to change the path-to-interesting-content
"""

from logging import getLogger
from datetime import datetime
from lxml import etree


class Article(object):
    """
    Class to represent an article in an issue of an newspaper
    """
    def __init__(self, source):
        """
        Create the article from source XML
        """
        self.logger = getLogger('py4j')
        self.tree = source
	# This is for articles from NLA archive. Every article is represented
	# by several strings, such as heading, articleText, title (= the name 
	# of the newspaper, publisher...), date ...
        self.quality = self.tree.xpath('ocr/text()')
        if not self.quality:
            self.quality = None
        elif len(self.quality) == 1:
            self.quality = float(self.quality[0])
        else:
            self.logger.info('Multiple OCR qualities found. Dropping.')
            self.quality = None

	#======= The stuff that matters: =====
        # heading of the article:
        self.title = self.tree.xpath('result/title/text()') #heading of the article:
        # text of the article:
	self.content = self.tree.findtext('fulltext')
	# date of publication:
	raw_date = self.tree.findtext('display-date')
 	self.date = datetime.strptime(raw_date, '%d-%m-%Y')
	# name of the newspaper:	
	self.papername = self.tree.xpath('result/publisher/publisher/text()')

	#old stuff that doesn't match anything here:
	#self.preamble = self.tree.xpath('text/text.preamble/p/wd/text()')

    @property
    def words(self):
        """
        Get the full text of the article, title etc.abs as a list of tokens
        """
        return self.title + self.content

    @property
    def words_string(self):
        """
        Return the full text of the article as a string (in NLA archive this is 	default). Remove all hyphens.
        This merges hyphenated word but may cause problems with subordinate
        clauses (The sheep - the really loud one - had just entered my office).
        """
        return ' '.join(self.content).replace(' - ', '')
