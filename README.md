# Facial Recognition Script

This script uses the DeepFace library to perform facial recognition tasks. It downloads images, runs facial recognition, and stores the results in a Google BigQuery table.

## Dependencies

- Python 3
- google-cloud-storage
- os
- pandas
- requests
- json
- csv
- flask
- DeepFace

## Environment Variables

The script uses the following environment variables:

- PROJECT_ID: The project ID for Google Cloud.
- BUCKET_NAME: The name of the storage bucket in Google Cloud.
- BQTABEL: The name of the BigQuery table to store results.

## Running the Script

1. Set the environment variables PROJECT_ID, BUCKET_NAME, and BQTABEL.
2. Run the script using the command `python FacialRecognition.py`.

The script will download images, run facial recognition tasks, and store the results in the specified BigQuery table.
