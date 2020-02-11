FROM python:3.7-alpine

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . /app.py /app/
COPY . /Datahandler.py /app/
COPY . /login_controller.py /app/
COPY . /Validation.py /app/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
	
CMD ["python", "app.py"]	
	
