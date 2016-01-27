FROM python:2.7

# Install Dependencies
RUN apt-get update -y \
    && apt-get install -y \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download Google App Engine SDK
RUN cd ~ \
    && mkdir appenginesdk \
    && cd appenginesdk \
    && wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.31.zip -O z.zip \
    && unzip z.zip \
    && rm z.zip

# Define start script
CMD ["/root/run.sh"]
