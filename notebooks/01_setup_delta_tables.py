# Databricks notebook source
# MAGIC %md
# MAGIC # QueryForge - Delta Table Setup
# MAGIC Run this notebook in Databricks Community Edition to create the financial data schemas as Delta tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Database

# COMMAND ----------

spark.sql("CREATE DATABASE IF NOT EXISTS queryforge")
spark.sql("USE queryforge")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Accounts Table

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, DecimalType, DateType

accounts_data = [
    ("ACC001", "Alice Chen", "checking", 125000.50, "2020-03-15", "NYC001", "active"),
    ("ACC002", "Bob Martinez", "savings", 89000.00, "2019-07-22", "LA002", "active"),
    ("ACC003", "Carol Williams", "loan", 250000.00, "2021-01-10", "CHI003", "active"),
    ("ACC004", "David Kim", "credit", 15000.75, "2018-11-05", "NYC001", "active"),
    ("ACC005", "Eva Patel", "checking", 340000.00, "2022-06-18", "SF004", "active"),
    ("ACC006", "Frank Johnson", "savings", 45000.00, "2017-02-28", "LA002", "closed"),
    ("ACC007", "Grace Lee", "checking", 178000.25, "2020-09-14", "CHI003", "active"),
    ("ACC008", "Henry Brown", "loan", 500000.00, "2023-03-01", "SF004", "active"),
    ("ACC009", "Irene Davis", "credit", 8500.00, "2021-08-20", "NYC001", "frozen"),
    ("ACC010", "Jack Wilson", "checking", 92000.00, "2019-12-03", "LA002", "active"),
]

accounts_df = spark.createDataFrame(accounts_data, ["account_id", "customer_name", "account_type", "balance", "open_date", "branch_code", "status"])
accounts_df = accounts_df.withColumn("balance", accounts_df.balance.cast(DecimalType(18, 2)))
accounts_df = accounts_df.withColumn("open_date", accounts_df.open_date.cast(DateType()))

