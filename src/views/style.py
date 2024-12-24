def get_main_stylesheet():
    return """
    QMainWindow {
        background-color: #0b5394;
        font-family: 'Bahnschrift';
    }

    QGroupBox {
        font-family: 'Bahnschrift';
        font-size: 14px;
        color: black;
    }

    QTabWidget::tab-bar {
        alignment: center;
    }

    QTabBar::tab:selected {
        background: #073763; 
    }

    QTabBar::tab {
        background: #0A4B85;
        font-family: 'Bahnschrift';
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        height: 20px;
        width: 150px;
        padding: 5px;
        margin: 0px;
        margin-left: 10px;
        margin-right: 10px;
    }

    QTabBar::tab:hover {
        background: #0B1E3E;
    }

    QTabWidget::pane {
        border: none;
        background: white; 
    }

    QTabBar::tab:disabled {
        background: #d3d3d3;  
        color: #a9a9a9; 
    }

    QPushButton {
        background-color: #0B1E3E; 
        color: white;
        border-radius: 5px;
        font-weight: bold;
        font-size: 12px;
        height: 40px;
        width: 200px;
    }
    QPushButton:hover {
        background-color: #F6BE00;
        color: #0B1E3E;
    }

    QMessageBox {
        color: #0A4B85;
    }

    QListWidget::item {
        background-color: white;  /* Fondo blanco para los items del QListWidget */
    }

    QListWidget::item:disabled {
        background-color: #d0d0d0;  /* Fondo gris para los items deshabilitados */
        color: #888888;  /* Color de texto más suave para los items deshabilitados */
    }

    QListWidget::item:selected {
        background-color: #B0C4DE;
        color: #0B1E3E;
        border-left: 2px solid #0B1E3E;
    }

    QGroupBox QLabel {
        font-family: 'Bahnschrift'; 
        font-size: 14px; 
    }

    """

def get_header_stylesheet():
    return """
    QWidget {background-color: #0b5394;}

    QPushButton {
        background-color: #F6BE00; 
        color: #0B1E3E;
        border-radius: 5px;
        font-weight: bold;
        padding-left: 15px;
        padding-right: 15px;
        height: 28px;
        width: 170px;
    }
                                         
    QPushButton:hover {
        background-color: #0B1E3E;
        color: white;
    }

    
    QLabel {
        color: white;
        font-family: 'Bahnschrift';
        font-size: 16px;
    }
    """


def get_prediction_stylesheet():
    return """
        QPushButton {
            background-color: #0B1E3E; 
            color: white;
            border-radius: 5px;
            font-weight: bold;
            font-size: 12px;
            padding: 0px;
        }
        QPushButton:hover {
            background-color: #F6BE00;
            color: #0B1E3E;
        }
    """

def get_tab_style(index, current_step):
    """Return style for a tab based on its state."""
    if index < current_step:
        # Past steps (blue = completed)
        return """
            background-color: #0b5394;  /* Blue */
            color: white;
            font-weight: bold;
            border: none;
            border-bottom: 2px solid #073763;
        """
    elif index == current_step:
        # Current step (yellow highlight)
        return """
            background-color: #ffd966;  /* Yellow */
            color: black;
            font-weight: bold;
            border: none;
            border-bottom: 2px solid #f1c232;
        """
    else:
        # Future steps (gray and inactive)
        return """
            background-color: #f0f0f0;
            color: #b0b0b0;
            font-weight: normal;
            border: none;
            border-bottom: 2px solid #d0d0d0;
        """
