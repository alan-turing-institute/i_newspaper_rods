'''
Module to load and read the files using Spark.
'''

from newsrods.issue import Issue
from requests import get


def open_stream(url):
    stream = get(url, stream=True)  # requests.models.Response
    raw = stream.raw  # urllib3.response.HTTPResponse
    raw.decode_content = True
    return raw


def get_streams(context,
                source="oids.txt"):
    '''
    Turn a list of oids in a file into a RDD of Issues.
    '''
    oids = [oid.strip() for oid in list(open(source))]
    are_urls = len(oids) > 0 and \
        (oids[0].lower().startswith("http://") or \
         oids[0].lower().startswith("https://"))
    rddoids = context.parallelize(oids)
    if (are_urls):
        issues = rddoids.map(lambda url: open_stream(url)) \
                            .map(lambda raw: Issue(raw))
    else:  # file paths
        issues = rddoids.map(lambda file_name: Issue(file_name))
    return issues
