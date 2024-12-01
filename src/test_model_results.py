import unittest
from model_results import ModelTrainer
import joblib
import os

class TestModelTrainer(unittest.TestCase):

    def test_model_creation(self):
        """Verifica que el modelo se pueda instanciar correctamente."""
        trainer = ModelTrainer()
        self.assertIsNotNone(trainer, "El objeto ModelTrainer no debería ser None")

    def test_model_training(self):
        """Verifica que el modelo se entrene sin errores."""
        trainer = ModelTrainer()
        X_train = [[1], [2], [3], [4]]
        y_train = [2, 4, 6, 8]
        trainer.train(X_train, y_train)
        self.assertTrue(hasattr(trainer, 'model'), "El modelo debería estar entrenado y tener un atributo 'model'")

    def test_model_prediction(self):
        """Verifica que el modelo pueda realizar predicciones."""
        trainer = ModelTrainer()
        X_train = [[1], [2], [3], [4]]
        y_train = [2, 4, 6, 8]
        trainer.train(X_train, y_train)
        prediction = trainer.model.predict([[5]])
        self.assertAlmostEqual(prediction[0], 10, places=1, msg="La predicción debería ser cercana a 10")

    def test_model_save_and_load(self):
        """Verifica que se pueda guardar y cargar el modelo."""
        trainer = ModelTrainer()
        X_train = [[1], [2], [3], [4]]
        y_train = [2, 4, 6, 8]
        trainer.train(X_train, y_train)

        # Guardar el modelo
        joblib.dump(trainer.model, 'test_model.pkl')
        self.assertTrue(os.path.exists('test_model.pkl'), "El archivo de modelo debería existir")

        # Cargar el modelo
        loaded_model = joblib.load('test_model.pkl')
        self.assertIsNotNone(loaded_model, "El modelo cargado no debería ser None")

        # Limpieza
        os.remove('test_model.pkl')

if __name__ == '__main__':
    unittest.main()
