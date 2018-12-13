# Available queries

The available queries, which can be substituted into `<QUERY>`, include the fol
lowing:

## Articles containing gender words

Run:

```bash
fab standalone.setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt
cd standalone
zip -r newsrods.zip newsrods/
nohup spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission &
```

Expected results for `oids.txt`:

```
0000164- The Courier and Argus/0000164_19070603.xml
0000164- The Courier and Argus/0000164_19151123.xml
```

Quick-and-dirty:

```bash
wc result.yml
head result.yml
```
```
146  437 1935 result.yml
1907:
- [william, 10]
- [alice, 2]
- [jane, 1]
- [deer, 1]
- [itself, 4]
- [mr, 43]
```

## Articles containing "krakatoa" and/or "krakatau"

Run:

```bash
fab standalone.setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_words.txt
cd standalone
zip -r newsrods.zip newsrods/
nohup spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission &
```

Expected results for `oids.txt`:

```
0000164- The Courier and Argus/0000164_19070603.xml
0000164- The Courier and Argus/0000164_19151123.xml
```

```
{}
``

The outputs can be parsed into a JSON file as follows:

```bash
cp standalone/result.yml analysis/result.1.yml
cd analysis
python extractOnlyText.py
```

This outputs a file `test.json` e.g.

```
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
```

A helper file, `analysis/BLN_list.txt`, with a list of newspaper names is used.

---

## Comparing results files

Note that results files may differ in the word ordering. A very quick-and-dirty way of comparing results files is to do, for example:

```bash
sort results1.yml > sorted_results1.yml
sort results2.yml > sorted_results2.yml
cmp sorted_results1.yml sorted_results2.yml
```

---

## Troubleshooting: `result.yml` is `{}`

If you run:

```bash
head result.yml
```

and see:

```
{}
```

then check the permissions of your data files. This can arise if, for example, your data file has permissions like:

```bash
ls -l /mnt/lustre/<your-urika-username>/blpaper/0000164_19010101.xml
```
```
---------- 1 <your-urika-username> at01 3374189 May 31 13:57
```
