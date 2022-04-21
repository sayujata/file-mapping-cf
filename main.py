
import csv
from google.cloud import storage
import functions_framework
import file_mapping_constants as fmconstants
import os

gcp_storage_name = os.environ.get(fmconstants.GCP_STORAGE_NAME)


@functions_framework.http
def file_mapping_operation(request):
    download_file_blob(gcp_storage_name, fmconstants.FILE_DETAILS)

    with open(f'{fmconstants.TEMP_DIR}{fmconstants.FINAL_OUTPUT_FILE_NAME}', 'w', newline='', encoding=fmconstants.ENCODING_LATIN_1) as output_csvfile:
        filewriter = csv.writer(output_csvfile)
        filewriter.writerow(fmconstants.OUTPUT_FILE_HEADER)
        fileheader = []
        for file in fmconstants.FILE_DETAILS:
            with open(f'{fmconstants.TEMP_DIR}{file}', newline='', encoding=fmconstants.ENCODING_LATIN_1) as csvfile:
                data = csv.reader(csvfile, quotechar='|')
                fileheader = next(data)

                for row in data:
                    filerow = []
                    if fileheader == fmconstants.FILE_HEADER_1:
                        filewriter.writerow(row)
                    elif fileheader == fmconstants.FILE_HEADER_2:
                        filerow.insert(0, row[2])
                        filerow.insert(1, row[4]+" " + row[6])
                        filerow.insert(2, row[0])
                        filerow.insert(3, row[1])
                        filerow.insert(4, row[7])
                        filerow.insert(5, row[3])
                        filerow.insert(6, row[5])
                        filewriter.writerow(filerow)
                    elif fileheader == fmconstants.FILE_HEADER_3:
                        filerow.insert(0, row[0])
                        filerow.insert(1, row[3])
                        filerow.insert(2, '')
                        filerow.insert(3, row[5])
                        filerow.insert(4, row[4])
                        filerow.insert(5, row[2])
                        filerow.insert(6, row[1])
                        filewriter.writerow(filerow)

    upload_file(gcp_storage_name, fmconstants.FINAL_OUTPUT_FILE_NAME)
    return "File Operation Completed"


def download_file_blob(bucket_name, file_details):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    for file_name in file_details:
        blob = bucket.blob(file_name)
        blob.download_to_filename(f'{fmconstants.TEMP_DIR}{file_name}')
        print("File {} downloaded successfully  from Bucket {}.".format(
            file_name, bucket_name))


def upload_file(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(f'{fmconstants.TEMP_DIR}{file_name}')
    print("File {} uploaded successfully to Bucket {}.".format(
        file_name, bucket_name))
