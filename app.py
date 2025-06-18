from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Sample product catalog
products = {
    1: {"name": "Laptop", "price": 899.99},
    2: {"name": "Headphones", "price": 129.99},
    3: {"name": "Smartphone", "price": 699.99}
}

@app.route('/')
def index():
    return render_template("index.html", products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    item = products.get(product_id)
    return render_template("product.html", product=item, product_id=product_id)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if product_id not in products:
        return "Product does not exist", 404
    cart = session.get('cart', {})
    
    # ✅ Convert key to string
    product_key = str(product_id)
    cart[product_key] = cart.get(product_key, 0) + 1

    session['cart'] = cart
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = products.get(product_id)
        if product:
            subtotal = product["price"] * quantity
            total += subtotal
            items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
    return render_template("cart.html", items=items, total=total)
from flask import request, flash

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = products.get(product_id)
        if product:
            subtotal = product["price"] * quantity
            total += subtotal
            items.append({"product": product, "quantity": quantity, "subtotal": subtotal})

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']

        # (Optional: Save order to DB here in future)

        flash(f"Thank you, {name}! Your order has been placed.")
        session['cart'] = {}  # Clear the cart
        return redirect(url_for('index'))

    return render_template("checkout.html", items=items, total=total)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
