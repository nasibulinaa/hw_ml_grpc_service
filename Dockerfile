FROM python:3.11-slim
ENV PORT=8080 \
    MODEL_PATH=/app/models/model.pkl \
    MODEL_VERSION=v1.0.0
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN ./utils/gen_proto.sh
EXPOSE 8080
CMD ["python", "server/server.py"]