# Technical and Developer Notes
This document contains product development information for the LRM App including product context, purpose, goals, design, quality assurance testing, and reference material for future developers. 

## Table of Contents 
1. [About the Project](#about-the-project)
   - [Collaborative Online International Learning (COIL)](#about-collaborative-online-international-learning-(coil))
   - [LRM App Project Purpose and Goals](#LRM-App-project-purpose-and-goals)
   - [Target Audience](#target-audience)
   - [Intended Platforms and Technology](#intended-platforms-and-technology)
   - [User Flow](#user-flow)
2. [About Linear Regression Modeling](#about-linear-regression-modeling)
   - [Linear Regression Modeling Past and Present](#linear-regression-modeling-past-and-present)
   - [AI and ML's Effect on Linear Regression Usage and Application](#AI-and-ML's-effect-on-linear-regression-usage-and-application)
   - [The LRM App in Context](#the-LRM-app-in-context)
3. [About the Team and the Development Process](#about-the-team-and-the-development-process)
   - [Team Members and Roles](#team-members-and-roles)
   - [Agile and Scrum Methodology](#agile-and-scrum-methodology)
4. [Developer Notes](#developer-notes)
   - [Software Development in GitHub](#software-development-in-github)
   - [Sprint Reviews, Retrospectives, and Planning](#sprint-reviews,-retrospectives,-and-planning)
   - [Sprint Increment Summaries](#sprint-increment-summaries)
   - [Functional Test Plan](#functional-test-plan)
5. [References](#references)

## About the Project
Group 5-UDC-Seneca is a group of students from the Universidade da Coruña in A Coruña, Spain and Seneca Polytechnic in Toronto, Canada who are working together through the Collaborative Online International Learning (COIL) program. During their collaboration in Fall 2024, Group-5-UDC-Seneca developed and documented, using the Agile project management approach, the **LRM App**, an online linear regression software application. In doing this, the students learned about
- linear regression modeling
- artificial intelligence and machine learning in the context of linear regression modeling
- industry standards and expectations for developing software
- Agile principles and Scrum methodology for developing software
- soft skills needed to collaborate effectively and efficiently despite different geographical regions, cultures, and languages.  

### Collaborative Online International Learning (COIL)
The COIL approach supports cultural awareness, cultural competency, and globalization in the modern economy. It does this by pairing professors and their classes at two different accredited institutions in two different countries or cultures to work on a collaborative learning project. The professors collaborate on the planning and design of the project. The students then collaborate on organizing, discussing, completing, and presenting their project with the assistance of technology that supports their meeting and communicating virtually. Along the way, the students get to know and trust each other and work together comfortably and effectively even though they are in different geographic locations, may have language barriers and cultural differences, and are often in different time zones. 

### LRM App Project Purpose and Goals
Group 5-UDC-Seneca received the following instructions for their collaborative learning project:

> A client contacts your development team and tells you:

> "I want to hire you to make an application that allows me to create and visualize simple and multiple linear regression models from data stored in csv, excel, and databases (SQLite) files, and make predictions with them. I also want it to allow me to save the models, load them, and make predictions. The application must have a graphical interface that allows me to do all of the above."

Group 5-UDC-Seneca understood that besides creating the application (app) described, their goals for the project also included working together to create the app efficiently and in accordance with scheduled project deadlines using Agile development principles, just as they would in real life for a real business client.

### Target Audience
In planning the LRM App, Group 5-UDC-Seneca decided to target as broad an audience as possible. They wanted to ensure users understood the app was versatile and not limited to certain datasets or certain fields of study. For example, the app can be used to estimate the market price of a house based on number of bedrooms. A realtor could use the app for that purpose. But the app can also be used to predict food consumption in a restaurant based on average age of the patrons. A restauranteur could find the app very helpful for that study. 

Also, they wanted to ensure non-technically-proficient users could use the app as easily as users who are very tech-savvy. An app that is complicated to use or assumes prior experience with similar apps would undesirably limit the size of the target audience. 

To meet the goal of making the app appropriate and easy to use for as many people as possible, Group 5-UDC-Seneca implemented a simple graphical interface with simple labels and descriptions along with optional tooltips. The simple visuals, labels, and descriptions do not suggest that the app is more suited for any one dataset or another. The tooltips, when activated, display additional information and guidance for less-technically-proficient users but otherwise do not clutter the interface or get in the way of advanced users who do not need that information. 

### Intended Platforms and Technology
The LRM App functions in both Windows and Mac desktop environments. However, as of v.1.0, scheduled for release on 3 December 2024, the interface is optimized for a 14-inch Windows display. Slight visual differences on other machines may occur. There is currently no plan to adapt the LRM App for tablets or smartphones. 

### User Flow
For reference, Figure 1 shows the User Flow for the LRM App.

![alt text](/images/process.jpg "Screenshot of LRM App User Flow diagram")
*Figure 1. LRM App User Flow*

## About Linear Regression Modeling
**Regression** is a statistical method that mathematically describes the interdependent relationship between one numerical value (called the dependent variable) and one or more other values (called the independent variable(s)). **Linear regression** is the most commonly used form of regression. **Simple linear regression** describes the relationship between one dependent variable and one independent variable. **Multiple linear regression** describes the relationship when there is more than one independent variable. The regression is called "linear" because the relationship can be illustrated as a straight line on a graph, also called the line of best fit (for a simple linear regression) or the plane of best fit (for a multiple linear regression). It can also be described in a mathematical formula:

>Basic simple linear regression formula: Y = β0 + β1X
>where Y is the dependent variable, X is the independent variable, β1 is the slope of the line, and β0 is the intercept (the value of Y when the line crosses the Y axis or the X value is zero).
>
>Basic multiple linear regression formula (assuming two independent variables): Y = β0 + β1X1 + β2X2
>where Y is the dependent variable, β0 is the value of Y when the independent variables are equal to zero), X1 is the first independent variable, X2 is the second independent variable, and β1 and β2 are estimated regression coefficients.

Because linear regression can illustrate a relationship between variables as a graph or a mathematical formula, it is possible, with algebra and a sufficient reliable historical data (also called a "dataset" or a set of "datapoints"), to **predict** the unknown value of a Y variable as long as one knows the value(s) of the X variable(s). This is why the X or independent variable is also called the "predictor" or "feature" variable, and the Y or dependent variable is also called the "response" or "target" variable.

For a video explanation of the above concepts, see the following YouTube video, An Introduction to Linear Regression Analysis, from David Longstreet of StatisticsFun:

[![An Introduction to Linear Regression Analysis](https://img.youtube.com/vi/zPG4NjIkCjc/0.jpg)](https://www.youtube.com/watch?v=zPG4NjIkCjc) 

### Linear Regression Modeling Past and Present
Sir Francis Galton ("Regression analysis," 2024) first used the term "regression" in 1885 when describing his research conclusions after examining the relationship between the physical heights of fathers and their sons. He observed that the sons "regressed" to the mean of the population instead of conforming to the heights (tall or short) of their fathers. While Galton only used regression in this biological context, statisticians have been using regression ever since in different contexts. 

Since Galton's time, the goals, methods, and possibilities of regression analysis have advanced as technologies, most notably artificial intelligence (AI) and its subset, machine learning (ML), have made it easier and faster to calculate regressions and make accurate predictions from data. As a point of comparison, economists in the 1960s using electromechanical calculators might need 24 hours to finish calculating the result of one regression ("Regression analysis," 2024), but today, computers routinely perform regression calculations and generate related analytical insights in a matter of seconds or milliseconds.

### AI and ML's Effect on Linear Regression Usage and Application
According to Stryker and Kavlakogulu of IBM (2024), AI is "technology that enables computers and machines to simulate human learning, comprehension, problem solving, decision making, creativity and autonomy," and ML is a derivative concept that involves training algorithms to create models and make predictions from data. Linear regression is one of the ML algorithms available, and it can be trained using **supervised learning**, a process by which the machine uses labeled data sets to learn how to predict outcomes accurately. Through processing many datasets, the machine "learns" the mapping between the variables in the training data, and from that, it learns to make predictions of the labels of new data. 

ML changed the usage and application of linear regression models by making them more reliable for predictions and relevant to many more practical applications than in the past. Traditional statistics focused on using linear regression to test hypotheses, estimate parameters, and make inferences about causation. Predictions were not the main goal. When predictions were made in traditional statistics, the data had to meet certain requirements like normal distribution, independence among observations, constant error variance, and a strictly linear relationship between the dependent and independent variables before the predictions could be considered reliable and valid. 

Unlike in traditional statistics, ML-powered linear regression models focus on making accurate predictions from data. Imperfect data is not as much of an obstacle to predictions as in traditional statistics; ML-powered linear regression models can be given imperfect data and still make reliable predictions using statistical methods like normalization (adjusting values of features to a common scale) or regularization (preventing the model from becoming too fixed or "overfitted" to its training data). And ML-powered models can process massive datasets and complex algorithms with far more speed and far fewer errors than traditional human-powered statistical approaches ever can (Saragadam, Asim, Etukuru, Stosik, Kulshrestha, and Brewton, 2024).

Some practical examples of multiple linear regression modeling and prediction not easily or reliably available before AI and ML made them so include predicting (Baraka, 2024):
- the sale price of a home based on variables including the age of the house in years, the value of neighbouring homes, and the number of parks and/or schools nearby
- the sale price of a stock based on variables including the company's profitability, its costs, the number of competitors, and the value of its assets
- the number of future infections from a virus in a city based on variables including population size, population density, and air temperature
- the future competitive performance of an athlete based on variables including the athlete's age, physical statistics, and years of experience
- the future height of a child based on variables including mother's height, father's height, nutritional factors, and environmental factors.

### The LRM App in Context
The LRM App has an easy-to-use graphical interface and allows users across different fields with varying levels of technical knowledge to upload their own datasets, process the data to handle create and visualize complex linear regression models, and then make statistically supportable predictions from them quickly. To put this in historical context, it was only a few decades ago that a layperson could not have accomplished these tasks without the help of an expert statistician, a specialized computer, and a significant investment of time and effort. But as of 2024, as long as they have good quality datasets, a layperson with a basic knowledge of statistics can use the LRM App and feel confident in the predictions.     

## About the Team and the Development Process
Group 5-UDC-Seneca has five student members and two faculty members. 

### Team Members and Roles

The student members of Group 5-UDC-Seneca and their roles in the project are

- Aníbal Sande González (UDC): Scrum Master, Software Researcher and Developer
- Carla Vázquez Barreiros (UDC): Software Researcher and Developer
- Claudia Fernández Vilela (UDC): Software Researcher and Developer
- Sofía García Perez (UDC): Software Researcher and Developer
- Ann Velez (Seneca): Technical Documentation Writer (Developer)

The faculty members are
- Alberto Alvarellos González (UDC): Product Owner
- Amy Briggs (Seneca): Documentation Manager

Group 5-UDC-Seneca followed the Agile Scrum methodology to complete the project. 

### Agile and Scrum Methodology
**Agile** is a software project management approach or philosophy that emphasizes early and continuous delivery of software to the customer and values "individuals and interactions over processes and tools, working software over comprehensive documentation, customer collaboration over contract negotiation, and responding to change over following a plan" (Beck et al, 2001). The Agile approach involves completing chunks of work in short phases often called "sprints," responding to change quickly, and collaborating and improving on the product throughout. This is in contrast to the **Waterfall** approach where one component or phase of the project must be finished before another one can be started and consequently is not often able to respond to change quickly or deviate from a set plan. 

There are different methodologies that follow Agile principles, and Group 5-UDC-Seneca followed **Scrum**, a common one.   

In Scrum:
- sprints are short - in this project, they were just one week long
- team members hold frequent (often daily) meetings ("scrums") where they discuss their work activities and problem-solve around challenges
- team members have a sprint planning meeting at the beginning of each sprint to plan and assign tasks for that sprint
- team members have a sprint retrospective at the end of each sprint to reflect on what was learned, what went well, and what could be improved for the future
- the Scrum Master is accountable for making sure the task goals for the sprint are met and thereby produce an "increment" of value for the project for that sprint
- the Product Owner manages the backlog of tasks for the project and looks to maximize value from the scrum team's work
- the Documentation Manager ensures documentation meets the project's needs 
- the Developers are responsible for creating the product.

**Note: In the Scrum context, developers include documentation writers as well as software developers since both create or develop the overall product.**

For further information on Agile project management, visit the [Agile Alliance](https://www.agilealliance.org/the-alliance/).

For further information on the Scrum methodology, visit [Scrum.org](https://www.scrum.org/).

## Developer Notes
This section contain the LRM App developers' summaries of their work process and how they solved problems in creating and documenting the LRM App. It serves as a reference for future developers working on the LRM App so they understand the original developers' thought process and work strategy. 

**All developers across both schools** found the COIL project positive and enriching both academically and professionally. The collaboration required working across different languages (Spanish and English) time zones (a six-hour difference), and disciplines (Artificial Intelligence and Technical Communication), and it worked seamlessly with the help of the shared technologies for communication and project management: Taiga, GitHub, Zoom, MS Teams, and e-mail.

**The Scrum Master** found that in addition to leading the assignment of tasks for sprints, he rose to the challenge of taking on a leadership role across the entire project. He took initiative in addressing challenges in completing sprint tasks, led timely communication with the Technical Documentation Writer who was in a different country and time zone, explained details of the functions and programming of the LRM App to the Technical Documentation Writer, and led the design and arrangement of elements within the LRM App, and updated .  

**The Technical Documentation Writer** prepared a Documentation Plan, interviewed UDC students as Subject Matter Experts on the app's development, prepared this Technical and Developer Notes document for internal use, and wrote the README file for external users of the LRM App. To do this the Technical Documentation Writer learned to use Markdown in GitHub and became familiar with the GitHub workflow involving branch management and making pull and push requests for changes to the documentation files in the repository.  

**The Software Researchers and Developers** purposefully chose to take on both research and programming tasks, which allowed all of them to gain experience in different roles and not just single aspects of the LRM App.

### Software Development in GitHub
Following best practices in programming, the team created a separate **develop** branch from the main branch in their GitHub repository to contain their code. Another branch contained the documentation. The software developers found that as programming tasks became more complex, they created more branches for new functionalities and then merged them with the develop branch when they were complete. All separate branches will be merged with the **main** branch by the time of the LRM App version 1.0 release scheduled for 3 December 2024.  

### Sprint Reviews, Retrospectives, and Planning
For Group 5-UDC-Seneca, Tuesdays marked the end and beginning of each sprint. On Tuesdays, they held their Sprint Review and Retrospective session virtually during scheduled online class time. Professor Alberto González assisted the team by interpreting feedback into Spanish or English as necessary so everyone could understand. The team would then conduct its Sprint Planning meeting. The UDC members planned their tasks for the sprint based on their availability and how efficiently they judged they could complete the work. During the sprint, the UDC members mostly worked individually and communicated regularly about progress and challenges, and before the Sprint Review, they would review and integrate the programming components. They also held several collaborative work sessions where some focused on working together on the code and others shared their research findings, decided on the libraries to use, and all aligned their work product for the software.

The Seneca member planned documentation tasks separately from UDC and could not attend the Sprint Planning live due to the language barrier and the timing of the UDC Sprint Planning session coinciding with a separate Seneca class. However, through Taiga, email, MS Teams, and Zoom, all team members were able to communicate about tasks, answer questions, and share information in a transparent and timely way. 

### Sprint Increment Summaries
This section summarizes the increments of value completed in each sprint from Sprint 1 commencing on 1 October 2024 to Sprint 8 ending on 26 November 2024 and notes challenges and solutions when applicable.

**Sprint 1 (1 to 8 October 2024)**
| Increment                                               | Tasks completed                                                                             | Notes                                                      |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:----------------------------------------------------------:|
| Create a GitHub repository and bases for documentation  | Create repository, give access to everyone; create Contributing.md, README.md, GitHub Pages |                                                            |
| Create data import module                               | Develop "Data Import from Files"                                                            |                                                            |

**Sprint 2 (8 to 15 October 2024)**
| Increment                                               | Tasks completed                                                                             | Notes                                                      |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:----------------------------------------------------------:|
| Investigate, test libraries for graphic interfaces (GUI)| Research libraries, develop test                                                            |                                                            |
| Reading datasets using the GUI                          | Create and design graphical interface; insert datasets into repository                      |  Challenge: designing app flow; Solution: choosing to develop app in a way that minimizes need for refactoring earlier functionalities while allowing optimization of existing features as needed                            |
| Interview Subject Matter Experts                        | Prepare questions, schedule & conduct interview, send summary to interviewees for review    |                                                            |

**Sprint 3 (15 to 22 October 2024)**
| Increment                                               | Tasks completed                                                                             | Notes                                                      |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:----------------------------------------------------------:
| Select model inputs and outputs (data columns) using GUI| Select inputs and outputs                                                                   |                                                            |
| Data preprocessing before model creation                | Preprocessing code; adjusting interface                                                     |                                                            |
| Investigate how to create linear models                 | Research scikit-learn; research pandas                                                      |                                                            |
| Learn PyQt6                                             | Meetings to learn PyQt6                                                                     | Challenge: steep learning curve, new library; Solution: persistence and keeping goals in mind (PyQt6 advanced features make it best choice for desired app functionalities)                                                           |
| Finish Documentation Plan                               | Finish documentation plan and distribute                                                    | Challenge: early in process, not much info on design; Solution: Plan to revise documentation plan at future date|

**Sprint 4 (22 to 29 October 2024)**
| Increment                                               | Tasks completed                                                                             | Notes                                                      |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:----------------------------------------------------------:|
| Improve the graphical interface                         | Restructure code, adjust GUI                                                                |                                                            |
| Research on model persistence                           | Research model persistence                                                                  |                                                            |
| Creation of linear models for prediction using GUI      | Create layout, create model                                                                 |                                                            |
| Add model description in graphical interface            | Implement description functionality                                                         |                                                            |

**Sprint 5 (29 October to 5 November 2024)** 
| Increment                                               | Tasks completed                                                                             | Notes                                                      |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:----------------------------------------------------------:|
| Save model to disk with file selection dialog           | Save model coding, share information about this research                                    |                                                            |
| Recover previously saved model                          | Plan development, select file, update model coding                                          |                                                            |
| Training on Good Programming Practices                  | New module: Model results                                                                   |                                                            |
| Improved graphical interface (UX)                       | GUI update, buttons, layouts, etc.                                                          | Time consuming, all UDC team members worked on this. Challenges: some unexpected dark backgrounds in different environments like Windows dark mode. Solution: overriding default settings where necessary and looking for other ways to standardize behavior across environments      |
| Prepare README.md outline                               | Prepare README.md outline; consider separate Quick Start Guide                              | Did not continue separate Quick Start Guide - not necessary|

**Sprint 6 (5 to 12 November 2024)**
| Increment                                               | Tasks completed                                                                             | Notes                                                       |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-----------------------------------------------------------:|
| Make predictions with a created or loaded model         | Create text box; create predictions; handling every situation                                | Multiple regression functionality challenges: handling Features as a list; regression line plotting, model training, and output visualization                                               |
| Continue README document - installation                 | Drafted installation instructions with images                                               |                                                             |
| Walkthrough with Technical Documentation Writer         | Scrum Master walked Technical Documentation Writer through LRM App                          | Very helpful walkthrough session, exchanged feedback on software and documentation       |
| Start Technical and Developer Notes                     | Start draft Technical and Developer Notes and discuss contents with team, request info      |                                                             |

**Sprint 7 (12 to 19 November 2024)**
| Increment                                               | Tasks completed                                                                             | Notes                                                       |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-----------------------------------------------------------:|
| Automated testing                                       | Test create model, fixing automated tests, test loading model, test predictions, test saved |                                                             |
| Individual project reports                              | Scrum Master individual report                                                              |                                                             |
| Modularize and organize interface                       | Adjust interface and modularize                                                             | After replacing results window with tab integrated into main application, the challenge was including a layout from a separate module in the primary window while ensuring it updated dynamically with each new model.                                                    |
| Continue README - usage and interface                   | Drafted usage and interface sections                                                        |                                                             |  
| Continue Technical and Developer Notes                  | Continue Technical and Developer Notes and request further info from team                   | Information received from Scrum Master to allow completion of Technical and Developer Notes                      |

**Sprint 8 (19 to 26 November 2024)**
| Increment                                               | Tasks completed                                                                             | Notes                                                       |
|:-------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|:-----------------------------------------------------------:|
| Creation of a Functional Test plan before release       | Create spreadsheet for functional test plan                                                 | See linked image of functional test plan as of 22 November 2024. Can be updated prior to LRM App v.1.0 release on 3 December 2024                                                          |
| Improve interface                                       |                                                                                             |                                                             |
| Finish Technical and Developer Notes to November 25     | Finished Technical and Developer Notes to November 25, 2024                                 | This documentation is due at Seneca on November 26; can be revised 
 up to December 3, 2024 as LRM App will still be improved to then                                                              |

### Functional Test Plan
For reference, the [Functional Test Plan for the LRM App](/images/Pruebas_Manuales_22NOV2024.pdf) as of 22 November 2024 (in the original Spanish) is included with these notes. 

## References
Baraka, S. (2024). Multiple (Linear) Regression: Formula, Examples, and FAQ. ***Indeed.com***. Retrieved from [https://www.indeed.com/career-advice/career-development/multiple-regression](https://www.indeed.com/career-advice/career-development/multiple-regression)   

Beck et al. (2001). Manifesto for Agile Software Development. Retrieved from [https://agilemanifesto.org](https://agilemanifesto.org/)

Saragadam, H., Asim, U., Etukuru, R.,  Stosik, D.,  Kulshrestha, V., & Brewton, J. (2024). How does AI's linear regression differ from traditional statistics? ***LinkedIn.com***. Retrieved from [https://www.linkedin.com/advice/3/how-does-ais-linear-regression-differ-from-6u77e](https://www.linkedin.com/advice/3/how-does-ais-linear-regression-differ-from-6u77e)

Regression analysis. (2024, November 21). In ***Wikipedia***. [https://en.wikipedia.org/wiki/Regression_analysis#](https://en.wikipedia.org/wiki/Regression_analysis#) 
