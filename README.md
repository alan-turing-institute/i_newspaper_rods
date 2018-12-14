# TDA and British Library Newspapers Data Analysis

The code is designed to query the following data:

* [Times Digital Archive](https://www.gale.com/uk/c/the-times-digital-archive) (TDA) from [Gale](https://www.gale.com), a division of [CENGAGE](https://www.cengage.com/).
* British Library Newspapers data is from [Gale](https://www.gale.com), a division of [CENGAGE](https://www.cengage.com/). The data is in 5 parts e.g. [Part I: 1800-1900](https://www.gale.com/uk/c/british-library-newspapers-part-i). For links to all 5 parts, see [British Library Newspapers](https://www.gale.com/uk/s?query=british+library+newspapers). The complete data consists of ~1TB of digitised versions of newspapers from the 18th to the early 20th century. Each newspaper has an associated folder of XML documents where each XML document corresponds to a single issue of the newspaper. Each XML document conforms to a British Library-specific XML schema.

---

## University College London and TDA

This project uses batched Apache PySpark queries on Legion to run queries over the Times Digital Archive. It is assumed that all queries are grouped by year, so that the results of different years can be concatenated together without any processing. If that is not the case, the code can still be used, but it must be run all as one job.

The goal of this code, where the compute is not done as a single PySpark run, but rather as a larger number of smaller, single node, PySpark executions has mutiple reasons:

* Support for partial failure, with an easy way to resubmit the failed task.  
* Better chances of running on a larger number of machines. As these tasks are generally considered to be I/O bound - in the time spent fetching each individual file from the remote - having more nodes involved in the process should increase the execution speed (due to having more bandwidth available). 
  - This was motivated by the fact that, at the moment, Legion does not give a way of saying how many actual machines are required.
* Allows work to be done even if only one machine is currently available.

### Use

See [Running within UCL](./docs/ucl/run.md).

---

## Analysing humanities data using Cray Urika-GX and British Library Newspapers

The "epcc-sparkrods" branch contains a version of the code that has been updated and extended by Rosa Filgueira and Mike Jackson of [EPCC](https://www.epcc.ed.ac.uk) in their role as members of the [Research Engineering Group](https://www.turing.ac.uk/research/research-engineering) of the [The Alan Turing Institute](https://www.turing.ac.uk).

This work was done in conjunction with Melissa Terras, College of Arts, Humanities and Social Sciences (CAHSS), The University of Edinburgh. This work looked at running the code on the [Alan Turing Institute Cray Urika-GX Service](https://ati-rescomp-service-docs.readthedocs.io/en/latest/cray/introduction.html).

This work was funded by Scottish Enterprise as part of the Alan Turing Institute-Scottish Enterprise Data Engineering Program.

### Use

* [Set up a local environment](./docs/setup-local.md)
* [Set up Urika environment](./docs/setup-urika.md)
* [Run queries](./docs/queries.md)
* [Run tests](./docs/tests.md)

**Note:** the `epcc-sparkrods` branch currently will not work on UCL systems. This is because the code was refactored so that `newsrods/sparkrods.py` no longer constructs UCL-specific URLs by prefixing OIDS file entries with `http://utilities.rd.ucl.ac.uk/objects/`. It would be expected that infrastructure specific functions in `deploy/`, which construct the OIDS files do this. These functions need to be updated to support this.

---

## Copyright and licence

Copyright (c) 2016 University College London

Copyright (c) 2018 The University of Edinburgh

All code is available for use and reuse under a [MIT Licence](http://opensource.org/licenses/MIT). See [LICENSE](./LICENSE).
