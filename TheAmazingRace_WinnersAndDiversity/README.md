## Research Question or Organizational Need

This project will take historical data from the past 32 seasons of the reality television show The Amazing Race and will use exploratory data analysis to discover patterns of past winners. The analysis will also hope to show the representation of contestants and if there is a true reflection on the population in the United States.

## Context and Background

Reality televisions shows, especially those based on a game or a race, contain numerous points of data and challenges to determine an overall winner. The Amazing Race is now in its 33rd season and we can look over the historical data of past winners to discover patterns or undiscovered factors that could potentially lead to winners of the show’s future seasons. The Amazing Race combines teams of two as they race around the world finding clues that lead the teams to both physical and mental puzzles. The ability to think quickly and strategically while also pushing themselves mentally separates this show from its competition. Each team is represented by numerous differences in age, occupation, relationship to each other, their hometowns, race, ethnicity, and gender. With 32 seasons of races already behind us, we can observe its ratings to determine reasons for its decline. One factor that could lead to any televisions show’s decline in popularity is its inability to produce various, non-repetitive winners to keep audiences engaged. Having the same teams win again and again might persuade certain audience members to discontinue watching the show. Determining the factors, which ultimately lead to a winning team, when both mental and physical boundaries are pushed, can also be representative of who might be willing to watch future seasons of The Amazing Race.

## Summary of Data Analytics Solution

My solution will be to use Python and Exploratory Data Analysis to determine precisely what factors led to a winning team during the previous 32 seasons of The Amazing Race. The use of statistics for comparison of the data can lead to further insights that will ultimately be displayed visually using Python.

## Benefit to Organization and Decision-Making Process
The primary benefits to the organization of Paramount Global would be to show a unique pattern of winners and if past contestants are true reflections of American race and culture. The ratings for The Amazing Race have been decreasing each season. With a new season airing roughly on a yearly schedule, the ability to bring in new contestants that might reflect America’s diversity more could also potentially bring in higher ratings for the show. Higher ratings could also lead to better sponsorships. We have to consider that the network sponsors are important stakeholders. Paramount Global stakeholders include five executive producers for The Amazing Race: Jerry Bruckheimer, Bertram van Munster (co-creater), Elise Doganieri (co-creator), Jonathan Littman and Mark Vertullo. While the diversity of the executive producers is lacking, their ability to choose the contestants helps to steer the direction of who is and is not watching their program. The audience is potentially the biggest overall stakeholder involved since their choice to watch the show determines the future of the show. A pattern of similar winners is not enjoyable for any fan of game or television shows. Most sports would be extremely lackluster if only one or two teams won consistently, and the same principal applies to reality television and The Amazing Race. The ability for the show to remain fresh by bringing in reflective diversity and unique winners could help ensure that the future of the show is not in jeopardy.

## Goals, Objectives, and Deliverables

The goal of this project is to create a Google Colab Notebook using Python and its libraries to analyze past winners of The Amazing Race.
-	Create datasets of all contestants, teams, ratings, airings, locations, etc. from the past 32 seasons
-	Discover patterns from previous seasons’ winners and use the factors to determine a potential future winner
-	Discover statistical counts of the representation of past contestants to compare to current US population data
-	Visualize the discoveries to make a much more legible representation of the data

## Source of Data

The datasets for my project are newly created because a dataset does not already exist to the public. Nine (9) datasets will be created with each one consisting of a certain breakdown of factors from the show. The largest source of data will be imported from The Amazing Race’s Wikipedia page. Another site that will be used is Fandom.com’s Amazing Race page. This site contains more minutia of data such as age, race and genders which are important factors in my project. The quickfacts dataset will be created from the US Census Bureau’s “Quickfacts” website and will incorporate data from the 2020 US Census. The distance dataset was started by a reddit contributor up to the 29th season and then I added the additional 30th-32nd season’s data. The remaining datasets I created manually in Microsoft Excel using data found from Wikipedia.com, Fandom.com and Reddit.com. 

## Appropriateness of Dataset

The justification for using these datasets is that, currently, no publicly accessible datasets created for The Amazing Race exists. This data contains all the necessary fields, in the correct formats, needed to use Python and Exploratory Data Analysis to present my findings.

## Data Collection Methods
To create most of the datasets used, I imported several pages of html into Python using the Pandas library as a “web scraper”. Pandas then read the html of the webpage into dataframes, using the pandas.read_html function. Using Python, I was able to move through the dataframes to clean and transform the data. I exported the cleaned data to csv files for further cleaning or transformation if necessary. The website Fandom.com would not import successfully into a dataframe using this method. Possibly due to some JavaScript on the website that prevents scraping of data. In this case, I had to manually update csv files with data from the website directly. The remaining datasets were manually created in Microsoft Excel, cleaned, and transformed and then exported to a csv file. Since I was manually importing and updating the csv files, I ensured accuracy along the way. This also allowed me to double-check the data from the websites such as Wikipedia to ensure accuracy and quality.
