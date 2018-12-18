# Run tests

## Using `fab` (local only)

To run unit tests using `fab`, run:

```bash
fab standalone.setup standalone.pytest
```

You should see:

```bash
============================= test session starts =============================
platform linux2 -- Python 2.7.13, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
rootdir: /home/users/michaelj/i_new_ucl, inifile:
collected 6 items

newsrods/test/test_article.py ..                                        [ 33%]
newsrods/test/test_issue.py ....                                        [100%]

========================== 6 passed in 7.14 seconds ===========================
```

## Using `pytest`

To run unit tests using `pytest`, run:

```bash
cd standalone
pytest
```

You should see:

```
============================= test session starts =============================
platform linux2 -- Python 2.7.13, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
rootdir: /home/users/michaelj/i_new_ucl, inifile:
collected 6 items

newsrods/test/test_article.py ..                                        [ 33%]
newsrods/test/test_issue.py ....                                        [100%]

========================== 6 passed in 7.14 seconds ===========================
```
