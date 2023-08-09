from airflow import DAG
from airflow.decorators import task
from airflow.exceptions import AirFlowException
from airflow.utils.trigger_rule import TriggerRule

@task(trigger_rule=TriggerRule.ONE_FAILED, retries=0)
def watcher():
    raise AirFlowException("")

with DAG(
    dag_id="security_master_pipeline",
    schedule="",
    start_date=None,

) as sec_master_dag:
    
    @task()
    def run_scrape():
        from scripts.dataacq.dataacq.sec_master import scrape
        scrape()

    @task()
    def run_parse():
        from scripts.dataacq.dataacq.sec_master import parse
        parse()

    scrape_task = run_scrape()
    run_task = run_parse()

    scrape_task >> run_task
    list(sec_master_dag.tasks) >> watcher()