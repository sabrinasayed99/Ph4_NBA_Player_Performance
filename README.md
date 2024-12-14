# Predicting Jalen Brunson's Impact on Team Success
![d7a05fe0-05a1-11ef-b4d3-c5b110488063](https://github.com/user-attachments/assets/3a043496-b8f4-4d56-8ff1-bd66eb97ba4d)

## Author : [Sabrina Sayed](https://github.com/sabrinasayed99)


## Problem:
Can we predict the outcome of a game based solely on one player's performance? Jalen Brunson is a 2-time MVP and star player of the Knicks NBA team. How much does his performance weigh into the team's success in a game?



## Data Overview: 
The data was sourced and scaped from Basketball Reference using a data pipeline and web scraping techniques.

The target variable we are predicting is the Win-Loss Margin of a game. I created a classification system to bin the margins into 6 class:

- Tight Loss/Tight Victory (1-5pts)
- Medium Loss/Medium Victory (6-19pts)
- Blowout Loss/Blowout Victory (20+ pts)


Features: 70 features
- Categorical: Team, Opponent, Home/Away, Season
- Numerical: Per Game, Per Season Averages, Advanced Stats
            Points, Assists, Steals, 3 Pointers, Minutes Played
            Field Goal %, Free Throw %, Plus/Minus
            Player Efficiency Rate, Effective FG %, True Shooting %

Limitations:
  - Class Imbalance
  - Very small data set (467, 70)

# Methods:
- Linear Regression (baseline model)
- RandomForest Classifier
- XGBoost Classifier
I used various encoding and scaling techniques including OneHotEncoder, StandardScaler, and LabelEncoder. The models were tuned with GridSearch Cross Validation Hyperparameter tuning techniques. 

# Data Analysis:

Through data exploration, I learned that there was a major shift in Brunson's performance between the first 3 seasons and the last 3 seasons of his career related to his performance. This can be seen through the distribution plots below:

![Distribution_of_Points_Per_Game_by_Season](https://github.com/user-attachments/assets/5570e9a8-3c44-4d2a-8886-bb1eb3010eab)
![Minutes_Played_Per_Game_by_Season](https://github.com/user-attachments/assets/7bc20405-6b61-4c14-a807-41fd643ccf84)
![Plus_Minus_Per_Game_by_Season](https://github.com/user-attachments/assets/a68267e5-4b2d-4360-910e-f2033025ffb3)

We can see his performance improves significantly and his impact on the team also improves. This can most likely be attributed to his switch to the Knicks in 2022. The change in his teammates and environment could be a big factor in how his performance enhanced.  

# Results:
The best model was a RandomForest Classifier which produced an accuracy of 40%
![Confusion_Matrix](https://github.com/user-attachments/assets/7c4750a4-c8a4-4120-b13a-582c256f3c0e)

The model is having a very hard time predicting the the smaller classes. We can attribute this to both a lack of information from the limited size of the data, the inherent difficult of this problem, and the class imbalance.

![ROC_Curve](https://github.com/user-attachments/assets/51364dc3-cb0d-4624-9b9f-68ae0247c21c)

The ROC curve shows that on the cross validation set the model is able to do well in predicting the minority classes, but when given the test set it is not confident in making those same predictions.

![Feature_Importance](https://github.com/user-attachments/assets/33ea738a-f305-45e2-8e45-d045e97b73f6)

The most important features for the model are Plus/Minus score, Minutes Played per Game, Field Goal percentage per Game, and Game Score.


# Interpreting the Model with SHAP
![SHAP_Summary_Plot](https://github.com/user-attachments/assets/81a1c46f-9208-466c-8684-e1685a06a22a)

#### Minutes Played
Minutes played has strong interactions with Field Goals and Field Goal attempts based on the size of the dots. This suggests that when Brunson players longer he tends to score more and attempt more shots. The relationship appears to be non-linear given the way the dots are spread vertically, which tells us that longer play time doesn't always directly translate to more points. 

#### Field Goal Attempts
Field Goal Attempts and Field Goals have a strong mutual interaction that is represnted by the dense cluster of dots. Blue does suggest sometimes high attempt rates don't lead to proportionally made shots, indicating his margin of error.

#### Home/Away Games
Moderate interaction with field goals. The mix of red and blue dots indicate that home/away games influence shooting performance but not in a consistent direction, which tells us that there are other factors at play..

#### Team and Opponent
Team and Opponent interacts are present but less pronounced, indicating that team matchups may not be a strong predictor of game outcomes. The dots are smaller and more scattered. The clutering with Minutes played tells us that certain matchups effect his playtime. The mix of red and blue dots indicate the team/opponent effects are dependent on other contextual factors rather than systematic correlations.


 ## Next Steps:
Collect more stats form Brunson's teammates for each game and gain more contextal features that inform us on the non-linear relationships and interactions between features.

## Directory:
[Presentation](https://www.canva.com/design/DAGWfOUA7MA/C7TaAAeUlFvrzr8DdZ-Emw/view?utm_content=DAGWfOUA7MA&utm_campaign=designshare&utm_medium=link&utm_source=editor)


## Repository Files:

### Scraped Data
The python script for my data pipeline and scraping requests are located in this folder.

### Logs
Contains logs of scraped data via python script data pipeline

### Cleaned Data
'Cleaned Data' folder contains the cleaned dataframe that was used for exploratory data analysis and modeling

### Data
'Misc Data' Contains the raw data files, databases, and alternative dataframes built from filtering features

### EDA
Contains Exploratry Data Analysis notebook

### Modeling Notebooks
This folder contains 3 notebooks with my various modeling iteratios, tuning, and analysis.

### Images
Contains all data visualizations and plots


