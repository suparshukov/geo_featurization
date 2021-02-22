FROM python

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY src/geo_featurization /app/
