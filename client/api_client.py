"""
API Client for DummyJSON API.
This module provides a wrapper around the requests library to make API calls
to https://dummyjson.com in a clean and reusable way.
"""

from ast import keyword

import requests


class DummyJSONClient:
    """Client for interacting with the DummyJSON API."""

    BASE_URL = "https://dummyjson.com"

    def __init__(self):
        # Create a session to reuse the same connection across requests (more efficient)
        self.session = requests.Session()

    # ---------- PRODUCTS ----------

    def get_all_products(self):
        """GET /products - Returns all products."""
        return self.session.get(f"{self.BASE_URL}/products")

    def get_product_by_id(self, product_id):
        """GET /products/{id} - Returns a single product by ID."""
        return self.session.get(f"{self.BASE_URL}/products/{product_id}")

    def search_products(self, keyword):
        """GET /products/search?q={keyword} - Searches products by keyword."""
        return self.session.get(f"{self.BASE_URL}/products/search", params={"q": keyword})

    def get_products_paginated(self, limit=10, skip=0, select=None):
            """GET /products?limit={limit}&skip={skip}&select={select}"""
            params = {"limit": limit, "skip": skip}
            if select:
                params["select"] = select
            return self.session.get(f"{self.BASE_URL}/products", params=params)

    def create_product(self, product_data):
        """POST /products/add - Creates a new product."""
        return self.session.post(f"{self.BASE_URL}/products/add", json=product_data)

    def update_product(self, product_id, product_data):
        """PUT /products/{id} - Updates an existing product."""
        return self.session.put(f"{self.BASE_URL}/products/{product_id}", json=product_data)

    def delete_product(self, product_id):
        """DELETE /products/{id} - Deletes a product."""
        return self.session.delete(f"{self.BASE_URL}/products/{product_id}")

    # ---------- AUTHENTICATION ----------

    def login(self, username, password, expiresInMins=60):
        """POST /auth/login - Authenticates a user."""
        payload = {"username": username, "password": password, "expiresInMins": expiresInMins}
        return self.session.post(f"{self.BASE_URL}/auth/login", json=payload)
    
    # ---------- COMMENTS ----------
    def get_all_comments(self):
        """GET /comments - Returns all comments."""
        return self.session.get(f"{self.BASE_URL}/comments")

    def get_comment_by_id(self, comment_id):
        """GET /comments/{id} - Returns a single comment by ID."""
        return self.session.get(f"{self.BASE_URL}/comments/{comment_id}")

    def get_comments_paginated(self, limit=10, skip=0, select=None):
            """GET /comments?limit={limit}&skip={skip}&select={select}"""
            params = {"limit": limit, "skip": skip}
            if select:
                params["select"] = select
            return self.session.get(f"{self.BASE_URL}/comments", params=params)

    def get_comments_by_post(self, post_id):
        """GET /comments/post/{post_id} - Searches comments by post ID."""
        return self.session.get(f"{self.BASE_URL}/comments/post/{post_id}")

    def create_comment(self, comment_data):
        """POST /comments/add - Creates a new comment."""
        return self.session.post(f"{self.BASE_URL}/comments/add", json=comment_data)

    def update_comment(self, comment_id, comment_data):
        """PUT /comments/{id} - Updates an existing comment."""
        return self.session.put(f"{self.BASE_URL}/comments/{comment_id}", json=comment_data)

    def delete_comment(self, comment_id):
        """DELETE /comments/{id} - Deletes a comment."""
        return self.session.delete(f"{self.BASE_URL}/comments/{comment_id}")
