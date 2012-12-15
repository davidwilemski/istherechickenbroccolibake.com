
from fabric.api import *
from fabtools import require
import fabtools

@task
def deploy():
    with prefix('source ~/itcbb_env/bin/activate'):
        with cd('~/itcbb'):
            run('git pull')
    stop()
    start()

@task
def start():
    with prefix('source ~/itcbb_env/bin/activate'):
        with cd('~/itcbb'):
            run('supervisord')

@task
def stop():
    with prefix('source ~/itcbb_env/bin/activate'):
        with cd('itcbb'):
            run('kill `cat supervisord.pid`')

@task
def setup():
    require.python.pip()

    # Create venv
    run('virtualenv -p /usr/local/bin/python2.7 itcbb_env')

    # activate venv
    with fabtools.python.virtualenv('itcbb_env'):
        # clone repo
        run('git clone https://github.com/davidwilemski/istherechickenbroccolibake.com.git itcbb')
        
        # install requirements
        fabtools.python.install_requirements('itcbb/requirements.txt')

    start()
