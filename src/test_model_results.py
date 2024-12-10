import unittest
from model_results import ModelTrainer
import joblib
import os

class TestModelTrainer(unittest.TestCase):

    def test_model_creation(self):
        """Verify that the model can be instantiated correctly"""
        trainer = ModelTrainer()
        self.assertIsNotNone(trainer, "The ModelTrainer object should not be None")

    def test_model_training(self):
        """Verify that the model trains without errors."""
        trainer = ModelTrainer()
        X_train = [[1], [2], [3], [4]]
        y_train = [2, 4, 6, 8]
        trainer.train(X_train, y_train)
        self.assertTrue(hasattr(trainer, 'model'), "The model should be trained and have a 'model' attribute.")

    def test_model_prediction(self):
        """Verify that the model can make predictions."""
        trainer = ModelTrainer()
        X_train = [[1], [2], [3], [4]]
        y_train = [2, 4, 6, 8]
        trainer.train(X_train, y_train)
        prediction = trainer.model.predict([[5]])
        self.assertAlmostEqual(prediction[0], 10, places=1, msg="The prediction should be close to 10.")

    def test_model_save_and_load(self):
        """Verify that the model can be saved and loaded."""
        trainer = ModelTrainer()
        X_train = [[1], [2], [3], [4]]
        y_train = [2, 4, 6, 8]
        trainer.train(X_train, y_train)

        # Guardar el modelo
        joblib.dump(trainer.model, 'test_model.pkl')
        self.assertTrue(os.path.exists('test_model.pkl'), "The model file should exist.")

        # Cargar el modelo
        loaded_model = joblib.load('test_model.pkl')
        self.assertIsNotNone(loaded_model, "The loaded model should not be None")

        # Limpieza
        os.remove('test_model.pkl')

if __name__ == '__main__':
    unittest.main()
