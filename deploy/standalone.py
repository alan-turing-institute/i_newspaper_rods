'''
Set up to run standalone without use of IRODS.
'''

import os
import pandas as pd
from fabric.api import task, env, execute, lcd, local

DEPLOY_DIR = "standalone"

@task
def setup(query, datafile, years_per_chunk=1e10, number_oid=-1):
    '''
    Prepare instance for running. Generates necessary files and installs
    packages
    '''
    execute(install, query=query, datafile=datafile)


@task
def install(query, datafile):
    '''
    Run the tests
    '''
    local('rm -rf ' + DEPLOY_DIR)
    local('mkdir -p ' + DEPLOY_DIR)
    with lcd(DEPLOY_DIR):  # pylint: disable=not-context-manager
        local('cp -r ../newsrods .')
        local('cp ../' + query + ' ./newsrods/query.py')
        local('cp ../' + datafile + ' input.data')
        local('cp ../oids.txt oids.txt')
        local('find . -iname "*.pyc" -delete')
        local('find . -iname "__pycache__" -delete')


@task
def test():
    '''
    Run the query on the sub set of files
    '''
    with lcd(DEPLOY_DIR):  # pylint: disable=not-context-manager
        local('pyspark < newsrods/standalone_runner.py')


@task
def pytest():
    '''
    Run the pytest tests
    '''
    with lcd(DEPLOY_DIR):  # pylint: disable=not-context-manager
        local('py.test')
