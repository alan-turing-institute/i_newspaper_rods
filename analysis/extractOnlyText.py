'''
Collect text from XML fragments resulting from whitechapel queries
'''

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
            preamble = tree.xpath('text/text.preamble/p/wd/text()')
            content = tree.xpath('text/text.cr/p/wd/text()')
            #words = title + preamble + content
            #words_string = ' '.join(words).replace(' - ', '')
            #texts.append(words_string)
            info_article={
		"title":" ".join(title).replace(' - ', ''),
		"preamble":" ".join(preamble).replace(' - ', ''),
		"content":" ".join(content).replace(' - ', '')}
            text_year[day].append(info_article)

	     
    #with open('test.' + str(i) + '.yml', 'w') as output:
    #    output.write(yaml.dump(texts, default_flow_style=False))
    #    i += 1
    #stream.close()
    with open("test.json", 'w') as outfile:
    		json.dump(text_year, outfile)

