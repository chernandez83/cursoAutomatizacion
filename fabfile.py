from fabric import task, Connection

connection = Connection('10.0.0.101', user='batman', port=22, connect_kwargs={'password': '123'})

@task
def show_dir(context):
    result = connection.run('uname -a')
    print(result)

# fab show-dir