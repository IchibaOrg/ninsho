FROM public.ecr.aws/docker/library/python:3.12.8-slim-bookworm

WORKDIR /app/

# Always look in /app when trying to import modules.
ENV PYTHONPATH ${PYTHONPATH}:/app/

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential=12.9 \
    libffi-dev=3.4* \
    curl=7* \
    postgresql-client-15=15.14* \
    unzip=6.0-28 \
    gettext-base=0.21-12 \
    libpq-dev=15.14* \
    awscli=2.9.19-1 \
    jq=1.6-2* \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache


# move required folders files to container
# copy dependency files first (better caching)
COPY pyproject.toml poetry.lock ./
RUN pip install poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

COPY alembic.ini gunicorn.conf.py ./
COPY migrations ./migrations
COPY ninsho ./ninsho


# migrations are here for now!
CMD ["sh", "-c", "alembic upgrade head && gunicorn ninsho.app:app"]

