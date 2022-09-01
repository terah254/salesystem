
from datetime import datetime
from flask import Flask,render_template,request,redirect,url_for
import psycopg2
app = Flask(__name__)

conn=psycopg2.connect(user="postgres",password="terah001A",host="localhost",port="5432",database="myduka")
cur=conn.cursor()
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

@app.route("/sales",methods=["POST","GET"])
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