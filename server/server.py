import grpc
from grpc_reflection.v1alpha import reflection
import os
from concurrent import futures

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import model_pb2, model_pb2_grpc
import joblib, pandas as pd

MODEL_PATH=os.environ.get('MODEL_PATH', "model.pkl")
MODEL_VERSION=os.environ.get('MODEL_VERSION', "v1.0.0")

class PredictionService(model_pb2_grpc.PredictionServiceServicer):
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            iris = load_iris()
            self.model = RandomForestClassifier(random_state=42)
            self.model.fit(iris.data, iris.target)
            joblib.dump(self.model, MODEL_PATH)
        else:
            self.model = joblib.load(MODEL_PATH)

    def Predict(self, request, context):
        df = pd.DataFrame([{
            "feature1": request.feature1,
            "feature2": request.feature2,
            "feature3": request.feature3,
            "feature4": request.feature4
        }])
        pred = self.model.predict(df)[0]
        confidence = self.model.predict_proba(df)[0][pred]
        return model_pb2.PredictResponse(prediction=str(pred), confidence=str(confidence), modelVersion=MODEL_VERSION)

    def Health(self, request, context):
        return model_pb2.HealthResponse(status="ok", modelVersion=MODEL_VERSION)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    model_pb2_grpc.add_PredictionServiceServicer_to_server(PredictionService(), server)
    SERVICE_NAMES = (
        model_pb2.DESCRIPTOR.services_by_name['PredictionService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()