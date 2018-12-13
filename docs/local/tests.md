# Run tests locally

To run unit tests using `fab`, run:

```bash
fab standalone.setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt standalone.pytest
```

You should see:

```bash
============================= test session starts ==============================
platform linux2 -- Python 2.7.14, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /home/centos/i_newspaper_rods, inifile:
collected 5 items

newsrods/test/test_article.py .                                          [ 20%]
newsrods/test/test_issue.py ....                                         [100%]

=========================== 5 passed in 5.31 seconds ===========================
```

To run unit tests using `pytest`, run:

```bash
cd standalone
pytest
```
