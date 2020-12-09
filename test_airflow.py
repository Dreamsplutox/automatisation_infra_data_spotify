from airflow import DAG
import datetime

 
dag = DAG(
dag_id = "toto_"+str(datetime.date.today()),
start_date = str(datetime.date.today()),
schedule_interval = timedelta(days=1))
 
task1 = BashOperator(
task_id = "toto1",
bash_command = "echo hello world",
dag = dag)
 
task2 = BashOperator(
task_id = "toto2",
bash_command = "echo {{ ds }}",
dag = dag)
 
task3 = BashOperator(
task_id = "toto3",
bash_command = "echo {{ ds_nodash }}",
dag = dag)