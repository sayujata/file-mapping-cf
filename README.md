# Cloud function to generate a single CSV file with a defined header from 3 different header CSV files.

This _Cloud Function_ is triggered on **http** event, which retrieve 3 files from GCP storage and upload transformed file into storage

## Usage

1. Get this repository in local

   ```shell
   git clone git@github.com:sayujata/file-mapping-cf.git
   ```

2. Enter into folder created from git clone

   ```shell
   cd file-mapping-cf
   ```

3. Install `python` dependencies
   ```shell
   pip3 install -r requirements.txt
   ```
   
## Prerequisite

1. Create GCP storage bucket and update '.github\fm-env-variable.yaml' file with created storage bucket name
2. Upload the files from input file directory to GCP storage

## Environment Variables

| Variable         | Description                        | Type     |
| ---------------- | ---------------------------------- | -------- |
| GCP_STORAGE_NAME | GCP Storage name to read/put files | `string` |

> You can find values to above env variables in fm-env-variable.yaml config

## Use below command to deploy the cloud function

gcloud functions deploy file-mapping-cf --project=<project_id> --region=europe-west1 --source=. --trigger-http --entry-point=file_mapping_operation --runtime=python39 --env-vars-file=.github\fm-env-variable.yaml
> Replace the project_id with GCP project id

## Configuration Options

Cloud functions must be enabled in the GCP project.

## Future scope

1. Accept file details (file Name, header, file location etc) from http request.
2. Read file column header mapping from database or http request
