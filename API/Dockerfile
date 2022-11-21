FROM python:3.10

WORKDIR /usr/src/app

# ./ refers to the WORKDIR
COPY requirements.txt ./

# responsible of installing dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# copy everything in this directory to the container's, copy the source code
COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]