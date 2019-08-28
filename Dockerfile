FROM python:3.6.8
MAINTAINER "famri@alterra.id"
RUN mkdir -p /backend
COPY /e_commerce_project /backend
RUN pip install -r /backend/requirements.txt
WORKDIR /backend
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
