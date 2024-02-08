PROYECT_NAME ?= dataproc-serveless

RAW_DATA_BUCKET_NAME ?= raw-data-$(PROYECT_NAME)
OUTPUT_DATA_BUCKET_NAME ?= output-$(PROYECT_NAME)
CODE_BUCKET_NAME ?= code-$(PROYECT_NAME)
BUCKETS ?= $(RAW_DATA_BUCKET_NAME) $(OUTPUT_DATA_BUCKET_NAME) $(CODE_BUCKET_NAME)

REGION ?= us-central1

PROYECT_ID ?= datatest-347114
GCS_LOCATION ?= gs://$(PROYECT_ID)

all: create

create: send_2_dataproc_serverless

# Create the required buckets and dependencies for execution
buckets:
	@echo ""
	@$(foreach BUCKET, $(BUCKETS),\
	gsutil mb -l $(REGION) gs://$(BUCKET);\
	echo "\e[32mCreated $(BUCKET) bucket\e[0m";\
	)

# Copy the dataproc code to execute in the bucket,
# copying main.py to path gs://code-dataproc-serverless/main.py
build_code:
	@echo "\e[32mCopying dataproc's code to GS bucket $(FUNCTION_CODE_BUCKET_NAME)\e[0m"
	@gsutil cp ../scripts/main.py gs://$(CODE_BUCKET_NAME)/dependencies/main.py
	@echo "\e[32mCode copied correctly to $(CODE_BUCKET_NAME)\e[0m"


send_data_files:
	@echo "\e[32mCopying all files in /data to $(RAW_DATA_BUCKET_NAME)\e[0m"
	@gsutil -m cp -r ../data gs://$(RAW_DATA_BUCKET_NAME)
	@echo "\e[32mAll files in /data copied to $(RAW_DATA_BUCKET_NAME)\e[0m"


# Enviar carga de trabajo de Spark a Dataproc Serverless
send_2_dataproc_serverless:
	@gcloud dataproc batches submit pyspark ../scripts/main.py \
		--project=$(PROYECT_ID) \
		--region=$(REGION) \
		--deps-bucket=$(CODE_BUCKET_NAME) \
		--properties="spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"\
		--properties="spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension"\
		--properties="spark.jars.packages=io.delta:delta-core_2.12:1.1.0" \


clean:
	@$(foreach BUCKET,$(BUCKETS),\
	gsutil -m rm -r gs://$(BUCKET);\
	echo "\e[32mDeleted $(BUCKET) bucket\e[0m";\
	)


