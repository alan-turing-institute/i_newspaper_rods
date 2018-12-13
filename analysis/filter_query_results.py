"""
Process XML fragments with articles matching some query into a JSON document with both the matching articles and metadata about each article.

Usage:

    python extractOnlyText.py <NEWSPAPER_FILE> <INPUT_FILE> <OUTPUT_FILE>

where:

* <NEWSPAPER_FILE>: plain-text list of newspaper names.
* <INPUT_FILE>: YAML file with output from analysis.
  - Each key is of form YYYY-MM-DD HH:MM:SS
  - Each value is a list of XML "article" elements as strings.

    YYYY-MM-DD HH:MM:SS: ["...", "..."],
    ...

* <OUTPUT_FILE>: JSON file of form:

    {
        "YYYY-MM-DD": [
            {"id_name": "<NEWSPAPER-NAME>",
             "id_newspaper": "<PAPER-ID>",
             "id_issue": "<ISSUE>",
             "title": "<TITLE>",
             "content": "<STRING-CONTAINING-WORD>",
             "page": "<PAGE>"}
             ...
        ],
        "YYYY-MM-DD": [ ... ],
        ...
    }
"""


import datetime
from lxml import etree  # pylint: disable=all
import json
import sys
import yaml


def read_newspapers(newspaper_file):
    with open(newspaper_file, "r+") as f:
        newspapers = f.readlines()
    return newspapers


def read_yaml_articles(yaml_file):
    with open(yaml_file, "r") as f:
        yaml_articles = yaml.load(f)
    return yaml_articles


def write_json_articles(json_file, json_articles):
    with open(json_file, 'w') as f:
        json.dump(json_articles, f)


def process_query_results(query_results, newspapers):
    articles = {}
    for date_time, match_articles in query_results.items():
        day = str(date_time.date())
        articles[day] = []
        for match_article in match_articles:
            parser = etree.XMLParser(recover=True)
            tree = etree.fromstring(match_article, parser)
            title = tree.xpath('text/text.title/p/wd/text()')
            content = tree.xpath('text/text.cr/p/wd/text()')
            page_total = tree.xpath('pi/text()')
            page = []
            for i in page_total:
                page.append(i.split("_")[-1])
                id_xml = page_total[0].split("_")[:2]
            id_newspaper = page_total[0].split("_")[:1]
            for newspaper in newspapers:
                if "".join(id_newspaper) in newspaper:
                    id_name = newspaper 
            article = {
                "title":" ".join(title).replace(' - ', ''),
                "page":" ".join(page).replace(' - ', ''),
                "content":" ".join(content).replace(' - ', ''),
                "id_newspaper": "".join(id_newspaper),
                "id_name": id_name,
                "id_issue":"_".join(id_xml)}
            articles[day].append(article)
    return articles


if __name__ == "__main__":
    newspaper_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    newspapers = read_newspapers(newspaper_file)
    yaml_articles = read_yaml_articles(input_file)
    json_articles = process_query_results(yaml_articles, newspapers)
    write_json_articles(output_file, json_articles)
