# References

Use this page when you want to go deeper than the local POC docs. Prefer official documentation first, then community examples or blog posts when they answer a specific implementation question.

## How To Use This Page

| If you are asking... | Start with local docs | Then read |
|---|---|---|
| What is this project? | `docs/learning/plain-language-guide.md` | [Docker Compose](https://docs.docker.com/compose/), [Apache Iceberg](https://iceberg.apache.org/docs/latest/) |
| What does a term mean? | `docs/learning/glossary.md` | The matching topic section below |
| How does data become a table? | `docs/architecture/data-flow.md` | [Spark SQL and DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html), [Iceberg Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/) |
| How do analysts query the data? | `docs/learning/lakehouse-learning-path.md` | [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) |
| How do jobs run in order? | `docs/learning/airflow-learning-path.md` | [Apache Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/) |
| How do dashboards work? | `docs/learning/superset-learning-path.md` | [Apache Superset intro](https://superset.apache.org/docs/intro), [Superset database connections](https://superset.apache.org/docs/configuration/databases) |
| How do we monitor the platform? | `docs/learning/observability-learning-path.md` | [Prometheus overview](https://prometheus.io/docs/introduction/overview/), [Grafana docs](https://grafana.com/docs/grafana/latest/) |
| How should a team contribute? | `CONTRIBUTING.md` | [GitHub Pull Requests](https://docs.github.com/articles/about-pull-requests), [GitHub Actions](https://docs.github.com/en/actions) |

## Beginner Orientation

- [Docker Compose](https://docs.docker.com/compose/) explains the local multi-container runtime used by this POC.
- [Apache Iceberg docs](https://iceberg.apache.org/docs/latest/) explain the table format used for lakehouse tables.
- [MinIO documentation](https://docs.min.io/) explains the local S3-compatible object storage pattern.
- [Apache Spark docs](https://spark.apache.org/docs/latest/) explain the processing engine used for transformations.
- [Trino docs](https://trino.io/docs/current/) explain the distributed SQL engine used for queries.
- [Apache Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/) explain workflow orchestration.

## Local Platform And GitHub Workflow

- [Docker Compose](https://docs.docker.com/compose/) for running the local service stack.
- [GitHub Pull Requests](https://docs.github.com/articles/about-pull-requests) for review-based development.
- [GitHub Actions](https://docs.github.com/en/actions) for CI concepts.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) for editing CI YAML.
- [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) for ownership rules.
- [Branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule) for merge safety.

## Lakehouse Core

- [Apache Iceberg docs](https://iceberg.apache.org/docs/latest/) for table format concepts.
- [Iceberg Spark quickstart](https://iceberg.apache.org/spark-quickstart/) for a hands-on Spark and Iceberg introduction.
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) for querying Iceberg tables through Trino.
- [Trino S3-compatible storage](https://trino.io/docs/current/object-storage/file-system-s3.html) for object storage configuration.
- [MinIO documentation](https://docs.min.io/) for S3-compatible object storage concepts and operations.
- [MinIO Docker image](https://hub.docker.com/r/minio/minio) for the local S3-compatible storage container.
- [Apache Polaris](https://github.com/apache/polaris) for learning about an Apache Iceberg REST catalog implementation.

## Data Engineering

- [Apache Spark docs](https://spark.apache.org/docs/latest/) for the processing engine.
- [Spark SQL and DataFrames](https://spark.apache.org/docs/latest/sql-programming-guide.html) for table and DataFrame transformations.
- [Iceberg Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/) for writing and modifying Iceberg tables from Spark.

## Orchestration

- [Apache Airflow docs](https://airflow.apache.org/docs/apache-airflow/stable/) for DAGs, tasks, scheduling, and operators.
- [Airflow Docker Compose guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) for local Airflow setup patterns.
- [Trino with Airflow example](https://trino.io/blog/2022/07/13/how-to-use-airflow-to-schedule-trino-jobs.html) for scheduling Trino SQL work.

## BI And Dashboarding

- [Apache Superset intro](https://superset.apache.org/docs/intro) for BI and dashboard concepts.
- [Superset database connections](https://superset.apache.org/docs/configuration/databases) for connecting Superset to query engines such as Trino.

## Observability

- [Prometheus overview](https://prometheus.io/docs/introduction/overview/) for metrics collection concepts.
- [Prometheus cAdvisor guide](https://prometheus.io/docs/guides/cadvisor/) for container metrics examples.
- [Grafana docs](https://grafana.com/docs/grafana/latest/) for dashboarding metrics.
- [cAdvisor GitHub](https://github.com/google/cadvisor) for the container metrics exporter used in this POC.

## Ingestion UX

- [Apache NiFi docs](https://nifi.apache.org/documentation/) for visual flow-based ingestion.
- [Apache Hop docs](https://hop.apache.org/manual/latest/) for visual data pipelines and orchestration experiments.

## AI And ML

- [FastAPI docs](https://fastapi.tiangolo.com/) for the optional query API service.
- [Trino Python client](https://github.com/trinodb/trino-python-client) for Python access to Trino.
- [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry) for model lifecycle concepts.
- [Qdrant documentation](https://qdrant.tech/documentation/) for vector database concepts.
