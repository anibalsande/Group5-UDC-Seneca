# Technical and Developer Notes
This document contains product development information for the LRM App including product context, purpose, goals, design, quality assurance testing, and reference material for future developers. 

## Table of Contents
<!--Finalize TOC at the very end. These are placeholders only at this point. All headings subject to change depending on project progress.--> 
1. [Project Overview](#project-overview)
   - [About Collaborative Online International Learning (COIL)](#about-collaborative-online-international-learning-(coil))
   - [LRM App Project Purpose and Goals](#LRM-App-project-purpose-and-goals)
   - [Target Audience](#target-audience)
   - [Intended Platforms and Technology](#intended-platforms-and-technology)
   - [User Flow](#user-flow)
2.[About Linear Regression Modeling](#about-linear-regression-modeling)

3. [Project-Specific Information](#project-specific-information)
   - [The Group 5-UDC-Seneca Team, Roles, and Responsibilities](#the-group-5-udc-seneca-team,-roles,-and-responsibilities)

## Project Overview 
Group 5-UDC-Seneca is a group of students from the Universidade da Coruña in A Coruña, Spain and Seneca Polytechnic in Toronto, Canada who are working together through the Collaborative Online International Learning (COIL) program. During their collaboration, Group-5-UDC-Seneca develop and document, using the Agile project management approach, the **LRM App**, an online linear regression software application. In doing this, the students learn about
- linear regression modeling
- artificial intelligence and machine learning in the context of linear regression modeling
- industry standards and expectations for software development
- industry standards and expectations for software documentation
- Agile working environments
- soft skills needed to collaborate effectively and efficiently despite different geographical regions, cultures, and languages.  

### About Collaborative Online International Learning (COIL)
The COIL approach supports cultural awareness, cultural competency, and globalization in the modern economy. It does this by pairing professors and their classes at two different accredited institutions in two different countries or cultures to work on a collaborative learning project. The professors collaborate on the planning and design of the project. The students then collaborate on organizing, discussing, completing, and presenting their project with the assistance of technology that supports their meeting and communicating virtually. Along the way, the students get to know and trust each other and work together comfortably and effectively even though they are in different geographic locations, may have language barriers and cultural differences, and are often in different time zones. 

### LRM App Project Purpose and Goals
Group 5-UDC-Seneca received the following instructions for their collaborative learning project:

> A client contacts your development team and tells you:

> "I want to hire you to make an application that allows me to create and visualize simple and multiple linear regression models from data stored in csv, excel, and databases (SQLite) files, and make predictions with them. I also want it to allow me to save the models, load them, and make predictions. The application must have a graphical interface that allows me to do all of the above."

Group 5-UDC-Seneca understand that besides creating the application (app) described, their goals for the project also include working together to create the app efficiently and in accordance with scheduled project deadlines using Agile development principles, just as they would in real life for a real business client.

### Target Audience
In planning the LRM App, Group 5-UDC-Seneca decided to target as broad an audience as possible. They wanted to ensure users understood the app was versatile and not limited to certain datasets or certain fields of study. For example, the app can be used to estimate the market price of a house based on number of bedrooms. A realtor could use the app for that purpose. The app can also be used to predict food consumption in a restaurant based on average age of the patrons. A restauranteur could find the app very helpful for that study. 

Also, they wanted to ensure non-technically-proficient users could use the app as easily as users who are very tech-savvy. An app that is complicated to use or assumes prior experience with similar apps would undesirably limit the size of the target audience. 

To meet the goal of making the app appropriate and easy to use for as many people as possible, Group 5-UDC-Seneca implemented a simple graphical interface with simple labels and descriptions along with optional tooltips. The simple visuals, labels, and descriptions do not suggest that the app is more suited for any one dataset or another. The tooltips, when activated, display additional information and guidance for less-technically-proficient users but otherwise do not clutter the interface or get in the way of advanced users who do not need that information. 

### Intended Platforms and Technology
The LRM App functions in both Windows and Mac desktop environments. However, as of v.1.0 (26 November 2024), the interface is optimized for a 14-inch Windows display. Slight visual differences on other machines may occur. There is currently no plan to adapt the LRM App for tablets or smartphones. 

### User Flow
For reference, Figure 1 shows the User Flow created for the LRM App.

![alt text](/images/process.jpg "Screenshot of LRM App User Flow diagram")
*Figure 1. LRM App User Flow*

## About Linear Regression Modeling
**Regression** is a statistical method that mathematically describes the interdependent relationship between, essentially, one numerical value (called the dependent variable) and another (called the independent variable(s)). **Linear regression** is the most commonly used form of regression. **Simple linear regression** describes the relationship between one dependent variable and one independent variable. **Multiple linear regression** describes the relationship when there is more than one independent variable. The reason for the name "linear" regression is because the relationship can be illustrated as a straight line on a graph, also called the line of best fit. It can also be described in a mathematical formula:

>Basic simple linear regression formula: Y = β0 + β1X, where Y is the dependent variable, X is the independent variable, β1 is the slope of the line, and β0 is the intercept (the value of Y when the line crosses the Y axis or the X value is zero).
>
>Basic multiple linear regression formula (assuming two independent variables): Y = β0 + β1X1 + β2X2, where Y is the dependent variable, β0 is the value of Y when the independent variables are equal to zero), X1 is the first independent variable, X2 is the second independent variable, and β1 and β2 are estimated regression coefficients.

Because linear regression can illustrate a relationship between variables as a graph or a mathematical formula, it is possible, with algebra and sufficient reliable datapoints, to predict the unknown value of a Y variable as long as one knows the value of the X variable(s). This is why the X or independent variable is also called the "predictor" or "feature" variable, and the Y or dependent variable is also called the "response" or "target" variable.

For a video explanation of the above concepts with graphs and a practical example, see

[![An Introduction to Linear Regression Analysis](https://img.youtube.com/vi/zPG4NjIkCjc/0.jpg)](https://www.youtube.com/watch?v=zPG4NjIkCjc) 

from David Longstreet of StatisticsFun. 

## Linear Regression Modeling, Artifical Intelligence (AI), and Machine Learning (ML)
Sir Francis Galton ("Regression analysis," 2024) first used the term "regression" in 1885 when describing his research conclusions after examining the relationship between the physical heights of fathers and their sons. He observed that the sons "regress" to the mean of the population instead of conforming to the heights (tall or short) of their fathers. While Galton only used linear regression in this biological context, statisticians have been using regression, mostly linear, ever since in different contexts. 

Since Galton's time, the goals, methods, and possibilities of regression analysis have advanced as technologies, most notably AI and its subset ML, have made it easier and faster to calculate linear regressions, handle gigantic datasets, and train linear regression models to predict a target variable. 

According to Stryker and Kavlakogulu of IBM (2024), AI is "technology that enables computers and machines to simulate human learning, comprehension, problem solving, decision making, creativity and autonomy," and machine learning is a derivative concept that involves training algorithms to create models and make predictions from data. Linear regression is one of the machine learning algorithms available, and it can be trained using **supervised learning**, a process by which it uses labeled data sets to learn how to predict outcomes accurately. The machine learns the mapping between the variables in the training data, and from that, it learns to make informed predictions of the labels of new data. 



Traditional statistics focuses on using linear regression to test hypotheses and estimate parameters, but AI and ML focus on making predictions from the data. Whereas traditional statistics depends on data meeting certain requirements like normal distribution, independence among observations, constant error variance, and a strictly linear relationship between the dependent and independent variables, AI-powered linear regression models can often handle imperfect data and still make reliable predictions through methods like regularization. Further, AI can quickly process far more complex datasets and algorithms than traditional human-powered statistical approaches ever can (Saragadam, Asim, Etukuru, Stosik, Kulshrestha, and Brewton, 2024).

The result of AI and ML advances 
The LRM App must create and visualize linear regression models as well as allow the user to make reliable predictions from them. Practical eff 



Some practical examples of linear regression modeling and prediction include predicting (Baraka, 2024):
- the sale price of a home based on variables like the age of the house in years, the value of neighbouring homoes, and/or the number of parks or schools nearby
- the sale price of a stock based on variables like the company's profitability, its costs, the number of competitors, and/or the value of its assets
- the number of future viral infections based on variables like population size, population density, and/or air temperature
- the competitive performance of an athlete based on variables like the athlete's age, physical statistics, and/or years of experience
- the future height of a child based on variables like mother's height, father's height, nutritional factors, and/or environmental factors.


## Linear Regression, Artificial Intelligence (AI), and Machine Learning (ML)


### About Artificial Intelligence (AI) and Machine Learning (ML)



## Project-Specific Information
Group 5-UDC-Seneca has five members.  All of them contributed to the development and documentation of the LRM App in diverse ways. 

### The Group 5 Team, Roles, and Responsibilities
- Aníbal Sande González (UDC): Scrum Master, Researcher and Developer
- Carla Vázquez Barreiros (UDC): Researcher and Developer
- Claudia Fernández Vilela (UDC): Researcher and Developer
- Sofía García Perez (UDC): Researcher and Developer
- Ann Velez (Seneca): Technical Documentation Writer
  
All of the UDC students worked on research and development of the LRM App (see [Developer Notes](#Developer-Notes) for detailed information), allowing all of them to gain experience in different aspects of the product instead of focusing on a single area. 

The Scrum Master had additional responsibilities:
- assigning tasks to team members, taking into consideration their preferences and skills
- checking to ensure all sprint objectives were met in a timely manner
- taking initiative on addressing challenges in completing tasks on time
- leading communication with the Technical Documentation Writer who was the only team member in a different country and school
- leading the design arrangement of elements within the LRM App

The Technical Documentation Writer prepared a Documentation Plan, interviewed the UDC students as Subject Matter Experts on the app's development, prepared this Technical and Developer Notes document for internal use, and wrote the README file for external users of the LRM App. To do this the Technical Documentation Writer learned to use Markdown in GitHub and became familiar with the GitHub workflow involving branch management and making pull and push requests for changes to the documentation files in the repository.  

### Group 5 Reflections on Collaboration
Group 5-UDC-Seneca found the COIL project positive and enriching both academically and professionally. The collaboration required working across different languages (Spanish and English) time zones (a six-hour difference), and disciplines (Artificial Intelligence and Technical Communication), and it worked seamlessly with the help of the shared technologies for communication and project management: Taiga, GitHub, Zoom, MS Teams, and e-mail.


### Developers Considerations

### Testing 



## About Agile



# Developer Notes
The Developer Notes contain the devs' summaries of their work process and how they solved problems in coding the app. It can include Agile product roadmaps, backlogs, standards, plans, estimates, schedules, test strategy, release checklist, working papers, reports.


This document contains summaries of the developers' work process and details as to how they solved problems in coding the app.



**Multiple Regression Handling**
Challenges in implementing the multiple regression functionality of the LRM App include:
- handling the Features menu as a list
- regression line plotting 
- model training
- output visualization
Solutions:
**Compatibility**
The app behaves differently in different environments. For example, the dark mode in Windows shows unexpected dark backgrounds.
Solution: Besides finding ways to standardize behavior across environments, we are overriding default settings where necessary.



What was your development process like? For example, how often did you meet, and how did you plan your sprints?
After the Sprint Review and Retrospective sessions, we conducted Sprint Planning meetings on Tuesdays. During these, we selected tasks based on our availability. When tasks overlapped or required similar actions, we used to choose both to streamline our work.
Throughout the sprint, we worked individually but ensured regular communication about progress and challenges. Toward the end of each sprint, we reviewed and integrated all components. 
 
We also held several collaborative sessions, some focused on working together on the code and others to share research findings, decide on the libraries to use, and align our work.
 
How did you manage the GitHub repository and code? Did you establish a particular policy or rules for branches and merges/commits?
We created a develop branch to work independently from the documentation part. Initially, we committed directly to this branch, as the tasks were straightforward and completed quickly. Later, as tasks became more complex, we created separate branches for new functionalities. Once these were complete, we merged them back into the develop branch.
 
Can you give me specific details of any problems you encountered while developing and how you solved them?
Learning PyQt6
At the beginning, working with PyQt6 was challenging because it was a new library for us. Translating our "on-paper" layout designs into code required significant effort. PyQt6 has a steeper learning curve than other libraries, but its advanced features made it the best choice. By the end of the first few weeks, we met our expectations and continuously refactored the code to accommodate new functionalities.
Integrating the Results Window
In the last sprint, we replaced the results window with a tab integrated into the main application. The challenge was including a layout from a separate module in the primary window while ensuring it updated dynamically with each new model.
Defining the User Flow
Initially, it was difficult to outline the app’s flow and provide documentation. However, we made progress by developing the app in a way that minimized the need for refactoring earlier functionalities while optimizing existing features as needed.

## References
Baraka, S. (2024). Multiple (Linear) Regression: Formula, Examples, and FAQ. ***Indeed.com***. Retrieved from [https://www.indeed.com/career-advice/career-development/multiple-regression](https://www.indeed.com/career-advice/career-development/multiple-regression)   

Regression analysis. (2024, November 21). In ***Wikipedia***. [https://en.wikipedia.org/wiki/Regression_analysis#](https://en.wikipedia.org/wiki/Regression_analysis#) 
