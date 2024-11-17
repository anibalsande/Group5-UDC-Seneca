# Group 5 | UDC-Seneca | LRM App

## Overview
<!-- TO DO: Add link to accessible PDF of Quick Start Guide-->

The LRM App creates, visualizes, and makes predictions from simple and multiple linear regression models. It provides a graphical interface that allows users to easily interact with the models, using data from various sources, including CSV files, Excel files, and SQLite databases.

## Table of Contents
<!--Finalize TOC at the very end. These are placeholders only at this point. All headings subject to change depending on project progress.--> 
1. [Introduction](#introduction)
2. [System requirements](#system-requirements)
3. [Installation](#installation)
4. [User interface](#user-interface)
    - [Main interface](#main-interface)
    - [Variable selection](#variable-selection)
    - [Model creation](#model-creation)
    - [Save and load models](#save-and-load-models)
5. [Usage instructions](#usage-instructions)
    - [Loading a file](#loading-a-file)
    - [Selecting variables](#selecting-variables)
    - [Model creation and prediction](#model-creation-and-prediction)
    - [Saving and loading models](#saving-and-loading-models)

<!--Does Troubleshooting section need to be added? What about FAQs, Credits, Licence/License?-->


## 1. Introduction
<!-- TO DO: Add more information about name of the app (LRM App?), motivation for app, the target audience, the problem it solves, what we learned -->

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

Before you can use the LRM App, you need to have the following software installed:
- GitHub Desktop
- Python 3.13.0 or later
- Visual Studio Code
- Visual Studio Build Tools.
   
If you do not already have the above software installed, use the instructions below to install them first. 

**To install GitHub Desktop**
1. Download [GitHub Desktop](https://desktop.github.com/download/).
2. Launch the installation file.  
    The program opens automatically after installation.  

**To install Python 3.13.0**
1. Download and launch [Python](https://python.org/downloads/) for Windows.
2. Launch the installation file.
3. In the initial installation window, select Customize installation (see Figure 1).  
    Note: You do not need admin privileges when installing.
   
    ![Screenshot of Python installation options](/images/Python_installation_screenshot.jpg)  
    *Figure 1. Installation options for Python 3.13.0*  

4. In the Optional Features window, select all features except "for all users" (see Figure 2).

    ![Screenshot of Python optional features](/images/Python_optional_features_screenshot.jpg)  
    *Figure 2. Python optional features*  

5. Select Next.
6. In the Advanced Options window, ensure that "Associate files with Python" and "Add Python to environment variables" are checked (see Figure 3).

    ![Screenshot of Python advanced options](/images/Python_advanced_screenshot.jpg)  
    *Figure 3. Python advanced options*  

7. Select Install.

**To install Visual Studio Code**
1. Download [Visual Studio Code](https://code.visualstudio.com/).
2. Launch the installation file and select Next.  
    Note: You must accept the license agreement to continue installation.
3. In the Select Additional Tasks window, ensure "Register Code as an editor for supported file types" and "Add to PATH" are checked (see Figure 4).

    ![Screenshot of Select Additional Tasks window for Visual Studio Code](/images/VSCsetuppagescreenshot.jpg)  
    *Figure 4. Select Additional Tasks for VSC setup*  
   
4. Select **Next > Install > Finish**.

**To install Visual Studio Build Tools**
1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022).
2. Launch the installation file and select Continue.
3. Under the heading Desktop & Mobile, select Desktop development with C++ (see Figure 5, box 1).
4. Under the heading Installation details, ensure the C++ CMake tools for Windows component is checked (see Figure 5, box 2).  

    ![Screenshot of installation options for Visual Studio Build Tools 2022](/images/Compiler_installation_screenshot.jpg)
    *Figure 5. Installation options for Visual Studio Build Tools 2022*
5. Select **Install**. 

**To check Visual Studio Code extensions**
1. Open Visual Studio Code.
2. Select **View > Extensions**.
3. If not already installed, install the Pylance, Python, and Python Debugger extensions.
 
### 3. Installation
Installing the LRM App requires cloning its code repository on GitHub Desktop and then running the program through Visual Studio Code. 

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
   
   ![Screenshot of VSC Run Python File icon](/images/VSCRunIconScreenshot.jpg)    
   *Figure 6. VSC Run Python File icon*

   ![Screenshot of LRM App start page](/images/LRMAppStartPage.jpg)
   *Figure 7. LRM App start page*
   
## 4. User interface
This section describes each feature of the LRM App. 

### Main interface
See Figure 8 for a map and legend explaining what each feature of the LRM App does.  

**Legend**
1. Open File - Select this button to select your model's dataset from your computer or drive.
2. Open Model - Select this button to open a previously-saved model you created.
3. Display Area - The main panel of the interface is where your dataset, graph, model, and equations appear.
4. Column Selection - The first menu in this panel, Features, is where you select the independent variable(s) for your model. The second menu, Target, is where you select the dependent variable(s).
5. Preprocessing Options - This panel's menu allows you to confirm what you want the LRM App to do with missing or incomplete information in your dataset. You can remove those rows or fill them with a mean, a median, or a constant.
6. Create Model - This panel allows you to name your model before creating it. You can also create your model without a specific name.
    
### Variable selection

### Model creation

### Save and load models

## 5. Usage instructions
This section takes you step by step through the process of creating, naming, saving, and reloading your own linear regression models and graphs.

### Select your dataset
The first step is to select the dataset you will use to make your model. The LRM App 
### Selecting variables

### Model creation and prediction

### Saving and loading models

<!--Troubleshooting? FAQs? Credits? Licence/License?-->
