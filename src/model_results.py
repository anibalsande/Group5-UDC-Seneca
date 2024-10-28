from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt

class ModelResultWindow(QDialog):
    def __init__(self, formula, r2, mse, X, y, y_pred, input_columns, output_column, data):
        super().__init__()
        self.setWindowTitle("Linear Model Results")
        self.setFixedSize(800, 600)

        # Guardar datos para verificar tipos
        self.data = data  # Almacenar los datos para el uso posterior

        # Layout principal
        layout = QVBoxLayout()

        # Mostrar la fórmula del modelo y métricas
        model_info = QLabel(
            f"Model Formula: {formula}\nR²: {r2:.2f}\nMSE: {mse:.2f}"
        )
        model_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(model_info)

        # Verificar si todas las columnas de entrada son numéricas para graficar
        if all(self.data[col].dtype.kind in 'fi' for col in input_columns):  # Verificar que todas las columnas sean numéricas
            plt.figure()
            for i in range(X.shape[1]):
                plt.scatter(X[:, i], y, label=f"Data Points for {input_columns[i]}")
                plt.plot(X[:, i], y_pred, color="red", label="Regression Line")
            plt.xlabel('Input Columns')
            plt.ylabel(output_column)
            plt.title("Linear Regression Fit")
            plt.legend()
            plt.savefig("temp_model_plot.png")
            plt.close()

            # Mostrar el gráfico en QLabel
            graph_label = QLabel()
            pixmap = QPixmap("temp_model_plot.png")
            graph_label.setPixmap(pixmap)
            graph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(graph_label)
        else:
            # Si no es numérico, muestra un mensaje
            no_plot_label = QLabel("No plot available as input data is not numeric.")
            no_plot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_plot_label)

        # Botón para cerrar
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Configurar el layout
        self.setLayout(layout)
