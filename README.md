# CDE Great Expectations Article

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

##### Custom Runtime Setup

```
docker build --network=host -t pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-003 . -f Dockerfile

docker run -it docker build --network=host -t pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-003 . -f Dockerfile /bin/bash

docker push pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-great-expectations-003
```

##### Create CDE Docker Runtime for Sedona

```
cde credential create --name docker-creds-pauldefusco --type docker-basic --docker-server hub.docker.com --docker-username pauldefusco

cde resource create --name dex-spark-runtime-sedona-geospatial-pauldefusco --image pauldefusco/dex-spark-runtime-3.2.3-7.2.15.8:1.20.0-b15-sedona-geospatial-003 --image-engine spark3 --type custom-runtime-image
```

##### Create CDE Files Resource for Countries Data

```
cde resource create --name countries_data
```

##### Upload files to Countries Data Files Resource

```
cde resource upload-archive --name countries_data --local-path data/ne_50m_admin_0_countries_lakes.zip
```

##### Create CDE Files Resource for Scripts

```
cde resource create --name job_code
```

##### Upload Code and Depdencies to CDE Files Resource

```
cde resource upload --name job_code --local-path code/geospatial_joins.py --local-path code/geospatial_rdd.py --local-path code/parameters.conf --local-path code/utils.py
```

##### Create CDE Jobs

```
cde job create --name geospatial_rdd --type spark --mount-1-prefix jobCode/ --mount-1-resource job_code --mount-2-prefix countriesData/ --mount-2-resource countries_data --runtime-image-resource-name dex-spark-runtime-sedona-geospatial-pauldefusco --packages org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.5.0,org.datasyslab:geotools-wrapper:1.5.0-28.2 --application-file jobCode/geospatial_rdd.py
```

```
cde job create --name geospatial_joins --application-file jobCode/geospatial_joins.py --type spark --mount-1-prefix jobCode/ --mount-1-resource job_code --mount-2-prefix countriesData/ --mount-2-resource countries_data --runtime-image-resource-name dex-spark-runtime-sedona-geospatial-pauldefusco --packages org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.5.0,org.datasyslab:geotools-wrapper:1.5.0-28.2
```

##### Run CDE Jobs

```
cde job run --name geospatial_rdd --executor-cores 2 --executor-memory "4g"

cde job run --name geospatial_joins --executor-cores 2 --executor-memory "4g"
```

## References

[Great Epectations Documentation](https://docs.greatexpectations.io/docs/)
[Cloudera Data Engineering Documentation](https://docs.cloudera.com/data-engineering/cloud/index.html)
