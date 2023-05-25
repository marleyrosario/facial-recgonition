# Facial Recognition Script

This script uses the DeepFace library to perform facial recognition tasks. It downloads images, runs facial recognition, and stores the results in a Google BigQuery table.

# https://github.com/marleyrosario/facial-recgonition

## Dependencies

- Docker
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

- GOOGLE_APPLICATION_CREDENTIALS: Your Google Cloud JSON Credential File.

## Building the Docker Image

You can build the Docker image using the following command:

```bash
docker build --build-arg GOOGLE_APPLICATION_CREDENTIALS=<Your JSON Credential File> -t <Your Image Name> .
```

docker run -p 8080:8080 <Your Image Name>

  
The added sections include detailed instructions on how to build and run the Docker image for your facial recognition script.
