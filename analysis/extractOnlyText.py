'''
Collect text from XML fragments resulting from whitechapel queries
'''
import datetime
from lxml import etree  # pylint: disable=all
import yaml
import json

FILENAMES = ['./result.1.yml']

i = 1
for fname in FILENAMES:
    texts = []
    stream = file(fname, 'r')
    batch_data = yaml.load(stream)
    text_year={}
    for a_date, list_articles in batch_data.items():
        day=str(a_date.date())
        text_year[day]=[]
        for article in list_articles:
            info_article={}
            parser = etree.XMLParser(recover=True)
            tree = etree.fromstring(article, parser)
            title = tree.xpath('text/text.title/p/wd/text()')
            content = tree.xpath('text/text.cr/p/wd/text()')
            page_total = tree.xpath('pi/text()')
	    page=[]
            for i in page_total:
		page.append(i.split("_")[-1])
	    id_xml = page_total[0].split("_")[:2]
	    id_newspaper = page_total[0].split("_")[:1]
            info_article={
		"title":" ".join(title).replace(' - ', ''),
		"page":" ".join(page).replace(' - ', ''),
		"content":" ".join(content).replace(' - ', ''),
		"id_newspaper": "".join(id_newspaper),
		"id_issue":"_".join(id_xml)}
            text_year[day].append(info_article)
	     
    with open("test.json", 'w') as outfile:
    		json.dump(text_year, outfile)

