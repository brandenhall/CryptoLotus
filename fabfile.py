from fabric.api import *

def update(): 
    with prefix('source env/bin/activate'):
        local('./env/bin/pip install -r requirements.txt', False)

def bootstrap():
    """
    Bootstrap the local environment and download required packages
    """
    local('mkdir -p env', False)
    local('virtualenv env --no-site-packages', False)
    update()

def reset():
    """
    Clean up and reset the environment
    """
    run ('rm -rf env')