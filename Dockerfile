# Choose proper base image
FROM nvcr.io/nvidia/tlt-streamanalytics:v2.0_py3

# Move to root
WORKDIR /
RUN mkdir training-data

# Install python libraries
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy application
COPY . .
