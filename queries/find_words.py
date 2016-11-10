interesting_words = ['Holland',
                         'Netherlands',
                         'Netherland',
                         'Flanders',
                         'Flemish',
                         'Frisian',
                         'Friesland',
                         'Frisia',
                         'Belgium',
                         'Belgian',
                         'Wallonia',
                         'Amsterdam',
                         'Rotterdam',
                         'Utrecht',
                         'Groningen',
                         'Leeuwarden',
                         'Zwolle',
                         'Deventer',
                         'Tilburg',
                         'Overijssel',
                         'Drenthe',
                         'Gelderland',
                         'Guelders',
                         'Gelders',
                         'Twente',
                         'Twenthe',
                         'Drente',
                         'Drenthe',
                         'Brabant',
                         'Brabantian',
                         'Limburg',
                         'Limburgian',
                         'Limbourg',
                         'Limbourgian',
                         'Zeeland',
                         'Zeeuws',
                         'Sealand',
                         'Zeelandic',
                         'Sealandic',
                         'North-Holland',
                         'Noord-Holland',
                         'South-Holland',
                         'Zuid-Holland',
                         'Texel',
                         'Ameland',
                         'Schiermonnikoog',
                         'Vlieland',
                         'Batavia',
                         'Batavian',
                         'Indies',
                         'Suriname',
                         'Curacao',
                         'Aruba',
                         'Almere',
                         'Lelystad',
                         'Hindeloopen',
                         'Almeloo',
                         'Hengelo',
                         'Roermond',
                         'Breda',
                         'Tilburg',
                         'Willemstad',
                         'Amersfoort',
                         'Bruges',
                         'Brugge',
                         'Gent',
                         'Ghent',
                         'Bruxelles',
                         'Brussel',
                         'Brussels',
                         'Antwerp',
                         'Anvers',
                         'Antwerpen',
                         'Maline',
                         'Mechelen',
                         'Ypres',
                         'Ieper',
                         'Passchendaele',
                         'Pachendale',
                         'Vlissingen',
                         'Flushing',
                         'Middelburg',
                         'Zierikzee',
                         'Wallonian',
                         'Dutch',
                         'Flemish',
                         'Hollandic',
                         'Benelux',
                         'Luembourg',
                         'Luxemburg',
                         'Luxembourgian',
                         'Luxemburgian']

interesting_ngrams=[
            ['Low','Countries'],
            ['The','Hague'],
            ['Den','Haag'],
            ['East','Indies']
]

from newsrods.issue import Issue
from newsrods.sparkrods import get_streams

streams = get_streams(downsample = 1024)

issues = streams.map(Issue)

articles = issues.flatMap(lambda x: [(x.date.year, article) for article in x.articles])
interest = articles.flatMap(lambda x: [((x[0], y), 1) for y in interesting_words if y in x[1].words])
interesting_by_year = interest.reduceByKey(lambda x,y: x+y).map(
    lambda x: (x[0][0], (x[0][1], x[1]))
    ).groupByKey().map(lambda x: (x[0],list(x[1]))).collect()

import yaml
with open('result.yml','w') as result_file:
    result_file.write(yaml.safe_dump(dict(interesting_by_year)))
