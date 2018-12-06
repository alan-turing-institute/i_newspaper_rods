# i_Newspaper_RODS

This project uses batched Apache PySpark queries to run queries over the Times Digital Archive. It is assumed that all queries are grouped by year, so that the results of different years can be concatenated together without any processing.

While iRODS is in the name of the project, there is actualy little in the code that ties it to the iRODS system. All iRODS interaction is limited to a single fabric tasks, and does not happen at runtime. Data is fetched by HTTP (from UCL's WOS), however, this could be easily changed. The majority of work in this version of the code has gone into parsing and manipulating the Issue and Article XML.

Currently, the iRODS and HPC-related components are only compatible with UCL's internal resources including their Legion HPC resource. However, the code can be run standalone also.

---

## Architecture Motivation

The goal of this branch, where the compute is not done as a single PySpark run, but rather as a larger number of smaller, single node, PySpark executions has mutiple reasons:

* Support for partial failure, with an easy way to resubmit the failed task.  
* Better chances of running on a larger number of machines. As these tasks are generally considered to be I/O bound - in the time spent fetching each individual file from the remote - having more nodes involved in the process should increase the execution speed (due to having more bandwidth available). 
  - This was motivated by the fact that, at the moment, Legion does not give a way of saying how many actual machines are required.
* Allows work to be done even if only one machine is currently available.

---

## UCL users

### Beware: epcc-master branch

The `epcc-master` branch currently does not work for UCL systems. This is because the code was refactored so that `newsrods/sparkrods.py` no longer constructs UCL-specific URLs by prefixing OIDS file entries with `http://utilities.rd.ucl.ac.uk/objects`. It would be expected that infrastructure specific functions in `deploy/`, which construct the OIDS files do this. These functions need to be updated to support this.

### Local machine requirements

* Apache Spark.
* Python 2.7.
* iCommands. If you're on Mac OS X, install Kanki, see below.

**Installing iRODS iCommands locally on Mac OS X Sierra**

While it looks like you can install iCommands with `brew install irods`, in actual fact that version is too old to be usable with UCL's iRODS system.

You need to install [Kanki](https://github.com/ilarik/kanki-irodsclient).

You have to install the most recent version (not the stable one) to work with the newer version of Mac OS X.

While it is hidden in the documentation, remember the following steps: 

* Create `~/.irods/irods_environment.json` with the following contents (this combines both the instructions for UCL and Kanki).

```json
{
    "irods_host": "arthur.rd.ucl.ac.uk",
    "irods_port": 1247,
    "irods_default_resource": "wos",
    "irods_zone_name": "rdZone",
    "irods_home": "/rdZone/live",
    "irods_authentication_scheme": "PAM",
    "irods_default_hash_scheme": "SHA256",
    "irods_user_name": "YOUR_UCL_USER_ID",
    "irods_plugins_home": "/Applications/iRODS.app/Contents/PlugIns/irods/"
}
```

* Add the following lines to your `~/.bash_profile`

```bash
# iRods iCommands setup
export PATH=/Applications/iRODS.app/Contents/PlugIns/irods/icommands:$PATH
# This is not a real export due to SIP on OS X 
export DYLD_LIBRARY_PATH=/Applications/iRODS.app/Contents/Frameworks:$DYLD_LIBRARY_PATH
```

* After having done both steps, run:

```bash
iinit
```

* You will be prompted for your password.

## Running locally

Any query can be tested on your local machine, using a tiny subset of the total file archive. This is acheived as follows.

Mac OS X:

```bash
fab --set DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5
test
```

Note that the `DYLD_LIBRARY_PATH` must be provided explicitly on Mac OS X as it cannot be passed to sub-shells automatically due to System Integrity Protection (SIP).

Otherwise:

```bash
fab setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5 test
```

### Running on HPC resources

In theory this project can be run on either Legion or Grace. However, testing has only been done on Legion. Also, the rsd-modules modules (which include Spark which this project requires) have not yet been set up on Grace. However, once that has all been set up, the same commands should work for Grace if the command `legion` is substituted for `grace`, with the same parameters. 

You can run the program to run with:

```bash
fab --set DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=0,years_per_chunk=5 legion:username=<YOUR_UCL_USER_ID> prepare sub
```

You can see the status of your jobs with:

```bash
fab legion:username=<YOUR_UCL_USER_ID> stat
```

**Note**: the `prepare` and `sub` tasks must be run as part of the same `fab` invocation because they create a folder with the current time and date on Legion to store all the data.

---

## Standalone users

If you don't have access to UCL's resources, you can run queries on your local machine, using a tiny subset of the total file archive.

### Local machine requirements

* Apache Spark
  - https://spark.apache.org
* Java 8
* Python 2.7/3.4

### To install on Mac OS X

```bash
brew install apache-spark
```

### To install on CentOS 7

Install Java 1.8:

```bash
yum install java-1.8.0-openjdk-devel
wget https://repo.anaconda.com/archive/Anaconda2-5.1.0-Linux-x86_64.sh
```

Install Anaconda 5.1 Python 2.7:

* See https://www.anaconda.com/download/

```bash
bash Anaconda2-5.1.0-Linux-x86_64.sh
nano anaconda2.sh
```

Add content:

```
export PATH=/home/centos/anaconda2/bin:$PATH
```

```bash
source anaconda2.sh
pip install -r requirements.txt
```

Install Apache Spark:

* See https://spark.apache.org/downloads.html
* See https://spark.apache.org/docs/latest/index.html

```bash
wget http://apache.mirror.anlx.net/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.asc
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.md5
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.sha512
wget https://www.apache.org/dist/spark/KEYS
gpg --import KEYS
gpg --verify spark-2.3.0-bin-hadoop2.7.tgz.asc spark-2.3.0-bin-hadoop2.7.tgz
md5sum spark-2.3.0-bin-hadoop2.7.tgz
cat spark-2.3.0-bin-hadoop2.7.tgz.md5 
sha512sum spark-2.3.0-bin-hadoop2.7.tgz
cat spark-2.3.0-bin-hadoop2.7.tgz.sha512 
tar -xf spark-2.3.0-bin-hadoop2.7.tgz
cd spark-2.3.0-bin-hadoop2.7/
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```

## Running standalone

To run standalone, run:

```bash
fab standalone.setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5 standalone.test
```

`fab` sets up a `standalone` directory with the following format:

* `newrods`: a copy of `newrods`.
* `newrods/query.py`: a copy of the `query` e.g. `queries/articles_containing_words.py`.
* `oids.txt`: a copy of `oids.txt`.
* `input.data`: a copy of the file specifed as the `datafile` argument e.g. `query_args/interesting_gender_words.txt`.

To only set up the `standalone` directory, run:

```bash
fab standalone.setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt
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

To view results, run:

```bash
cat standalone/result.yml
```

If using the sample data in `oids.txt`, you should see:

```bash
1939:
- [them, 9]
- [mr, 29]
- [ewe, 1]
- [man, 7]
- [it, 62]
- [philip, 3]
...
- [it, 245]
```

### Running unit tests

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

### Troubleshooting: `pyspark: command not found`

If when running `fab standalone` you get:

```bash
setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5
test
...
[localhost] local: pyspark < newsrods/local_runner.py
/bin/sh: pyspark: command not found

Fatal error: local() encountered an error (return code 127) while
executing 'pyspark < newsrods/local_runner.py'

Aborting.
```

Then add Apache Spark to your `PATH`:

```
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```

### Troubleshooting: `ImportError: No module named api`

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

## Urika users

### Set up Python environment

Create `py27` environment:

```bash
module load anaconda3/4.1.1
conda create -n py27 python=2.7 anaconda

Proceed ([y]/n)? y
```

Activate environment:

```bash
source activate py27
```

Show active environment:

```bash
conda env list
```
```
# conda environments:
#
py27                  *  /home/users/<your-urika-username>/.conda/envs/py27
root                     /opt/cray/anaconda3/4.1.1
```

Install dependencies:

```bash
cd i_newspaper_rods
conda install -c anaconda --file requirements.txt
```

**Note**:  After creating the `py27` environment, for your subsequent Urika sessions you just need to type:

```bash
module load anaconda3/4.1.1
source activate py27
```

### Mount data using SSHFS

```bash
mkdir blpaper
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-urika-username>@sg.datastore.ed.ac.uk:<path-in-uoe-datastore> blpaper
```

Create data directory on Lustre:

```bash
mkdir -p /mnt/lustre/<your-urika-username>/blpaper/xmls
```

Copy data file `0000164_19010101.xml` into Lustre:

```bash
cp blpaper/xmls/0000164-\ The\ Courier\ and\ Argus/0000164_19010101.xml /mnt/lustre/<your-urika-username>/blpaper/

#or use the news_copy script stored in deploy directory 
./news_copy.sh $HOME/blpaper/xmls/ /mnt/lustre/<username>/blpaper 
```

**Important note:**

* Do **not** mount the DataStore directory directly onto Lustre. Urika compute nodes have no network access and so can't access DataStore via the mount. Also, for efficient processing, data movement needs to be minimised. Copy the data into Lustre as above.

Set data file permissions:

```bash
chmod -R u+rx /mnt/lustre/<your-urika-username>/blpaper/*.xml
```

### Update OIDS file

Change `oids.txt` to be the path to your files e.g.:

```bash
find /mnt/lustre/<your-urika-username>/blpaper/ -name "*xml" > oids.txt
```

Check:

```bash
cat oids.txt
```

You should see:

```bash
/mnt/lustre/<your-urika-username>/blpaper/0000164_19010101.xml
```

### Submit Spark job

Create directory:

```bash
fab standalone.setup:query=queries/articles_containing_words.py,datafile=query_args/interesting_gender_words.txt,number_oid=5
cd standalone
zip -r newsrods.zip newsrods/
```

Submit Spark job:

```bash
nohup spark-submit --py-files newsrods.zip newsrods/standalone_runner.py 144 > output_submission &
```
(144 --> to indidcate the number of cores to use --> 144/36 == number of workers)

### Check results

```bash
wc result.yml
head result.yml
```

You should see:

```
73 219 968 result.yml
1901:
- [mary, 6]
- [his, 44]
- [gerald, 1]
- [himself, 9]
- [boy, 4]
- [brother, 4]
- [queen, 11]
- [duke, 6]
```

### Comparing results files

Note that results files may differ in the word ordering. A very naive way of comparing results files is to do, for example:

```bash
sort results1.yml > sorted_results1.yml
sort results2.yml > sorted_results2.yml
cmp sorted_results1.yml sorted_results2.yml
```

### Troubleshooting: `result.yml` is `{}`

If you run:

```bash
head result.yml
```

and see:

```bash
{}
```

then check the permissions of your data files. This can arise if, for example, your data file has permissions like:

```bash
ls -l /mnt/lustre/<your-urika-username>/blpaper/0000164_19010101.xml
```
```bash
---------- 1 <your-urika-username> at01 3374189 May 31 13:57
```

---

## Notes

### GalenP newspaper data examples

https://www.ft.com/content/514f00a0-a0fe-3b2c-99e0-3be8201f9e8c

Latest query: Find all the articles with “Krakatoa and/or Krakatua “ terms

```bash
fab standalone.setup:query=queries/article_xml_with_words.py,datafile=query_args/interesting_words.txt,number_oid=5 
```


Analysis directory: 
```bash
	cp standalone/results.yml analysis/.
	python extractOnlyText.py --> returns the results into test.json
```
