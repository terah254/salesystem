
from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for
import psycopg2
app = Flask(__name__)


conn=psycopg2.connect(user='msmwbuasjjmkml',
                      password='be1a0fe0b5e067e56e1f33531b1f79df70ccd49d75af012089a9c923f804a7c7',
                      host='ec2-176-34-215-248.eu-west-1.compute.amazonaws.com',
                      port='5432',
                      database='d9o5unanlhobn9')
cur=conn.cursor()



cur.execute("CREATE TABLE IF NOT EXISTS products (id serial PRIMARY KEY, name VARCHAR ( 100 ) NOT NULL,buying_price NUMERIC(14, 2), selling_price NUMERIC(14, 2), stock_quantity INT )")
cur.execute("CREATE TABLE IF NOT EXISTS sales (id serial PRIMARY KEY, pid int, quantity numeric(5,2), created_at DATE NOT NULL DEFAULT NOW())")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    cur.execute("select * from products;")
    products=cur.fetchall()
    print(products)
    return render_template("product.html",products=products)

@app.route("/add_products",methods=["POST","GET"])
def add_products():
    name=request.form["Name"]
    bp=request.form["Buying Price"]
    sp=request.form["Selling Price"]
    sq=request.form["quantity"]
    cur.execute("INSERT INTO products (name,buying_price,selling_price,stock_quantity) VALUES (%s, %s,%s ,%s)",(name,bp,sp,sq))
    conn.commit()
    return redirect("/products")

@app.route("/sales")
def sales():
        cur.execute("select * from sales;")
        sales=cur.fetchall()
        print(sales)
        return render_template("sale.html",sales=sales)


@app.route('/make_sale',methods=["POST","GET"])
def make_sale():
    pid=request.form['pid']
    quantity=request.form['qty']
    created_at=datetime.now()
    
    cur.execute("INSERT INTO sales (pid, quantity, created_at) VALUES (%s, %s, %s)",(pid,quantity,created_at))

    return redirect("/products")

@app.route('/sales/<int:pid>')
def view_sale(pid):
    cur.execute("SELECT * FROM sales WHERE product_id=%s;"[pid])
    sales=cur.fetchall()
    return render_template("sale.html",sales=sales)


@app.route('/charts')
def charts():
    cur=conn.cursor()
    cur.execute("SELECT name,stock_quantity FROM products")
    data=cur.fetchall()
    print(data)

    labels=[products[0]for products in data]
    values=[products[1]for products in data]



    cur=conn.cursor()
    cur.execute("SELECT pid,quantity FROM sales")
    data=cur.fetchall()
    print(data)

    item_sold=[sales[0]for sales in data]
    amount_sold=[sales[1]for sales in data]

    return render_template('/chartjs.html',item_sold=item_sold,amount_sold=amount_sold,labels=labels,values=values)





app.run()