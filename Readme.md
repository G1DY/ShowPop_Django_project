<center><h1>ShoePop Django Project</h1></center>
This was the first portfolio project, a requirement to complete ALX foundation training. I learnt the Django framework and built an ecommerce website to market shoes. The main aim was to test knowledge on backend and frontend coding. I maneged to create the website and host it on the ALX nginx servers

---

<center><h2>Description</h2></center>
ShoePop is a Django web app hosted on the ALX remote server. It is an online shop to sell shoes

<center><h2>Essentials</h2></center>
- Django module to facilitate running and deployment of the project
- Vim, Visual Studio code
- db.sqlite3

### **Program Flow**

- **The Structure and Schema of the Database**

>> The database manages product categories, individual products, customer accounts, shopping carts, cart items, and customer orders. We were able to create and display products, manage customer accounts, handle shopping cart functionality, and process customer using Django Framework

>> The system tracks the number of views for each product, providing insights into product popularity

>> Customers can place orders, specifying delivery addresses and contact information. Orders are associated with specific shopping carts and can have different statuses, such as "Order Received" or "Order Processing."

>> The project includes a shopping cart system that allows customers to add products to their carts as they shop. The cart keeps track of the total cost of items.

>> Customers can create accounts, providing their full names, addresses, and other details. They can log in to their accounts to make the shopping experience more personalized.

>> The project allows you to organize products into different categories, making it easy for customers to browse and find the type of shoes they are looking for.

- **Landing Page***

- ![image](Screenshot%20(20).png)

### **Project Deployment**
We hosted the project on the alx server. We had to modify the gunicorn configuration file and the nginx configuration files

```
t]
Description=Gunicorn daemon for Your Django Project
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/ecomP
ExecStart=/home/ubuntu/ecomP/venv/bin/gunicorn --workers 3 --access-logfile - --bind 0.0.0.0:8000 portf1.wsgi:application

Restart=always

[Install]
WantedBy=multi-user.target

server {
        listen 80 default_server;
        listen [::]:80 default_server;
        add_header X-Served-By gideon-web-02;
        server_name 127.0.0.1 52.3.244.163;
        location / {
                include proxy_params;
                proxy_pass http://127.0.0.1:8000;
        }
	location /airbnb-dynamic/number_odd_or_even/ {
		root /home/ubuntu/ecomP;
```


