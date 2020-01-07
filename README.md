# Video Rental Store

## Author: Peng Kuang
## Email: kap.kuang@gmail.com

Video Rental Store (VRS) is a system for VRS owners to manage their film inventory and rental and return records from their customers.
VRS includes four main futures: film catalogue, customer list, film rental and film return.

## Usage
To use the system for the first time, you will need to follow the steps below:
1. add some films
2. create a customer
3. rent a film
4. return the film

## Setup
Change to the directory where the project is located

```bash
cd dir-to-the-project
```

Create a virtual environment

```bash
python -m venv env
```

Install all the dependencies

```bash
pip3 install -r requirements.txt
```

Activate the environment

```bash
source env/bin/activate
```

Run the application

```bash
python3 app.py
```

If it runs successfully, a link for access the app on your localhost should appear as below:
http://127.0.0.1:5000/

## Test
Please use the browser CHROME on desktop/laptop for testing the application. There are a few known issues on Safari, including date picker will not function, navbar responsiveness, etc. 

Using localhost for testing is also recommended. There are some latency issues for displaying updated data instantly and correctly on Heroku.

## Deployment
The app is also deployed to Heroku:
https://flaskcrudapp2020.herokuapp.com/ 

There are some known issues with the production version on Heroku. For example, the film catalogue will not display completely and correctly after adding a new film. This issue cannot be replicated on localhost. It mainly due to the environment itself, such as its network speed and database communication.

The author only did minimum deployment work for the production version. So bugs akin to the live environment are not addressed due to shortage of time and lack of knowledge of the environment. 

If you prefer to test the application on Heroku, please keep refreshing the page until you get the correct data displayed when encounting any data incomplete or incorrect issues.

## Message from the Developer

This web application is developed using Python Flask framework, SQLAlchemy, WTForms and Bootstrap. I used Flask for the whole structure, SQLAlchemy for database, WTForms for form input and validation, and Bootstrap for UI. There are a few other flask extensions utilised.

### Why Flask?
I chose Flask because it is a thin web application framework. It is easy to grab for new programmers or those who are not very experienced with Python, especially with time constrains. It also has many well-written extensions. The drawback is that it lacks very detailed documentations, especially for some of its extensions. Many documentations are not updated anymore and/or relatively brief. Hence, it takes time to fix bugs or figure out solutions.

On the other hand, Django is widely used and with abundant resources available on the internet. However, it may be challenging for less experienced programmers to grab within a short timeframe. It usually suits complex systems or large projects better.

### Relational Database (SQLAlchemy) vs. NoSQL (PyMongo)
There are not many entities involved in the business process of a video rental store. The relationships among them are simple and easy to map. Wtih SQLAlchemy, handling data is not difficult when using Flask. 

NoSQL databases such as MongonDB gained popularity because of the prevalence of social media and e-commerce. It is naturally more suitable to those complex or less structured scenarios. Also, it takes time to read its API documentation. However, it is easy to operate on data.

### Fuctionality and UI/UX Design
I first focused on delivering a functional web application. In the meantime, I also want to write clean and quality code as well as produce a presentable user interface.

In terms of functionality, I took into account both the specification and the user experience. I split some functionalities into parts/modules to allow more flexbility and scalability. This is why both rental and return are implemented as individual rather than as batch. In practice, such design could be useful in some cases, for example, customer wants to rent several films for different days, or he/she lost one or two films when return them. However, batch processing is efficient and makes better sense for placing an order and calculating the total price. If I have more time, I would like to implement it. 

For the user interface, I used four different colours to represent tasks related to the four features. I assume such design provides good visual hints to the user. User can easily get a sense about what kind of task he/she is performing. Meanwhile, I don't want it to be too colourful to distract the user from accomplishing his/her task or cause unnecessary visual burden. Hence, I used them in a relatively constrained way and only on places where I deem variations are necessary. I added extra attributes in each table for the information to be easier to comprehend. Some of them are interlinked as well. For instance, film's availability, rental's status and return's tick box. In addition, I also designed some message prompts for better communication with the user in those scenarios where additional transactions are subsequently processed. 

### Future Improvements
Lastly, I added a few small features that are easy to realise and left several features unfinished there, for example, filtering, sorting and searching. I think they would be useful but couldn't complete them due to shortage of time.