# Running within UCL

## Local Machine Requirements

* Apache Spark
* Python 3.5

---

## Testing Locally

Any query can be tested on your local machine, using a tiny subset of the total file archive. This is achieved using: 

```bash
USER=<gpfs_username> fab run_local -u ccearkl -d analysis/place_words.csv -q queries/words_per_year.py
```

For this to work you must have password-less ssh access from your machine to GPFS set up.

---

## Running on HPC Resources

In theory this project can be run on either Legion or Grace. However, testing has only been done on Legion. Also, the `rsd-modules` modules (which include Spark which this project requires) have not yet been set up on Grace. However, once that has all been set up, the same commands should work for grace if the url for `legion` is substituted for `grace`. 

For this to work you must have password-less ssh access from legion to GPFS set up.

You can run the program to run with:

```bash
USER=<gpfs_username>  fab -H "<username>@legion.rc.ucl.ac.uk" run_remote -n 10 -u ccearkl -d analysis/place_words.csv -q queries/words_per_year.py -y 3
```
