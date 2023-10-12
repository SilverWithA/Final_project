from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging


# 1. Get 'num_list' as an argument of function
# 2. Insert 10 to 'num_list'
# 3. Return list
def func_insert_list(num_list):
    num_list.append(10)
    return num_list

# 1. Get num_list (Return value of 'func_get_list')
# 2. Get sum value of the list
# 3. Return sum value
def func_sum_list(**context):
    # Get return value of funtion 'func_insert_list' using task id 'id_insert_number_list'
    response_num_list = context['task_instance'].xcom_pull(
        task_ids='id_insert_number_list')
    logging.info(response_num_list)
    sum_val = sum(response_num_list)
    return sum_val

# Store data to output.txt
def func_save(**context):
    # Get return value of function 'func_sum_list' using task id 'id_sum_list'
    sum_val = context['task_instance'].xcom_pull(task_ids='id_sum_list')
    logging.info(f"Sum of list: {sum_val}")
    with open("output.txt", "w") as file:
        file.write(f"Sum of list: {sum_val}")

#########################################################
# Define DAG

default_args = {
    'owner': 'airflow',
    "start_date": datetime(2023, 1, 1),
    # Receive the context information as kwargs in the function
    "provide_context": True
}

with DAG(
    # DAG name
    'sum_of_list',
    default_args=default_args,
    # Run every 10 minutes
    schedule_interval=timedelta(minutes=10),
) as dag:

    # Define number list
    num_list = [1, 2, 3]

    # Define task
    insert_list = PythonOperator(
        # Define task ID
        task_id='id_insert_number_list',
        # Function to run
        python_callable=func_insert_list,
        # Specify the arguments for the function
        op_args=[num_list],
        dag=dag
    )

    # Define task
    sum_list = PythonOperator(
        # Define task ID
        task_id='id_sum_list',
        # Function to run
        python_callable=func_sum_list,
        dag=dag
    )

    # Define task
    save = PythonOperator(
        # Define task ID
        task_id='id_saving_data',
        # Function to run
        python_callable=func_save,
        dag=dag
    )

    # Task relationship
    insert_list >> sum_list >> save