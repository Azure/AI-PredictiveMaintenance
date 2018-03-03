# Format: FROM    repository[:version]
FROM       python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["simulator.py"]
