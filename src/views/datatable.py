from PyQt6.QtWidgets import QTableView, QAbstractScrollArea, QHeaderView
from PyQt6.QtGui import QColor, QStandardItemModel, QStandardItem

class DataTable(QTableView):
    def __init__(self):
        super().__init__()
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.setStyleSheet(""" 
            QTableView {
                background-color: #f0f0f0;
                gridline-color: #d0d0d0;
                font-size: 12px;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #dcdcdc;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #b0b0b0;
            }
        """)
        self.model = QStandardItemModel()
        self.setModel(self.model)

    def update_table(self, data, input_columns=None, output_column=None):
        """Update the table with data, highlighting input/output columns and NaN values."""
        if data is None:
            return
        
        self.model.clear()  # Reset the model
        self.model.setHorizontalHeaderLabels(data.columns)

        # Colors for highlighting
        input_color = QColor("#FFDDC1")  # Light peach
        output_color = QColor("#D1E8FF")  # Light blue
        nan_color = QColor("#FFAAAA")  # Light red for NaN values

        # Populate the model
        for row in data.itertuples(index=False):
            items = []
            for col_index, value in enumerate(row):
                item = QStandardItem(str(value) if value == value else "NaN")
                column_name = data.columns[col_index]
                
                # Highlight input and output columns
                if input_columns and column_name in input_columns:
                    item.setBackground(input_color)
                elif output_column and column_name == output_column:
                    item.setBackground(output_color)

                # Highlight NaN values
                if value != value:
                    item.setBackground(nan_color)

                items.append(item)
            self.model.appendRow(items)

        # Adjust column widths
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)