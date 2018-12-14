# Run queries

## Specify data files to query

Populate `oids.txt` with the paths to the data files e.g.:

* Local:

```bash
find $HOME/blpaper/xmls -name "*.xml" > oids.txt
```

* Urika:

```bash
find /mnt/lustre/<your-urika-username>/blpaper/xmls -name "*.xml" > oids.txt
```

Check:

```bash
cat oids.txt
```


You should see the following:

* Local, where `<HOME>` is the path to your home directory, where you mounted the data:

```
<HOME>/blpaper/xmls/0000164- The Courier and Argus/0000164_19070603.xml
<HOME>/blpaper/xmls/0000164- The Courier and Argus/0000164_19151123.xml
...
```

* Urika:

```
/mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/0000164_19070603.xml
/mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/0000164_19151123.xml
...
```

---

## Specify a subset of data files to query

For experimentation, you may find it useful to run queries across a subset of the data. For examplnm you can hard-code the paths.

Alternatively, you can run `find` over a subset of the paths:

* Local:

```bash
find $HOME/blpaper/xmls/0000164- The Courier and Argus/ -name "*.zip" > oids.txt
```

* Urika:

```bash
find /mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/ -name "*.zip" > oids.txt
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query and `<DATA>` the name of a complementary query-specific data file.

Create job for Spark:

```bash
fab standalone.setup:query=queries/<QUERY>.py,datafile=query_args/<DATA>.txt
```

`fab` sets up a `standalone` directory with the following format:

* `newsrods`: a copy of `newrods`.
* `newsrods/query.py`: a copy of the `query` i.e. `queries/<QUERY>.py`.
* `oids.txt`: a copy of `oids.txt`.
* `input.data`: a copy of the file specifed as the `datafile` argument e.g. `query_args/<DATA>.txt`.

Run using `pyspark` (local only):

```bash
cd standalone
pyspark < newsrods/standalone_runner.py
```

Run using `spark-submit`:

```bash
cd standalone
zip -r newsrods.zip newsrods/
nohup spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission &
```

**Note:**

* `144` is the number of cores requested for the job. This, with the number of cores per node, determines the number of workers/executors and nodes. For Urika, which has 36 cores per node, this would request 144/36 = 4 workers/executors and nodes.
* This is required as `spark-runner --total-executor-cores` seems to be ignored.
* If omitted, this defaults to `1`.

Check results:

```bash
cat result.yml 
```

---

## Available queries

The available queries, which can be substituted into `<QUERY>`, include the fol
lowing.

### Articles containing gender words

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

### Articles containing "krakatoa" and/or "krakatau"

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
```

`results.xml` will contain XML fragments with articles matching the query, indexed by timestamp. These can be converted into a JSON document with both the matching articles and metadata about each article as follows:

```bash
python analysis/filter_query_results.py  analysis/BLN_list.txt standalone/result.yml result.json
```

The JSON file has the following format:

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

`analysis/BLN_list.txt` is a helperfile with a plain-text list of newspaper names.

---

## Comparing results files

Note that results files may differ in the word ordering. A very quick-and-dirty way of comparing results files is to do, for example:

```bash
sort results1.yml > sorted_results1.yml
sort results2.yml > sorted_results2.yml
cmp sorted_results1.yml sorted_results2.yml
```

---

## Check number of executors used

A quick-and-dirty way to get this number is to run:

```bash
grep Exec output_submission | wc -l
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

---

## Troubleshooting: `ImportError: No module named api`

If, when running `fab` you see:

```bash
ImportError: No module named api
```

Then check your version of `Fabric` e.g.

```bash
pip freeze | grep Fabric
```

It should be 1.x e.g. 1.14.0 and not 2.x. Fabric changed between version 1 and 2. See [fabric](https://github.com/fabric/fabric/issues/1743) issue [no module named fabric.api#1743](https://github.com/fabric/fabric/issues/1743).

---

## Troubleshooting: `pyspark: command not found`

If when running `fab standalone` you get:

```bash
...
/bin/sh: pyspark: command not found
...
Aborting.
```

Then add Apache Spark to your `PATH`:

```bash
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```