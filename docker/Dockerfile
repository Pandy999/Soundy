
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.0  
ENV PYTHONUNBUFFERED=1 
RUN git clone https://github.com/Pandy999/Soundy.git
WORKDIR /Soundy
RUN pip install -r /requirements.txt
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /Soundy
USER appuser
CMD ["python", "main.py"]