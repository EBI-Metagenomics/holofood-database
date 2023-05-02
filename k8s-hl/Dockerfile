FROM python:3.11

ENV USER=docker
ENV UID=7123
ENV GID=1347
RUN addgroup --gid "$GID" "$USER" \
   && adduser \
   --disabled-password \
   --gecos "" \
   --home "$(pwd)" \
   --ingroup "$USER" \
   --no-create-home \
   --uid "$UID" \
   "$USER"

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD manage.py /app/manage.py
ADD config/data_config.json /app/config/data_config.json
ADD config/local.env /app/config/local.env
ADD holofood /app/holofood
ADD static /app/static
ADD templates /app/templates

WORKDIR /app

EXPOSE 8000

RUN python manage.py compilescss
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "holofood.wsgi"]