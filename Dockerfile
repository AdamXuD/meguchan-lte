FROM python:3.9 as requirements-stage

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

# 更换镜像为国内源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install poetry

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# 更换镜像为国内源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN rm requirements.txt

COPY ./ /app/

