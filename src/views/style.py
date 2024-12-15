def get_main_stylesheet():
    return """
    QMainWindow {
        background-color: #0b5394;
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
