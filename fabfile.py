# from fabric import task, Connection

# connection = Connection('10.0.0.101', user='batman', port=22, connect_kwargs={'password': '123'})

# @task
# def show_dir(context):
    # result = connection.run('uname -a')
    # print(result)

# fab show-dir
from fabric.api import run, task, env, cd, prefix, sudo, get, local
from datetime import datetime

env.hosts = ['10.0.0.101']
env.user = 'batman'

DATABASE = 'tiendaFlask'
LOCAL_BACKUP_FOLDER = 'descargas/'

def pull():
    run('git pull')

def install_requirements():
    run('pip install -r requirements.txt')

@task
def deploy(c):
    with cd('src/tiendaFlask'):
        pull()
        with prefix('source env/bin/activate'):
            install_requirements()
        
        sudo('systemctl restart tiendaFlask')
        sudo('systemctl restart nginx')


def get_backup_name():
    return f'{DATABASE}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql'


def get_backup(backup):
    get(
        remote_path=backup,
        local_path=LOCAL_BACKUP_FOLDER
    )


def delete_backup(backup):
    sudo(f'rm {backup}')


def load_backup(backup_path):
    local(f'mysql -u root --password= -e "DROP DATABASE {DATABASE}"')
    local(f'mysql -u root --password= -e "CREATE DATABASE {DATABASE}"')
    local(f'mysql -u root --password= {DATABASE} < {backup_path}')


def create_backup(backup_name):
    run(f'mysqldump -u batman --password=123 {DATABASE} > {backup_name}')


@task
def backup(c):
    backup_name = get_backup_name()
    
    create_backup(backup_name)
    
    get_backup(backup_name)
    
    backup_path = f'{LOCAL_BACKUP_FOLDER}{backup_name}'
    load_backup(backup_path)
    
    delete_backup(backup_name)

# fab deploy