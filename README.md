# Group 5 | UDC-Seneca | LRM App

## Overview

The LRM App creates, visualizes, and makes predictions from simple and multiple linear regression models. It provides a graphical interface that allows users to easily interact with the models, using data from various sources, including CSV files, Excel files, and SQLite databases.

## Table of Contents
1. [Introduction](#introduction)
2. [System requirements](#system-requirements)
    - [Display settings](#display-settings) 
4. [Installation](#installation)
5. [User interface](#user-interface)
    - [Main interface](#main-interface)
    - [Variable selection](#variable-selection)
    - [Model creation](#model-creation)
    - [Save and load models](#save-and-load-models)
6. [Usage instructions](#usage-instructions)
    - [Loading a file](#loading-a-file)
    - [Selecting variables](#selecting-variables)
    - [Model creation, metrics, and prediction](#model-creation,-metrics,-and-prediction)
    - [Saving and loading models](#saving-and-loading-models)
7. [Additional help](#additional-help)


## 1. Introduction
<details>
    <summary>What is the LRM App?</summary>    
    The LRM App is a tool for analyzing data and making predictions from it.
</details>
<details>
    <summary>How does the LRM App analyze data and make predictions?</summary>    
    Using information from you and the power of artificial intelligence, the LRM App creates and visualizes simple and multiple linear regression models. These linear regression models let you analyze historical data patterns and from them predict future data patterns.
</details>
<details>
    <summary>What is artifical intelligence?</summary>    
    Artificial intelligence, or AI, is defined by Google Cloud as "a field of science concerned with building computers and machines that can reason, learn, and act in such a way that would normally require human intelligence or that involves data whose scale exceeds what humans can analyze."  
</details>
<details>
    <summary>What is linear regression?</summary>    
    Linear regression is one of the methods, or algorithms (sets of instructions), by which mathematicians can show statistical information and model relationships between variables. AI can perform the linear regression algorithm in a matter of milliseconds, whereas it would take a human significantly longer.      
</details>
<details>
    <summary>Is the LRM App hard to use?</summary>    
    No. The LRM App has an easy-to-use graphical interface and guides you through the entire data analysis and prediction process, including uploading your dataset, addressing incomplete information, selecting datapoints to focus on, building a visual model and graph, displaying the mathematical formula and expected accuracy, and updating predictions upon receiving new datapoints. The LRM App also lets you save and reload your models quickly, making it indispensable for your research needs.
</details>

## 2. System requirements
The LRM App is designed for a Windows 11 operating system.

### Display settings
For maximum readability and contrast between elements, use the Windows Light mode setting. The LRM App is currently optimized for Light mode.    

## 3. Installation
Follow these steps to installg the LRM App is earequires cloning its code repository on GitHub Desktop and then running the program through Visual Studio Code. 

**To clone the LRM App code repository on GitHub Desktop**
1. From GitHub Desktop, select **File > Clone a repository**.
2. In the URL tab, enter the LRM App's GitHub repository URL: https://github.com/anibalsande/Group5-UDC-Seneca/)  
    Note: The name of the LRM App's code repository is Group5-UDC-Seneca.
3. In Path, enter the location on your computer for the cloned repository.  
    Note: You need to sign into your GitHub account if you are not already signed in to continue.
4. Select **Clone**.  
    The Group5-UDC-Seneca repository now appears in GitHub Desktop. 

**To run the LRM App on Visual Studio Code**
1. From GitHub Desktop, ensure the Group5-UDC-Seneca repository is the Current repository, and select **Open in Visual Studio Code**.  
    The Group5-UDC-Seneca repository now appears in the Explorer panel of Visual Studio Code.
2. Navigate to **Group5-UDC-Seneca > src > main.py**.
3. Select the Run Python File icon (see Figure 6) or select **Run > Run Without Debugging**.  
    The LRM App opens in a separate window (see Figure 7).
   
   ![alt text](/images/VSCRunIconScreenshot.jpg "Screenshot of VSC Run Python File icon")    
   *Figure 6. VSC Run Python File icon*

   ![alt text](/images/LRMAppStartPage.jpg "Screenshot of LRM App start page")
   *Figure 7. LRM App start page*
   
## 4. User interface
This section illustrates and describes each feature of the LRM App. 

### Main interface
See Figure 8 for a map and legend explaining what each feature of the LRM App does.  

   ![alt text](/images/LRMAppMainInterfaceMap.jpg "Screenshot of LRM App Main Interface")  
   *Figure 8. LRM App Main Interface Map*
    
**Legend**
1. Open File Button - Select this button to select your model's dataset from your computer or drive.
2. Display Area Tabs - Selecting these tabs toggles between displaying the data, model, or help page in the Display Area.
3. Open Model Button - Select this button to open a previously-saved model you created.
4. Display Area - The main panel of the interface is where your dataset appears.
5. Column Selection Panel - The first menu in this panel, Features, is where you select the independent variable(s) for your model. The second menu, Target, is where you select the dependent variable(s).
6. Preprocessing Options Panel - This panel's menu allows you to confirm what you want the LRM App to do with missing or incomplete information in your dataset. You can remove those rows or fill them with a mean, a median, or a constant.
7. Create Model Panel - This panel allows you to name your model before creating it.
    
### Variable selection interface
Figure 9, box 1 shows an example of variable selection from a housing dataset. The Feature (independent) variable selected is "total_bedrooms." The vertical bar beside the variable marks it as selected. The Target (dependent) variable selected is "median_house_value" and the vertical bar beside the variable marks it as selected. Upon selecting Confirm Selection, the app highlights the columns showing the selected variables in the Display Area.

   ![alt text](/images/ColumnSelectionPreprocessing.jpg "Screenshot of variable selection and preprocessing options interfaces")
   *Figure 9. Variable selection and preprocessing options interfaces*

### Preprocessing options interface
Figure 9, box 2 shows the preprocessing options available: remove the rows with missing data or NaN (Not a Number) items or fill them with the mean or median value for that column, or fill them with a constant. 

## 5. Usage instructions
This section takes you step by step through the process of creating, naming, saving, and reloading a linear regression model and graph.

### Select your dataset
The first step is to select the dataset you will use to make your model. The LRM App can utilize data in .csv format, Excel spreadsheets, or SQLite databases. 

**To select dataset**
1. Select **Open File**.
2. Navigate to your dataset file.
3. Double-click the file or select it and then select **Open**.
   **Note**: If any NaN items are detected, a dialog box opens to inform you (see Figure 10). Select **OK** to continue.
   
   ![alt text](/images/Missing_NaN_screenshot.jpg "Screenshot of missing NaN information box")     
   *Figure 10. Missing NaN information box*

### Selecting variables
After you open a dataset, its columns will appear under the Features and Target menus in the Column Selection panel (Figure 11, Boxes 1 and 2).
You can select single or multiple independent variables for your Feature(s). You can only select one dependent variable for the Target.     
**Note**: The LRM App can provide the model metrics and equation for a multiple-independent-variable linear regression but cannot graph it. The LRM App can only display a graph for a single-independent-variable or simple linear regression.
 
   ![alt text](/images/VariablesPreprocessingModelMap.jpg "Screenshot with highlighted Column Selection, Preprocessing Options, and Create model panels")     
   *Figure 11. Column selection, Preprocessing options, and Create model panels*

**To select variables**
1. Scroll through the column headings in the Features menu.
2. Select a desired Feature(s) by clicking on it or them.
   A vertical bar appears beside the Feature(s) selected.
4. To deselect a Feature, click it again.
   The vertical bar disappears.
5. Repeat the selection process with the column headings in the Target menu.
6. Select Confirm Selection.     
   The Selection Confirmed dialog box opens to summarize your choices for Input Columns (Features) and Output Column (Target).
7. Select **OK**. 
   
### Data Preprocessing
Before you can create a model, you must remove or fill in missing or unreadable values ("NaN" or "Not a Number" values) in the dataset.

**To preprocess data**
1. Open the menu under Preprocessing Options by selecting the down arrow.
2. Select the appropriate option (remove or fill with the mean, median, or a constant) for the NaNs in your dataset.
3. If you select Fill NaN with a Constant, enter the constant in the field labelled "Enter constant value".
4. Select Apply Preprocessing.     
   A Success message appears to confirm preprocessing.
5. Select **OK**.
    
### Model creation, metrics, and prediction
You are ready to create your model, view the metrics, and make predictions.

**To create model and view metrics**
1. Name your model in the **Create description** field.
   **Note**: You can create a model with no name. A dialog box appears asking if you are sure before you can continue. You can still save the model.
2. Select **Create model**.     
   The model results appear in the Display Area under the Model tab.     
   The Model Metrics box (Figure 12, Box 1) shows the name, coefficient of determination, mean squared error, and model formula.     
   For a simple (single-independent-variable) linear regression, the model results also display a graph (Figure 12, Box 2).     
   **Note**: No graph appears for a multiple linear regression.

   ![alt text](/images/ModelResults.jpg "Screenshot of model results")
   *Figure 12. Model results*

**To make a prediction**
1. In the Make a Prediction panel (Figure 12, Box 3), enter the Feature value you wish to use to make a prediction.
2. Select **Realizar Predicción**.     
   The predicted Target value appears in the **Predicción** field (Figure 12, Box 4).

### Saving and loading models
After creating your model, you can save it from the Model tab and reload at a later time.

**To save a model**
1. From the Model tab, select **Save model** (Figure 12, Box 5).
2. Navigate to the location where you want to save.
3. Enter your desired file name and select **Save**.
   The file saves with a .joblib extension, and a dialog box appears to inform you of the successful save.
4. Select **OK**.

**To reload a model**
1. From the Data tab, select **Open Model**.
2. Navigate to the location of your saved model's .joblib file.
3. Double-click the file or select it and select **Open**.
   A dialog box opens to inform you the model has been loaded successfully.
4. Select **OK**.

### Additional help
For a quick summary of the LRM App's usage instructions, click the **Help** tab at any time while using the app (Figure 13). 

![alt text](/images/HelpTab.jpg "Screenshot of help tab contents")     
   *Figure 13. Help tab display*
