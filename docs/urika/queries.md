# Run queries on Urika

## Specify data files to query

Populate `oids.txt` with the paths to the data files e.g.:

```bash
find /mnt/lustre/<your-urika-username>/blpaper/xmls -name "*.xml" > oids.txt
```

Check:

```bash
cat oids.txt
```

You should see the following (where `<HOME>` is the path to your home directory, where you mounted the data):

```
/mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/0000164_19070603.xml
/mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/0000164_19151123.xml
...
```

---

## Specify a subset of data files to query

For experimentation, you may find it useful to run queries across a subset of the data. For example you can hard-code the paths:

```
/mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/0000164_19070603.xml
/mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/0000164_19151123.xml
...
```

Alternatively, you can run `find` over a subset of the paths:

```bash
find /mnt/lustre/<your-urika-username>/blpaper/xmls/0000164- The Courier and Argus/ -name "*.zip" > oids.txt
```

---

## Run queries (general form)

Queries are run as follows, where `<QUERY>` is the name of a query, `<DATA>` the name of a complementary query-specific data file.

Create job for Spark:

```bash
fab standalone.setup:query=queries/<QUERY>.py,datafile=query_args/<DATA>.txt
cd standalone
zip -r newsrods.zip newsrods/
```

Submit job to Spark:

```bash
nohup spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission &
```

`144` is the number of cores requested for the job. This, with the number of cores per node, determines the number of workers/executors and nodes. For Urika, which has 36 cores per node, this would request 144/36 = 4 workers/executors and nodes.

**Note:** This is required as `spark-runner --total-executor-cores` seems to be ignored.

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
