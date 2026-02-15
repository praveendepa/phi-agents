FROM python:3.11-slim
ENV PYTHONUNBUFFERED True

ENV APP_HOME /root
WORKDIR $APP_HOME
# COPY /app $APP_HOME/app
COPY /src $APP_HOME/src/
COPY config.json .

RUN pip install --upgrade pip
# COPY requirements.txt .
RUN pip install --no-cache-dir -r  src/phi_agents/requirements.txt

EXPOSE 8080
CMD ["uvicorn", "src.phi_agents.app.my-mainapp:app","--host", "0.0.0.0", "--port", "8080"]