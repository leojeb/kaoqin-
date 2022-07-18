from datetime import datetime, timedelta
from docker.types import Mount
from pprint import pprint
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable

#导入连续包名
bag = Variable.get('bag')
# 整合好所有路径
input_path = f'/disk/upload/upload/{bag}'
output_path = f'/disk/livego/cowarobot/test_output/{bag}/lu_test/output'
log_path = f'/disk/livego/cowarobot/test_output/{bag}/lu_test/log'

default_args = {
    "retries": 1
}
# 创建DAG对象
dag = DAG(
    "boge_docker",
    default_args=default_args,
    # schedule_interval=timedelta(minutes=10),
    start_date=datetime(2021, 1, 1),
    catchup=False,
)
def watch_files():
    pass
# 监控文件, 将新生成文件传入后续task中执行
t_watchdog = ShortCircuitOperator(
    task_id="check_if_file_updated",
    python_callable=watch_files,
    dag=dag,
)


def print_context(ds, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'

print_args = PythonOperator(
    task_id='print_the_context',
    python_callable=print_context,
    dag=dag,
    op_kwargs={'a':'我是a'},
)
echo_hello = BashOperator(
    task_id='say_hello',
    bash_command="echo 'hello, 运行正常' ",
    dag=dag,
)
run_redis = DockerOperator(
    api_version='1.41',
    image='redis',
    container_name='redis_test',
    dag=dag,
    # command="echo $PATH",
    # auto_remove=True,
    task_id="start-redis",
    docker_url="tcp://172.16.0.43:2375",

)

sleep_10 = BashOperator(
    task_id="wait-for-redis",
    bash_command='sleep 10s',
    dag=dag,
)
run_data = DockerOperator(
    api_version='auto',
    image='data_extracting_crmw-data',
    mounts=[
        Mount(source="/home/cowa/dockers", target="/data/input"),
        Mount(source="/log", target="/cowarobot/.log")
    ],
    container_name="data_test",
    dag=dag,
    task_id="run_data",
    tty=True,
    environment={
        "CRPILOT_HOST": "crmw-redis"
    },
    command="bash /cowarobot/start.sh",
    docker_url="tcp://172.16.0.43:2375",
)
print_args >> echo_hello
sleep_10 >> run_data
# run_this >> echo_hello >> run_redis >> run_data
