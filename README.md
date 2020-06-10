# Overview of the project

***The frontend of this project is still under implementation.***

Do weather conditions influence the transmission of COVID-19?

With COVID-19 becoming a pandemic, and the number of people being affected in the world increasing exponentially, it is important that we seek to understand the factors which influence its transmission. Studies have been conducted in the past to determine the seasonality of various infectious diseases such as influenza, common cold, etc. Flu typically arrives in the winters, whereas diseases such as typhoid increase in the summer. Thus, it is only natural to question if we can expect a seasonal pattern with COVID-19.


##### Contents  
<p align="center">
<b><a href="objective"> Objective of the project </a></b>
<b><a href="#data-collection">Data Collection</a></b>
|
<b><a href="#data-processing">Data Processing</a></b>
||
<b><a href="#modelling">Modelling</a></b>
|
<b><a href="#results">Results</a></b>
|
<b><a href="#app">Visualization Application</a></b>
|
<b><a href="#potential-issues-and-model-improvement">Potential issues and model improvement</a></b>
|
<b><a href="#references">References</a></b>
</p>


## Ojective of the project:
In this project, I analyze the Italian regions from a time period of 24th February 2020 to May 5th 2020. The goal is to develop a model which can explain the progression of COVID-19 as influenced by climatic factors. In order to visualize the model results, I will also develop a visualization tool with a ‘time travel’ feature which gets the weather forecasts of the next 10 days and predicts the estimated number of cases for each state.

## Data Collection: 

- Italian Cases Data: [COVID-19 Italia GitHub repository​](https://github.com/pcm-dpc/COVID-19)
- Historical Weather data: Built [Historical Weather Scraper Tool](https://github.com/vsanka14/historical-weather-scraper.git) to scrape temperature, humidity, wind and precipitation data from [WunderGround History](https://www.wunderground.com/history). 


## Data processing: 

- Instead of using the temperature and humidity values for each day, an exponentially-weighted moving average (EMA) of the maximum temperature and maximum humidity per day was used. This is because COVID-19 symptoms can appear 2-14 days after exposure to the virus.
- The number of confirmed coronavirus cases (our dependent/response variable) will be log-transformed to make it follow a normal distribution as per the assumption of statistical analysis, since the original data is skewed highly in selected states. 

## Modelling: 

- Independent variables: Temperature and Humidity
- Dependent variable: log(new_cases) per day
- I transformed the independent variables into a second degree polynomial and apply quadratic regression using ordinary least squares.

**Model for Growth rate**: log(​new_cases) = β​<sub>1</sub>(mat) + β​<sub>2</sub>(mat)​<sup>2</sup> +​ β​<sub>3</sub>(mah) + β​<sub>4</sub>(mah)<sup>2</sup> +​ Error Term


## Results: 

The model gave highly significant results for each state, with p-values less than 0.05. This indicates strong evidence against the null hypothesis, that there is no relationship between temperature, weather and humidity. Thus we can reject the null hypothesis and accept the alternative hypothesis. The R squared values for 19 out of 20 states were more than 50%, 16 out of 20 states were more than 80% and 13 out of 20 states were more than 90%. This means that the model was able to explain the variance in the data pretty well.

The coefficient values of temperature and humidity were used to determine the kind of effect temperature and humidity have on a region. I analyzed the the coefficient values for each state and depending on their sign (negative or positive), I categorized the state as either one of the four following categories:
1. β​<sub>1</sub> > 0, β<sub>2</sub>​ > 0: cases keep increasing (ii) 
2. β​<sub>1</sub> < 0, β​<sub>2</sub> < 0: cases keep decreasing (dd) 
3. β​<sub>1</sub> > 0, β​<sub>2</sub> < 0: cases increase first, and then decrease (id)
4. β<sub>1</sub>​ < 0, β​<sub>2</sub> < 0: cases decrease first, and then increase (di)

The maximum relative humidity was fixed at its 50th percentile to analyze the relationship between temperature and the number of cases in each state. The results (Figures 10 and 11) showed that while there are regions where cases are decreasing with increasing temperature, the trend is not consistent across italy. The split between the number of cases increasing and decreasing based on temperature is equal at 50%. The mean temperature past which the cases decrease is 60.54°F (or 15.55°C). This result follows the pattern of cases decreasing in areas with temperature greater than 11°C. However, there are almost an equal number of regions which show that the cases increase in number past a threshold temperature of 64.50°F (or 18.27°C).

The maximum temperature was fixed at its 50th percentile to analyze the relations between humidity and the number of cases in each state. The results (Figures 12 and 13) for humidity show that the mean relative humidity past which cases decrease is 82.67%. This result also follows the pattern of cases decreasing in number with areas greater than 79% humidity. However, similar to the case of temperature, there is almost an equal number of states which denote that the number of cases increase past the mean threshold humidity of 85.56%.

It should also be noted that out of the 18 regions analyzed, only Piemonte showed negative association in cases with both temperature and humidity.


## App: 

**Backend**:

I built the REST APIs using Python Flask. I chose Flask because the model was built in Python, and it was easy to utilize the results of the model in the same language.
    
The backend server needed two APIs for the following purposes:
1. get_initial_data: ​Sending initial data of confirmed cases, temperature and humidity values to the frontend (Request Method: GET)
2. get_multiple_predictions: ​Making predictions and sending results back to the frontend (Request Method: POST)

**Frontend**:

I am currently building the frontend using React and D3.


## Potential issues and model improvement: 
- Collinearity between temperature and humidity is a big factor. Regression models assume that the independent variables are not related to each other. 100% humidity at 8°C is the equivalent of 28.25% at 30°C. 
- Other metrics in addition to p-values and R-squared measures can be used to measure the relationship between cases and meteorological factors.
- There are many other factors which impact the progression of COVID-19, for example, region-specific socio-economic status, human interactions, transmission due to population density etc. 
- This study should also be extended to more countries to help understand the issue more.

## References: 

1. https://www.cebm.net/covid-19/do-weather-conditions-influence-the-transmission-of-the-coronavirus-sars-cov-2/ 
2. https://www.medrxiv.org/content/10.1101/2020.03.18.20036731v1.full.pdf+html
