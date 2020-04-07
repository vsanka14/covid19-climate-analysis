# Overview of the project

***This project is still in progress.***

Do weather conditions influence the transmission of COVID-19?

Emerging evidence appears to suggest that weather conditions may influence the transmission of COVID-19, with cold and dry conditions appearing to boost the spread. In this project, I analyze the association between weather and confirmed COVID-19 cases in US states. The objective is to build a model which can determine the relationship between weather conditions and the disease. Data will then be visualized this on a map-based application, and using the model users can see the rate of growth in each state based on future weather forecasts.

##### Contents  
<p align="center">
<b><a href="#data-collection">Data Collection</a></b>
|
<b><a href="#data-processing">Data Processing</a></b>
|
<b><a href="#hypothesis">Hypothesis</a></b>
|
<b><a href="#modelling">Modelling</a></b>
|
<b><a href="#results">Results</a></b>
|
<b><a href="#app">Visualization App</a></b>
|
<b><a href="#potential-issues-and-model-improvement">Potential issues and model improvement</a></b>
|
<b><a href="#references">References</a></b>
</p>


<a name = "data_collection"/>

## Data Collection: 

- US Cases Data: [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)
- Historical Weather data: Built [Historical Weather Scraper Tool](https://github.com/vsanka14/historical-weather-scraper.git) to scrape temperature, humidity, wind and precipitation data from [WunderGround History](https://www.wunderground.com/history). 

## Hypothesis: 

- For USA, regions with temperature higher than 59 degree farenheit (15 degree celsius) and 75% humidity encounters less spread of covid-19 cases than others. 

- A cross-sectional study (see references) correlated cases with mean temperature explored the effect of temperature on transmission in 429, mainly Chinese, cities. They found that for every 1℃ increase in the minimum temperature led to a decrease in the cumulative number of cases by 0.86. Another modelling study found that the current spread suggests a preference for cool and dry conditions. The outbreak epicenters such as China’s central province of Hubei, South Korea, Japan, Iran, Northwestern America and Northern Italy share an average temperature of 5°C to 11°C (41°F to 52°F) and 47% to 79% humidity.

- Our hypothesis, therefore, is that area with average temperature and humidity level higher than these regions will see a decrease in the spread of the virus. 

- After experimentation, I have set the threshold of temperature at 59 degree farenheit and humidity at 75% humidity. You can toggle with the temperature and humidity parameters to identify the suitable climate conditions for your hypothesis, based on the country of your analysis. These numbers will be subtracted from the max value of temperature and the overall humidity during the day of USA states in the modelling analysis.


## Data processing: 

- The number of confirmed coronavirus cases (our dependent/response variable) will be log-transformed to make it follow a normal distribution as per the assumption of statistical analysis, since the original data is skewed highly in selected states. 

## Modelling: 

- Naive OLS estimate is utilized for simplicity and ease of interpretation; 

**Model 1 for Infected cases**: log (Number of cases on Mar 16) = α(T emperature − 15C) + β(Humidity − 75%) + error term

**Model 2 for Growth rate**: log (Cases on Mar 16/ Cases on Mar 3) = α(T emperature − 15C) + β(Humidity − 75%) + error term

- For expansion of research, more complex models with proper causal analysis controlling for confounding variables should be created to capture the true effect of temperature and humidity on the spread of coronavirus cases.  

## Results: 

***Yet to be implemented***

## App: 

***Yet to be implemented***


## Potential issues and model improvement: 
***Yet to be implemented***

## References: 

1. https://www.cebm.net/covid-19/do-weather-conditions-influence-the-transmission-of-the-coronavirus-sars-cov-2/ 
2. https://www.medrxiv.org/content/10.1101/2020.03.18.20036731v1.full.pdf+html
