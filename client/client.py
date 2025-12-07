import grpc
import model_pb2, model_pb2_grpc

channel = grpc.insecure_channel("localhost:8080")
stub = model_pb2_grpc.PredictionServiceStub(channel)

request = model_pb2.PredictRequest(feature1=5.7, feature2=2.8, feature3=4.5, feature4=1.3)
response = stub.Predict(request)
print("Prediction:", response.prediction) #versicolor
print("confidence:", response.confidence)
print("modelVersion:", response.modelVersion)