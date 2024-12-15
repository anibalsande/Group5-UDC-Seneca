import joblib
import pickle
from sklearn.linear_model import LinearRegression


class ModelHandler:
    def __init__(self):
        self.model_info = None
        self.model = None

    def load_model(self, file_path):
        """Upload model from a file (.joblib or .pkl)"""
        try:
            if file_path.endswith('.joblib'):
                self.model_info = joblib.load(file_path)
            elif file_path.endswith('.pkl'):
                with open(file_path, 'rb') as f:
                    self.model_info = pickle.load(f)
            else:
                raise ValueError("Unsupported file format. Use .joblib or .pkl.")
            
            # Restore model for prediction
            if 'coefficients' in self.model_info and 'intercept' in self.model_info:
                self.model = LinearRegression()
                self.model.coef_ = self.model_info['coefficients']
                self.model.intercept_ = self.model_info['intercept']

        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")

    def get_model_info(self):
        """Devuelve la información cargada del modelo."""
        if not self.model_info:
            raise ValueError("No model loaded.")
        return self.model_info

    def save_model(self, file_path, model_info):
        """Save model in an specified format."""
        try:
            if file_path.endswith('.joblib'):
                joblib.dump(model_info, file_path)
            elif file_path.endswith('.pkl'):
                with open(file_path, 'wb') as f:
                    pickle.dump(model_info, f)
            else:
                raise ValueError("Unsupported file format. Use .joblib or .pkl.")
        except Exception as e:
            raise RuntimeError(f"Failed to save model: {str(e)}")