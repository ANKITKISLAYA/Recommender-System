In this project i have created recommender system . Method used is item based collabrative filtering using surprise library 

Implementation :-

1. myapp.py is the main driver file in which i have created the flask api configured with web file for deployment on IIS server.
2. InsertRecSys.py is the programme to calculate the similarity matrix and insert it into mongodb .
3. RecSys.py and RecSys2.py are the programmes to generate top n recommendations from mongodb .


Deploying Flask app on IIS server

https://medium.com/@rajesh.r6r/deploying-a-python-flask-rest-api-on-iis-d8d9ebf886e9