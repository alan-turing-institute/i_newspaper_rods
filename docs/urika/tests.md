# Run tests on Urika

To run unit tests using `pytest`, run:

```bash
fab standalone.setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt
cd standalone
pytest
```

You should see:

```
============================= test session starts ==============================
platform linux2 -- Python 2.7.14, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /home/centos/i_newspaper_rods, inifile:
collected 5 items

newsrods/test/test_article.py .                                          [ 20%]
newsrods/test/test_issue.py ....                                         [100%]

=========================== 5 passed in 5.31 seconds ===========================
```
