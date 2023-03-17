# Steam Hours Capstone Project
## Project Description

The gaming industry now makes more money than the film and music industry combined. We have decided to look into what makes a customer play games for large amounts of time. We will look into what features if any contribute to the number of gameplay hours and create a machine learning model to estimate the hours played for certain types of games. With the model we will be able to predict the value of a game based on hours played.

## Project Goal

* Discover drivers of hours played from database
* Use drivers to develop a machine learning model to determine value of the product
* This information could be used to further our understanding of which elements contribute to or detract from a person's tendency spend time on a game

## Initial Thoughts

We believe that Multiplayer games with a competitive element, such as battle royales, like Fortnite, have the highest game hours. We believe that the games with that are free to play will have very low hours. We also believe that the publisher and developer of the game will matter to hours played.

## The Plan

* Acquire the data
* Prepare the data
* Explore the data
    * Answer the following questions
        * Does the Developer of the game matter to hours played?
        * Does the Publisher of the game matter to hours played?
        * Does the initial price of the game matter to hours played?
        * Does the genre the game is under matter
* Develop a Model to predict hours played
    * Use key words identified to build predictive models of different types
    * Evaluate models on train and validate data samples
    * Select the best model based on precision
    * Evaluate the best model on test data samples
* Draw Conclusions

## Data Dictionary

| Feature | Definition |
|:--------|:-----------|
|name| The title of the game|
|developer| The name of the company that developed the game|
|publisher| The name of the compnay that published the game|
|positive| Number of positive reviews|
|negative| Number of negative reviews|
|average_forever| Average hours played since game was published|
|average_2weeks| Average hours played in past two weeks|
|median_forever| The median hours played since game was published|
|median_2weeks| The median hours played in past two weeks|
|ccu| The number of concurrent users|

## Steps to Reproduce
1) Clone this repo
2) Acquire the data from Steam
3) Put the data in the file containing the cloned repo
4) Run notebook

## Takeaways and Conclusions
Through our exploration we were able to find that a games publisher, developer, genre, and release price are all useful in predicting whether or not a game will fall under 'high hour' games. We were also able to create a model that predicts which hour bin a game will fall under with 96% accuracy and a precision of 88% on high hour games which is our targeted class.

## Next Steps

1) In game purchases would be great to study especially for the free games
2) Change the way we are using grid search in order to optimize modeling hyperparameters for predicting our target class as opposed to highest overall accuracy
3) Acquire the release dates for games
4) Explore the platform used for games to see its effect on average hours played
5) Acquire system requirements for games to see its effect on avg hours played
6) Do more exploration on developers to determine whether or not they are productive to our model