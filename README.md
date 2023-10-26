# CDE Data Quality Article

### Objective

This git repository supports the [Cloudera Community article on using Great Expectations in Cloudera Data Engineering (CDE)](). You can run the following commands to set up this Great Expectations demo in your CDE Virtual Cluster.

Great Expectations is a Python-based open-source library for validating, documenting, and profiling your data. It helps you to maintain data quality and improve communication about data between teams. Software developers have long known that automated testing is essential for managing complex codebases. Great Expectations brings the same discipline, confidence, and acceleration to data science and data engineering teams.

CDP Data Engineering is the only cloud-native service purpose-built for enterprise data engineering teams. Building on Apache Spark, Data Engineering is an all-inclusive data engineering toolset that enables orchestration automation with Apache Airflow, advanced pipeline monitoring, visual troubleshooting, and comprehensive management tools to streamline ETL processes across enterprise analytics teams.

Data Engineering is fully integrated with Cloudera Data Platform, enabling end-to-end visibility and security with SDX as well as seamless integrations with CDP services such as Data Warehouse and Machine Learning. Data Engineering on CDP powers consistent, repeatable, and automated data engineering workflows on a hybrid cloud platform anywhere.

Spark Data Engineers use Great Expectations in CDE to enforce data quality standards on enterprise datasets and data engineering pipelines at massive scale. In the rest of this tutorial we will walk through a basic workflow with Great Expectations and Spark.

### Requirements

The following are required to reproduce the Demo in your CDE Virtual Cluster:

* CDE Service version 1.19 and above
* A Working installation of the CDE CLI. Instructions to install the CLI are provided [here](https://docs.cloudera.com/data-engineering/cloud/cli-access/topics/cde-cli.html).
* A working installation of git in your local machine. Please clone this git repository and keep in mind all commands assume they are run in the project's main directory.
* A DockerHub account to push and pull Docker images.

##### Code Edits

Two minor code changes are required before deploying the pipeline to your Virtual Cluster:

1. Replace the current username and cloud_storage variables in code/parameters.conf with your credentials. If you don't know what your Storage location is please check in the CDP Management Console or reach out to your CDP Admin.
2. Replace the current username at line five in code/airflow.py.

The remaining are CDE CLI commands that should be run from the terminal.

##### Custom Runtime Setup

```
docker build --network=host -t pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-003 . -f Dockerfile

docker run -it --network=host -t pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-003 . -f Dockerfile /bin/bash

docker push pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-003
```

##### Create CDE Resource for the Great Expectations Docker Runtime

Personalize the value in the --name parameter to reflect your username; replace the value in the --docker-username parameter with your DockerHub username.

```
cde credential create --name docker-creds-pauldefusco --type docker-basic --docker-server hub.docker.com --docker-username pauldefusco

cde resource create --name dex-spark-runtime-great-expectations-data-quality-pauldefusco --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-003 --image-engine spark3 --type custom-runtime-image
```

##### Create CDE Files Resource for Scripts

```
cde resource create --name job_code_data_quality
```

##### Upload Code and Depdencies to CDE Files Resource

```
cde resource upload --name job_code_data_quality --local-path code/airflow.py --local-path code/batch_load.py --local-path code/great_expectations.py --local-path code/parameters.conf --local-path code/utils.py
```

##### Create CDE Jobs

```
cde job create --name batch_load --type spark --mount-1-prefix jobCode/ --mount-1-resource job_code_data_quality --runtime-image-resource-name dex-spark-runtime-great-expectations-data-quality-pauldefusco --application-file jobCode/batch_load.py
```

```
cde job create --name data_quality --type spark --mount-1-prefix jobCode/ --mount-1-resource job_code_data_quality --runtime-image-resource-name dex-spark-runtime-great-expectations-data-quality-pauldefusco --application-file jobCode/great_expectations.py
```

```
cde job create --name data_quality_orchestration --type airflow --mount-1-prefix jobCode/ --mount-1-resource job_code_data_quality --dag-file airflow.py
```

The Airflow Job is scheduled to run every five minutes by default. Therefore, there is no need to manually run any of the above jobs. Open the CDE Job Runs page and the pipeline will be running shortly.

## References

[Great Epectations Documentation](https://docs.greatexpectations.io/docs/)
[Cloudera Data Engineering Documentation](https://docs.cloudera.com/data-engineering/cloud/index.html)
