# Run queries locally

## Specify data files to query

Populate `oids.txt` with the paths to the data files e.g.:

```bash
find $HOME/blpaper/xmls -name "*.xml" > oids.txt
```

Check:

```bash
cat oids.txt
```

You should see the following (where `<HOME>` is the path to your home directory, where you mounted the data):

```
<HOME>/blpaper/xmls/0000164- The Courier and Argus/0000164_19070603.xml
<HOME>/blpaper/xmls/0000164- The Courier and Argus/0000164_19151123.xml
...
```

---

## Specify a subset of data files to query

For experimentation, you may find it useful to run queries across a subset of the data. For example (where `<HOME>` is the path to your home directory, where you mounted the data) you can hard-code the paths:

```
<HOME>/blpaper/xmls/0000164- The Courier and Argus/0000164_19070603.xml
<HOME>/blpaper/xmls/0000164- The Courier and Argus/0000164_19151123.xml
...
```

Alternatively, you can run `find` over a subset of the paths:

```bash
find $HOME/blpaper/xmls/0000164- The Courier and Argus/ -name "*.zip" > oids.txt
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query and `<DATA>` the name of a complementary query-specific data file:

```bash
fab standalone.setup:query=queries/<QUERY>.py,datafile=query_args/<DATA>.txt standalone.test
```

`fab` sets up a `standalone` directory with the following format:

* `newsrods`: a copy of `newrods`.
* `newsrods/query.py`: a copy of the `query` i.e. `queries/<QUERY>.py`.
* `oids.txt`: a copy of `oids.txt`.
* `input.data`: a copy of the file specifed as the `datafile` argument e.g. `query_args/<DATA>.txt`.

To set up the `standalone` directory, without running the query, run:

```bash
fab standalone.setup:query=queries/<QUERY>.py,datafile=query_args/<DATA>.txt
```

To run using `pyspark`, run:

```bash
cd standalone
pyspark < newsrods/standalone_runner.py
```

To run using `spark-submit`, run:

```bash
cd standalone
zip -r newsrods.zip newsrods/
spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 
```

Check results:

```bash
cat result.yml 
```

See [Available queries](../queries.md) for available queries, which can be substituted into `<QUERY>`.

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
