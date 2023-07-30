# Use the miniconda3 base image as the starting point.
# This base image includes the Miniconda package manager, which is useful for managing Python packages and environments.
FROM continuumio/miniconda3

# Set the maintainer's email and build date as labels for the image.
LABEL maintainer="prateektandon@alumni.cmu.edu"
LABEL build_date="07/19/2023"

# Install system dependencies using apt-get.
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends wget curl ca-certificates libxml2 unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the 'environment.yml' file into the image.
# This file contains the Conda environment specification.
COPY environment.yml .

# Create a Conda environment named 'eikon' and install the required packages.
RUN conda env create -f environment.yml

# Configure the 'bashrc' to automatically activate the 'tax_align' Conda environment when starting a new shell.
RUN echo "conda activate eikon" >> ~/.bashrc

# Set the shell to use 'bash' with login options and running commands as a login shell.
SHELL ["/bin/bash", "--login", "-c"]

# Verify that the required Python package 'numpy' is installed in the 'eikon' Conda environment.
RUN echo "Make sure modules are is installed:"
RUN python -c "import numpy"

# Copy the 'app.py' script into the image.
COPY app.py .
ADD data .

# Run the app.py to execute the etl process
RUN python app.py

# Move the script files to '/usr/local/bin' and set them as executable.
#RUN cp generate_report.py /usr/local/bin/generate_report.py && chmod a+x /usr/local/bin/generate_report.py;
#RUN cp create_plot.py /usr/local/bin/create_plot.py && chmod a+x /usr/local/bin/create_plot.py;
