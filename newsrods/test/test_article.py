'''
Tests for Article
'''

from unittest import TestCase
import os
import os.path
import urllib2
import urlparse

from ..issue import Issue


class TestPage(TestCase):
    '''
    Test class for Article
    '''

    def setUp(self):
        '''
        Load the standard test file
        '''
        url = os.path.join(os.path.dirname(__file__),
                           'fixtures', '2000_04_24.xml')
        url = urlparse.urljoin("file:", url)
        fixture = urllib2.urlopen(url)
        issue = Issue(fixture)
        self.article = issue.articles[0]

    def test_words_in_article(self):
        '''
        Check that the article length is correct
        '''
        assert len(self.article.words) == 18