accounts_df.write.format("delta").mode("overwrite").saveAsTable("queryforge.accounts")
print(f"Accounts table created with {accounts_df.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transactions Table

# COMMAND ----------

transactions_data = [
    ("TXN001", "ACC001", "2024-01-15 09:30:00", 5000.00, "credit", "salary", "Monthly salary deposit"),
    ("TXN002", "ACC001", "2024-01-16 14:22:00", 150.00, "debit", "utilities", "Electric bill payment"),
    ("TXN003", "ACC002", "2024-01-15 10:00:00", 2000.00, "credit", "transfer", "Transfer from checking"),
    ("TXN004", "ACC003", "2024-01-20 08:00:00", 3500.00, "debit", "loan_payment", "Monthly loan payment"),
    ("TXN005", "ACC004", "2024-01-18 16:45:00", 250.00, "debit", "shopping", "Online purchase"),
    ("TXN006", "ACC005", "2024-01-15 09:00:00", 12000.00, "credit", "salary", "Monthly salary deposit"),
    ("TXN007", "ACC005", "2024-01-22 11:30:00", 800.00, "debit", "dining", "Restaurant payment"),
    ("TXN008", "ACC007", "2024-01-15 09:15:00", 8500.00, "credit", "salary", "Monthly salary deposit"),
    ("TXN009", "ACC008", "2024-01-25 08:00:00", 5000.00, "debit", "loan_payment", "Monthly loan payment"),
    ("TXN010", "ACC010", "2024-01-15 09:45:00", 6000.00, "credit", "salary", "Monthly salary deposit"),
    ("TXN011", "ACC001", "2024-02-15 09:30:00", 5000.00, "credit", "salary", "Monthly salary deposit"),
    ("TXN012", "ACC001", "2024-02-20 13:10:00", 2200.00, "debit", "rent", "Monthly rent payment"),
    ("TXN013", "ACC005", "2024-02-15 09:00:00", 12000.00, "credit", "salary", "Monthly salary deposit"),
    ("TXN014", "ACC007", "2024-02-15 09:15:00", 8500.00, "credit", "salary", "Monthly salary deposit"),
    ("TXN015", "ACC010", "2024-02-15 09:45:00", 6000.00, "credit", "salary", "Monthly salary deposit"),
]

from pyspark.sql.types import TimestampType

transactions_df = spark.createDataFrame(transactions_data, ["txn_id", "account_id", "txn_date", "amount", "txn_type", "category", "description"])
transactions_df = transactions_df.withColumn("amount", transactions_df.amount.cast(DecimalType(18, 2)))
transactions_df = transactions_df.withColumn("txn_date", transactions_df.txn_date.cast(TimestampType()))

transactions_df.write.format("delta").mode("overwrite").saveAsTable("queryforge.transactions")
print(f"Transactions table created with {transactions_df.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Risk Metrics Table

# COMMAND ----------

risk_data = [
    ("ACC001", "2024-01-31", 750, "low", 0.0120, 0.3500),
    ("ACC002", "2024-01-31", 680, "medium", 0.0450, 0.4000),
    ("ACC003", "2024-01-31", 620, "high", 0.0890, 0.5500),
    ("ACC004", "2024-01-31", 580, "high", 0.1200, 0.6000),
    ("ACC005", "2024-01-31", 800, "low", 0.0050, 0.2500),
    ("ACC007", "2024-01-31", 720, "low", 0.0180, 0.3200),
    ("ACC008", "2024-01-31", 550, "critical", 0.1800, 0.7500),
    ("ACC009", "2024-01-31", 490, "critical", 0.2500, 0.8500),
    ("ACC010", "2024-01-31", 700, "medium", 0.0350, 0.3800),
]

from pyspark.sql.types import IntegerType

risk_df = spark.createDataFrame(risk_data, ["account_id", "metric_date", "credit_score", "risk_rating", "probability_of_default", "loss_given_default"])
risk_df = risk_df.withColumn("metric_date", risk_df.metric_date.cast(DateType()))
risk_df = risk_df.withColumn("credit_score", risk_df.credit_score.cast(IntegerType()))
risk_df = risk_df.withColumn("probability_of_default", risk_df.probability_of_default.cast(DecimalType(5, 4)))
risk_df = risk_df.withColumn("loss_given_default", risk_df.loss_given_default.cast(DecimalType(5, 4)))

risk_df.write.format("delta").mode("overwrite").saveAsTable("queryforge.risk_metrics")
print(f"Risk metrics table created with {risk_df.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model Inventory Table

# COMMAND ----------

model_data = [
    ("MDL001", "Credit Scoring v3", "classification", "2023-06-15", "Risk Team", "active", "2024-01-15"),
    ("MDL002", "Fraud Detection v2", "anomaly_detection", "2023-09-01", "Fraud Team", "active", "2024-01-20"),
    ("MDL003", "Churn Predictor", "classification", "2022-11-10", "Marketing", "retired", "2023-06-10"),
    ("MDL004", "LGD Model v1", "regression", "2024-01-05", "Risk Team", "validation", "2024-01-05"),
    ("MDL005", "Transaction Classifier", "classification", "2023-03-20", "Operations", "active", "2023-12-15"),
]

model_df = spark.createDataFrame(model_data, ["model_id", "model_name", "model_type", "deployment_date", "owner", "status", "last_validation_date"])
model_df = model_df.withColumn("deployment_date", model_df.deployment_date.cast(DateType()))
model_df = model_df.withColumn("last_validation_date", model_df.last_validation_date.cast(DateType()))

model_df.write.format("delta").mode("overwrite").saveAsTable("queryforge.model_inventory")
print(f"Model inventory table created with {model_df.count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify All Tables

# COMMAND ----------

for table in ["accounts", "transactions", "risk_metrics", "model_inventory"]:
    count = spark.sql(f"SELECT COUNT(*) FROM queryforge.{table}").collect()[0][0]
    print(f"queryforge.{table}: {count} rows")
