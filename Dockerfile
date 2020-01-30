FROM alpine:3.11

EXPOSE 3031
WORKDIR /app

# --no-cache reduces final image size
RUN apk update && \
    apk add --no-cache uwsgi-python python3

# COPY manifest first to take advantage of build stages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Finish copying rest of application
COPY . .

# We use http to make it easier to run local and proxy_pass. However,
# you are STRONGLY encouraged to put nginx in front of this as
# this invocation does act the same as the `--http` option.
# `--http` isn't supported in most distro versions of uwsgi.
# Read more at: https://uwsgi-docs.readthedocs.io/en/latest/ThingsToKnow.html

CMD [ "uwsgi", \
      "--socket", "0.0.0.0:3031", \
      "--uid", "uwsgi", \
      "--plugins", "python", \
      "--protocol", "http", \
      "--wsgi", "app:app" ]

