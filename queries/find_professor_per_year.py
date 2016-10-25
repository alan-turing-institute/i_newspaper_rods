interesting_word = 'professor'

def mapper(issue):
    mentions = 0
    for article in issue.articles:
        for word in article.words:
            if word.lower() == interesting_word:
                mentions += 1
    return {issue.date.year: [1, mentions]}

reducer = merge_under(double_sum)
