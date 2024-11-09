# Group 5 | UDC-Seneca | LRM App

## Overview
<!-- TO DO: Add link to accessible PDF of Quick Start Guide-->

The LRM App creates, visualizes, and makes predictions from simple and multiple linear regression models. It provides a graphical interface that allows users to easily interact with the models, using data from various sources, including CSV files, Excel files, and SQLite databases.

## Table of Contents
<!--Finalize TOC at the very end. These are placeholders only at this point. All headings subject to change depending on project progress.--> 
1. [Introduction](#introduction)
2. [Getting started](#getting-started)
  - [System requirements](#system-requirements)
  - [Installation](#installation)
3. [User interface](#user-interface)
  - [Main interface](#main-interface)
  - [Variable selection](#variable-selection)
  - [Model creation](#model-creation)
  - [Save and load models](#save-and-load-models)
4. [Usage instructions](#usage-instructions)
  - [Loading a file](#loading-a-file)
  - [Selecting variables](#selecting-variables)
  - [Model creation and prediction](#model-creation-and-prediction)
  - [Saving and loading models](#saving-and-loading-models)

<!--Does Troubleshooting section need to be added? What about FAQs, Credits, Licence/License?-->

## 1. Introduction
<!-- TO DO: Add more information about name of the app (LRM App?), motivation for app, the target audience, the problem it solves, what we learned -->

### What is the LRM App? 
The LRM App is a tool for analyzing data and making predictions from it. 

### How does the LRM App do this?
Using information from you and the power of artificial intelligence, the LRM App creates and visualizes simple and multiple linear regression models. These linear regression models let you analyze historical data patterns and from them predict future data patterns. 

### What is artificial intelligence?
Artificial intelligence, or AI, is defined as "a field of science concerned with building computers and machines that can reason, learn, and act in such a way that would normally require human intelligence or that involves data whose scale exceeds what humans can analyze." ([Google Cloud](https://cloud.google.com/learn/what-is-artificial-intelligence#artificial-intelligence-defined))

### What is linear regression? 
Linear regression is one of the methods, or algorithms (a set of instructions), by which mathematicians can show statistical information and model relationships between variables. AI can perform the linear regression algorithm in a matter of milliseconds, whereas it would take a human significantly longer.  

### Is the LRM App hard to use?
No. The LRM App has an easy-to-use graphical interface and guides you through the entire data analysis and prection process, including
  - uploading your dataset from common formats like .CSV, Excel, and SQLite and addressing incomplete information
  - focusing on the datapoints from your dataset that are important to you
  - building a visual model and a graph of the data
  - displaying the mathematical formula and the expected accuracy of predictions
  - making predictions upon receiving new datapoints

The LRM App also lets you save and reload your models quickly, making it indispensable for your research needs.    

## 2. System requirements
The LRM App is designed for a Windows 11 operating system.

Before you can use the LRM App, you will need to have the following software installed:
- Python 3.13.0 or later
- Visual Studio 2022 or another C++ compiler.
   
If you do not already have the above software installed, use the instructions below to install them first. 

**To install Python 3.13.0**
1. Download [Python](https://python.org/downloads/) for Windows.
2. Launch the installation file.
3. In the initial installation window, select Customize installation (see Figure 1).
   Note: You do not need admin privileges when installing.
![Screenshot of Python installation options](Python_installation_screenshot.jpg)
*Figure 1. Installation options for Python 3.13.0*
4. In the Optional Features window, select all features except "for all users" (see Figure 2).
![Screenshot of Python optional features](Python_optional_features_screenshot.jpg)
*Figure 2. Python optional features*
5. Select Next.
6. In the Advanced Options window, ensure that "Associate files with Python" and "Add Python to environment variables" are checked (see Figure 3).
![Screenshot of Python advanced options](Python_advanced_screenshot.jpg)
*Figure 3. Python advanced options
7. Select Install and wait for the installation to finish.

**To install Visual Studio**
1. Install [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/).
2. Under the heading Desktop & Mobile, select the Desktop development with C++ option on the installation menu (see Figure 4).
3. Ensure that the C++ CMake tools for Windows component is checked (see Figure 2).
![Screenshot of installation options for Visual Studio Build Tools 2022](Compiler_installation_screenshot.jpg)
*Figure 4. Installation options for Visual Studio Build Tools 2022*
4. Select Install and wait for the installation to finish.

**To check Visual Studio extensions**
1. Open Visual Studio
2. Select **View > Extensions**.
3. If not already installed, install the Pylance, Python, and Python Debugger extensions.
 
### Installation
Installing the LRM App requires cloning its code repository on GitHub and then running the program on your compiling software.

**To clone the LRM App code repository on Visual Studio**
1. Open Visual Studio.
2. From the opening screen, select Clone a repository (see Figure 5).
![Screenshot of Visual Studio start page with Clone a repository selected](VisualStudioStartPagescreenshot.jpg)
3. In Repository location, enter the location of the LRM App's source code on GitHub: https://github.com/anibalsande/Group5-UDC-Seneca/)
4. In Path, enter the location on your computer for the cloned repository.
   Note: You might need to sign into your GitHub account if you are not already signed in.
6. Select Clone.
   The LRM App code repository now appears in Visual Studio's Solution Explorer-Folder View.
   Note: If the Solution Explorer-Folder View does not appear, open it from **View > Solution Explorer** or with **Ctrl+Alt+L**.

**To run the LRM App on Visual Studio**
1. Open 

## 3. User interface

### Main interface

### Variable selection

### Model creation

### Save and load models

## 4. Usage instructions

### Loading a file

### Selecting variables

### Model creation and prediction

### Saving and loading models

<!--Troubleshooting? FAQs? Credits? Licence/License?-->
