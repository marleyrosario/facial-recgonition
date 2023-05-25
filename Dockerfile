FROM python:3.10-slim
ARG GOOGLE_APPLICATION_CREDENTIALS
ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}

RUN groupadd --gid 15555 notroot \ 
    && useradd --uid 15555 --gid 15555 -ms /bin/false notroot\
    && chown -R notroot:notroot /home/notroot

RUN apt-get update && apt-get install -y python3-opencv
ADD race_model_single_batch.h5 /home/notroot/.deepface/weights/
ADD gender_model_weights.h5 /home/notroot/.deepface/weights/
ADD age_model_weights.h5 /home/notroot/.deepface/weights/

USER notroot
ADD requirements.txt /

ENV PATH="${PATH}:/home/notroot/.local/bin"
RUN pip install --no-cache-dir -r /requirements.txt

ADD ${GOOGLE_APPLICATION_CREDENTIALS} /

ADD main.py /
CMD exec gunicorn --bind :8080 --workers 2 --threads 8 --timeout 0 --log-level critical main:app 
