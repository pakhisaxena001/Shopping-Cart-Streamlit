import streamlit as st
import mysql.connector



def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="shopping_app"
    )


def get_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return products


if "cart" not in st.session_state:
    st.session_state.cart = []



st.title("Shopping Cart")

st.divider()


# ADD PRODUCT

st.header("ADD PRODUCT")

products = get_products()

# Create dictionary for easy lookup
product_dict = {
    product["product_name"]: product
    for product in products
}


selected_product = st.selectbox(
    "Select Product",
    ["Select a product"] + list(product_dict.keys())
)


# Show selected product
if selected_product != "Select a product":

    product = product_dict[selected_product]

    st.write(f"**Product:** {product['product_name']}")
    st.write(f"**Price:** ₹{product['price']:.2f}")

    if st.button("Add to Cart"):

        st.session_state.cart.append({
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "price": float(product["price"])
        })

        st.success(f"{product['product_name']} added to cart!")


st.divider()


# ==========================================================
# MY CART

st.header("MY CART")


if len(st.session_state.cart) == 0:

    st.info("Your cart is empty.")

else:

    total = 0

    for item in st.session_state.cart:

        st.write(
            f"**{item['product_name']}** — ₹{item['price']:.2f}"
        )

        total += item["price"]

    st.divider()

    st.subheader(f"Total Bill: ₹{total:.2f}")

    if st.button("Clear Cart"):

        st.session_state.cart = []

        st.success("Cart cleared!")

        st.rerun()