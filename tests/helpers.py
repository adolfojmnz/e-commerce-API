from json import dumps

from accounts.models import User
from carts.models import Cart
from categories.models import Category
from inventory.models import InventoryItem
from orders.models import Order
from products.models import Product
from reviews.models import Review

from tests import data


class AccountsTestHelpers:
    user_data = data.user_single
    customer_data = data.customer_single
    vendor_data = data.vendor_single
    admin_data = data.admin_single
    superuser_data = data.superuser_single
    user_list_data = data.user_list

    def create_user(self, user_data=None, is_admin=False, is_superuser=False):
        user_data = user_data or self.user_data
        user = User.objects.create_user(
            **user_data,
            is_staff=is_admin,
            is_superuser=is_superuser,
        )
        return user

    def create_customer(self, customer_data=None):
        customer_data = customer_data or self.customer_data
        return self.create_user(customer_data)

    def create_vendor(self, vendor_data=None, is_admin=True):
        vendor_data = vendor_data or self.vendor_data
        return self.create_user(vendor_data, is_admin)

    def create_admin(self, superuser_data=None):
        superuser_data = superuser_data or self.admin_data
        return self.create_user(superuser_data, is_admin=True)

    def create_superuser(self, superuser_data=None):
        superuser_data = superuser_data or self.superuser_data
        return self.create_user(superuser_data, is_admin=True, is_superuser=True)

    def create_user_list(self, user_list_data=None, is_admin=False,
                                                    is_superuser=False):
        user_list_data = user_list_data or self.user_list_data
        users = User.objects.bulk_create([
            User(**user_data, is_staff=is_admin, is_superuser=is_superuser)
            for user_data in user_list_data
        ])
        return users


class CartTestHelpers:

    def create_cart(self, user):
        cart = Cart.objects.create(user=user)
        return cart

    def create_cart_item(self, cart, product, quantity):
        cart_item = cart.cart_items.create(
            product=product, quantity=quantity
        )
        return cart_item


class CategoriesTestHelpers:
    category_data = data.category_single

    def create_category(self, category_data=None):
        category_data = category_data or self.category_data
        category = Category.objects.create(**category_data)
        return category


class InventoryTestHelpers:

    def create_inventory_item(self, product, quantity):
        inventory = InventoryItem.objects.create(
            product=product, quantity=quantity
        )
        return inventory


class OrdersTestHelpers:
    product_values = dumps(data.product_single)

    def create_order(self, user):
        order = Order.objects.create(user=user)
        return order

    def create_order_item(self, order, product, quantity):
        sub_total = product.price * quantity
        order_item = order.order_items.create(
            product=product,
            quantity=quantity,
            sub_total=sub_total,
            product_values=self.product_values,
        )
        return order_item


class ProductsTestHelpers:
    product_data = data.product_single
    product_list_data = data.product_list

    def create_product(self, vendor, category, product_data=None):
        product_data = product_data or self.product_data
        product = Product.objects.create(
            vendor=vendor, category=category, **product_data
        )
        return product

    def create_product_list(self, vendor, category, product_list_data=None):
        product_list_data = product_list_data or self.product_list_data
        product_list = Product.objects.bulk_create([
            Product(vendor=vendor, category=category, **product_data)
            for product_data in product_list_data
        ])
        return product_list


class ReviewsTestHelpers:
    review_data = data.review_single

    def create_review(self, order, product, user, review_data=None):
        review_data = review_data or self.review_data
        review = Review.objects.create(
            order=order,
            product=product,
            user=user,
            **review_data,
        )
        return review
