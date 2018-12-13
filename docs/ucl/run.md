# Running within UCL

## Local machine requirements

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

---

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

---

## Running on HPC resources

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
