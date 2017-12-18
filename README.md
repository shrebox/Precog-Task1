# PreCog-Task

  <h2>1. Data extraction using the data.py script:</h2>
  Using the Twitter API with Tweepy wrapper, data has been extracted for particular hashtags. I have  collected 10001 tweets for Mumbai Rains and 12400 for Delhi/NCR Pollution-exported as json file in Data directory from mongodb. 
  
  To use the data script, in terminal run the following command:
 <b> $ python data.py</b>
  * You have put Twitter API keys for extraction.

  <h2>2. Partwise Data Explaination(according to the hosted webapp):</h2>
  1. Network Graph is made using the networkx tool in pyhton and later visualized using matplotlib. Replies, retweets and mentions are considered while building graphs. <br>
  2. Geoplotting for the location of tweets based on geo-coordinates, user-timezone and user-location has been visualized using CartDB with frequency of tweets occuring from a particular location. <br>
  3. Pie chart using Google charts to distinguish the percent of tweets the non-Delhi and non-Mumbai people did about the Delhi and Mumbai incidents. <br>
  4. Donut Chart using Google charts to show the range of entities used in tweets like text, image, video and GIFs and their ratio in overall tweets. <br>
  5. Pie chart using Google charts to show the ratio of original tweets vs the retweeted tweets. <br>
  6. Top 10 hashtags used for both Delhi and Mumbai data visualized using Google Charts. <br>
  7. CDF for the favourite count on the original tweets visualized using matplotlib. Point on the graph defines the probability of tweets on the y-axis will have at-most favourite count defined on x-axis. 

  <h2>3. Webapp for the data analysis:</h2>
  Data analysis script: "my2.py" is stored in the Codes directory which is further analysed using Google charts.
  Webapp is hosted on: <b>https://precog-task1-shrebox.herokuapp.com/ </b> OR <b> http://ec2-54-197-12-15.compute-1.amazonaws.com/precog/ </b>

