## FastAPI-and-Scikit-Learn-for-Machine-Learning-Deployment
Machine Learning models when built are not meant to sit inside a Notebook in isolation.
They are built so that they can be applied in the real world by instantaneously
making predictions. In this project, I not only build machine learning models, but I go a step further to deploy them as an API with [FastAPI](https://fastapi.tiangolo.com/lo/) so 
that it can be integrated into existing sytems or services by an  endpoint. The endpoint receives requests in real time
and generates responses. 

This project also features user management with role-based access for different levels of users using [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)

**Set up**

To run the service ensure you have [Python](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) installed

Run 

`git clone https://github.com/mutwiriian/FastAPI-and-Scikit-Learn-for-Machine-Learning-Deployment.git`

Then 

`cd temp_fastapi`

Go to [Poetry](https://python-poetry.org/docs/) for installation instructions on the Poetry package manager


Activate the environment by running 

`poetry shell`


To install all the packages and other dependencies required to run the service run: 

`poetry install`


To run the app open the terminal and run the `main.py` file

This will enable you access the service in any browser as demonstrated below

![Alt text](assets/Screenshot%20(14).png)

and execute your requests
![Alt text](assets/Screenshot%20(15).png)
