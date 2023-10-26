#****************************************************************************
# (C) Cloudera, Inc. 2020-2022
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# #  Author(s): Paul de Fusco
#***************************************************************************/

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pyspark.sql.functions as F
from great_expectations.profile.basic_dataset_profiler import BasicDatasetProfiler
from great_expectations.dataset.sparkdf_dataset import SparkDFDataset
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite
import time

run_id = f'{time.time()}'
print(run_id)

data_lake_name = "s3a://go01-demo/" #Edit config value with your CDP Data Lake name from the CDP Management Console

spark = SparkSession.builder.appName('INGEST').config("spark.kubernetes.access.hadoopFileSystems", data_lake_name).getOrCreate()

df = spark.read.option("inferSchema" , "true").option("header", "true").csv("/app/mount/lending.csv")

df.show(10)

print("PRINT DF SCHEMA")
df.printSchema()

# If you don't have a table you can use the data in the data folder:
# Upload to cloud storage first and then access with
#df = spark.read.option("inferSchema" , "true").option("header", "true").csv(data_lake_name+"/path/to/lending.csv")

# creating GE wrapper around spark dataframe
gdf = SparkDFDataset(df)

# gdf holds referance to df as gdf.spark_df
# we can access the df as gdf.spark_df

gdf.spark_df.show(10)

MANDATORY_COLUMNS = [
    "name",
    "street_address",
    "city",
    "postcode",
    "phone_number",
    "job",
    "recency",
    "history",
    "used_discount",
    "used_bogo",
    "zip_code",
    "is_referral",
    "channel",
    "offer",
    "conversion",
    "score",
    "estimated_annual_income",
    "estimated_joint_annual_status",
    "estimated_"
]

# EXPECTATIONS ON ALL COLUMN

#OK
for column in MANDATORY_COLUMNS:
    try:
        assert gdf.expect_column_to_exist(column).success, f"Column {column} is not found\n"
        print(f"Column {column} is found")
    except Exception as e:
        print(e)
#OK
for column in MANDATORY_COLUMNS:
    try:
        test_result = gdf.expect_column_values_to_not_be_null(column)
        assert test_result.success, f"Values for column {column} are null\n"
        print(f"Values for column {column} are not null")
    except Exception as e:
        print(e)

# EXPECTATIONS ON NUMERIC COLUMNS
#OK
try:
    test_result = gdf.expect_column_min_to_be_between(column="recency", min_value=0, max_value=1).success, f"Min for column recency is not within expected range\n"
    assert test_result.success, f"Min for column recency is within expected range\n"
except Exception as e:
        print(e)
#OK
try:
    test_result = gdf.expect_column_max_to_be_between(column="recency", min_value=8, max_value=10).success, f"Max for column recency is not within expected range\n"
    assert test_result.success, f"Max for column recency is within expected range\n"
except Exception as e:
        print(e)
#OK
try:
    test_result = gdf.expect_column_mean_to_be_between(column="score", min_value=0, max_value=3).success, f"Mean for column score is not within expected range\n"
    assert test_result.success, f"Min for column score is within expected range\n"
except Exception as e:
    print(e)
#OK
try:
    test_result = gdf.expect_column_stdev_to_be_between(column="estimated_annual_income", min_value=1, max_value=10).success, f"STDEV for column estimated_annual_income is not within expected range\n"
    assert test_result.success, f"STDEV for column estimated_annual_income is within expected range\n"
except Exception as e:
    print(e)
#OK
try:
    test_result = gdf.expect_column_median_to_be_between(column="emp_length", min_value=1, max_value=10).success, f"Min for column annual_inc_joint is not within expected range\n"
    assert test_result.success, f"Min for column annual_inc_joint is within expected range\n"
except Exception as e:
    print(e)

# EXPECTATIONS ON STRING COLUMNS
#OK
try:
    test_result = gdf.expect_column_values_to_match_regex(column="acc_now_delinq", regex="[at]+").success, f"xpected range\n"
    assert test_result.success, f"Min for column annual_inc is within expected range\n"
except Exception as e:
    print(e)
#OK
try:
    test_result = gdf.expect_column_values_to_not_match_regex(column="acc_now_delinq", regex="[at]+").success, f"Min for column annual_inc_joint is not within expected range\n"
    assert test_result.success, f"Min for column annual_inc_joint is within expected range\n"
except Exception as e:
    print(e)
#OK
try:
    test_result = gdf.expect_column_value_lengths_to_be_between(column="city", min_value=10, max_value=20).success, f"Column city length is not within expected range\n"
    assert test_result.success, f"Column city length is within expected range\n"
except Exception as e:
    print(e)

# EXPECTATIONS ON BOOLEAN COLUMNS

try:
    test_result = gdf.expect_column_distinct_values_to_be_in_set(column="used_discount", value_set=[0,1]).success, f"Expected values for column used_discount is not within provided set\n"
    assert test_result.success, f"Expected values for column used_discount is within provided set\n"
except Exception as e:
    print(e)

try:
    test_result = gdf.expect_column_distinct_values_to_contain_set(column="is_referral", value_set=[0,1]).success, f"Expected values for column is_referral do not contain provided set\n"
    assert test_result.success, f"Expected values for column is_referral contain provided set\n"
except Exception as e:
    print(e)

try:
    test_result = gdf.expect_column_distinct_values_to_equal_set(column="conversion", value_set=[0,1]).success, f"Expected values for column conversion do not equal provided set\n"
    assert test_result.success, f"Expected values for column conversion equal provided set\n"
except Exception as e:
    print(e)

# EXPECTATIONS BASED ON OTHER COLUMNS

try:
    test_result = gdf.expect_column_distinct_values_to_equal_set(column="conversion", value_set=[0,1]).success, f"Expected values for column conversion do not equal provided set\n"
    assert test_result.success, f"Expected values for column conversion equal provided set\n"
except Exception as e:
    print(e)

estimated_joint_annual_status
