"""
Tests for the /products endpoints of DummyJSON API.
"""

import pytest
from client.api_client import DummyJSONClient


# Create a client instance to be used in all tests of this file
client = DummyJSONClient()


# ---------- TEST CASE 1: Get all products ----------

def test_get_all_products():
    """
    Verify that GET /products returns:
    - Status code 200
    - A response with the expected JSON structure
    - A non-empty list of products
    - Each product has the expected fields
    """
    # Step 1: Call the API
    response = client.get_all_products()

    # Step 2: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 3: Parse the JSON response
    data = response.json()

    # Step 4: Check that the response has the expected top-level keys
    assert "products" in data, "Response is missing 'products' key"
    assert "total" in data, "Response is missing 'total' key"
    assert "skip" in data, "Response is missing 'skip' key"
    assert "limit" in data, "Response is missing 'limit' key"

    # Step 5: Check that we got a non-empty list of products
    assert isinstance(data["products"], list), "'products' should be a list"
    assert len(data["products"]) > 0, f"Products list should not be empty, got {len(data['products'])}"

    # Step 6 check pagination data
    assert data["limit"] == len(data["products"]), "The 'limit' value should equal the number of returned products"
    assert data["total"] > 0, f"'total' should be greater than 0, got {data['total']}"

    # Step 7: Check that the first product has ALL expected fields
    first_product = data["products"][0]
    expected_fields = [
        "id", "title", "description", "category", "price",
        "discountPercentage", "rating", "stock", "tags", "brand",
        "sku", "weight", "dimensions", "warrantyInformation",
        "shippingInformation", "availabilityStatus", "reviews",
        "returnPolicy", "minimumOrderQuantity", "meta",
        "thumbnail", "images"
    ]
    for field in expected_fields:
        assert field in first_product, f"Missing field '{field}' in product"

    # Step 8: Check data types of key fields
    assert isinstance(first_product["id"], int), f"'id' should be an integer, got {type(first_product['id'])}"
    assert isinstance(first_product["title"], str), f"'title' should be a string, got {type(first_product['title'])}"
    assert isinstance(first_product["description"], str), f"'description' should be a string, got {type(first_product['description'])}"
    assert isinstance(first_product["category"], str), f"'category' should be a string, got {type(first_product['category'])}"
    assert isinstance(first_product["price"], float), f"'price' should be a float, got {type(first_product['price'])}"
    assert isinstance(first_product["discountPercentage"], float), f"'discountPercentage' should be a float, got {type(first_product['discountPercentage'])}"
    assert isinstance(first_product["rating"], float), f"'rating' should be a float, got {type(first_product['rating'])}"
    assert isinstance(first_product["stock"], int), f"'stock' should be an integer, got {type(first_product['stock'])}"
    assert isinstance(first_product["tags"], list), f"'tags' should be a list, got {type(first_product['tags'])}"
    assert isinstance(first_product["brand"], str), f"'brand' should be a string, got {type(first_product['brand'])}"
    assert isinstance(first_product["sku"], str), f"'sku' should be a string, got {type(first_product['sku'])}"
    assert isinstance(first_product["weight"], int), f"'weight' should be an integer, got {type(first_product['weight'])}"
    assert isinstance(first_product["dimensions"], dict), f"'dimensions' should be a dict, got {type(first_product['dimensions'])}"
    assert isinstance(first_product["warrantyInformation"], str), f"'warrantyInformation' should be a string, got {type(first_product['warrantyInformation'])}"
    assert isinstance(first_product["shippingInformation"], str), f"'shippingInformation' should be a string, got {type(first_product['shippingInformation'])}"
    assert isinstance(first_product["availabilityStatus"], str), f"'availabilityStatus' should be a string, got {type(first_product['availabilityStatus'])}"
    assert isinstance(first_product["reviews"], list), f"'reviews' should be a list, got {type(first_product['reviews'])}"
    assert isinstance(first_product["returnPolicy"], str), f"'returnPolicy' should be a string, got {type(first_product['returnPolicy'])}"
    assert isinstance(first_product["minimumOrderQuantity"], int), f"'minimumOrderQuantity' should be an integer, got {type(first_product['minimumOrderQuantity'])}"
    assert isinstance(first_product["meta"], dict), f"'meta' should be a dict, got {type(first_product['meta'])}"
    assert isinstance(first_product["thumbnail"], str), f"'thumbnail' should be a string, got {type(first_product['thumbnail'])}"
    assert isinstance(first_product["images"], list), f"'images' should be a list, got {type(first_product['images'])}"

    # Step 9: Check nested fields in 'dimensions' (width, height, depth)
    dimensions = first_product["dimensions"]
    for field in ["width", "height", "depth"]:
        assert field in dimensions, f"Missing '{field}' in dimensions"
        assert isinstance(dimensions[field], float), f"'{field}' in dimensions should be a float"

    # Step 10: Check nested fields in 'meta' (createdAt, updatedAt, barcode, qrCode)
    meta = first_product["meta"]
    for field in ["createdAt", "updatedAt", "barcode", "qrCode"]:
        assert field in meta, f"Missing '{field}' in meta"
        assert isinstance(meta[field], str), f"'{field}' in meta should be a string"

    # Step 11: Check structure of reviews (each review has 5 fields)
    if len(first_product["reviews"]) > 0:
        first_review = first_product["reviews"][0]
        expected_review_fields = ["rating", "comment", "date", "reviewerName", "reviewerEmail"]
        for field in expected_review_fields:
            assert field in first_review, f"Missing '{field}' in review"
        assert isinstance(first_review["rating"], int), f"'rating' in review should be an integer, got {type(first_review['rating'])}"
        assert isinstance(first_review["comment"], str), f"'comment' in review should be a string, got {type(first_review['comment'])}"
        assert isinstance(first_review["date"], str), f"'date' in review should be a string, got {type(first_review['date'])}"
        assert isinstance(first_review["reviewerName"], str), f"'reviewerName' in review should be a string, got {type(first_review['reviewerName'])}"
        assert isinstance(first_review["reviewerEmail"], str), f"'reviewerEmail' in review should be a string, got {type(first_review['reviewerEmail'])}"
        assert 0 <= first_review["rating"] <= 5, f"Review rating must be 0-5, got {first_review['rating']}"
        assert "@" in first_review["reviewerEmail"], f"Email must contain '@', got {first_review['reviewerEmail']}"

    # Step 12: Check that tags list contains strings
    for tag in first_product["tags"]:
        assert isinstance(tag, str), f"Each tag should be a string, got {type(tag)}"

    # Step 13: Check that images list contains strings (URLs)
    for image in first_product["images"]:
        assert isinstance(image, str), f"Each image should be a string (URL), got {type(image)}"

    # Step 14: Business logic checks
    assert first_product["price"] > 0, f"Product price should be positive, got {first_product['price']}"
    assert first_product["stock"] >= 0, f"Product stock cannot be negative, got {first_product['stock']}"
    assert 0 <= first_product["rating"] <= 5, f"Rating must be between 0 and 5, got {first_product['rating']}"
    assert 0 <= first_product["discountPercentage"] <= 100, f"Discount percentage must be between 0 and 100, got {first_product['discountPercentage']}"
    assert first_product["weight"] > 0, f"Weight should be positive, got {first_product['weight']}"
    assert first_product["minimumOrderQuantity"] > 0, f"Minimum order quantity should be positive, got {first_product['minimumOrderQuantity']}"
    assert len(first_product["tags"]) > 0, f"Product should have at least one tag, got {len(first_product['tags'])}"
    assert len(first_product["images"]) > 0, f"Product should have at least one image, got {len(first_product['images'])}"

# ---------- TEST CASE 2: Get product by valid ID ----------

def test_get_product_by_valid_id():
    """
    Verify that GET /products/{id} with a valid ID returns:
    - Status code 200
    - A single product object (not a list)
    - The returned product has the requested ID
    - All expected fields are present with correct types
    """
    # Step 1: Define a valid product ID
    valid_id = 1

    # Step 2: Call the API
    response = client.get_product_by_id(valid_id)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    product = response.json()

    # Step 5: Check that the response is a dict (a single product), not a list
    assert isinstance(product, dict), "Response should be a single product object"

    # Step 6: Check that the returned product has the requested ID
    assert product["id"] == valid_id, f"Expected product id {valid_id}, got {product['id']}"

    # Step 7: Check that ALL 22 expected fields are present
    expected_fields = [
        "id", "title", "description", "category", "price",
        "discountPercentage", "rating", "stock", "tags", "brand",
        "sku", "weight", "dimensions", "warrantyInformation",
        "shippingInformation", "availabilityStatus", "reviews",
        "returnPolicy", "minimumOrderQuantity", "meta",
        "thumbnail", "images"
    ]
    for field in expected_fields:
        assert field in product, f"Missing field '{field}' in product"

    # Step 8: Check data types of all product fields
    assert isinstance(product["id"], int), f"'id' should be an integer, got {type(product['id'])}"
    assert isinstance(product["title"], str), f"'title' should be a string, got {type(product['title'])}"
    assert isinstance(product["description"], str), f"'description' should be a string, got {type(product['description'])}"
    assert isinstance(product["category"], str), f"'category' should be a string, got {type(product['category'])}"
    assert isinstance(product["price"], float), f"'price' should be a number, got {type(product['price'])}"
    assert isinstance(product["discountPercentage"], float), f"'discountPercentage' should be a number, got {type(product['discountPercentage'])}"
    assert isinstance(product["rating"], float), f"'rating' should be a number, got {type(product['rating'])}"
    assert isinstance(product["stock"], int), f"'stock' should be an integer, got {type(product['stock'])}"
    assert isinstance(product["tags"], list), f"'tags' should be a list, got {type(product['tags'])}"
    assert isinstance(product["brand"], str), f"'brand' should be a string, got {type(product['brand'])}"
    assert isinstance(product["sku"], str), f"'sku' should be a string, got {type(product['sku'])}"
    assert isinstance(product["weight"], int), f"'weight' should be a number, got {type(product['weight'])}"
    assert isinstance(product["dimensions"], dict), f"'dimensions' should be a dict, got {type(product['dimensions'])}"
    assert isinstance(product["warrantyInformation"], str), f"'warrantyInformation' should be a string, got {type(product['warrantyInformation'])}"
    assert isinstance(product["shippingInformation"], str), f"'shippingInformation' should be a string, got {type(product['shippingInformation'])}"
    assert isinstance(product["availabilityStatus"], str), f"'availabilityStatus' should be a string, got {type(product['availabilityStatus'])}"
    assert isinstance(product["reviews"], list), f"'reviews' should be a list, got {type(product['reviews'])}"
    assert isinstance(product["returnPolicy"], str), f"'returnPolicy' should be a string, got {type(product['returnPolicy'])}"
    assert isinstance(product["minimumOrderQuantity"], int), f"'minimumOrderQuantity' should be an integer, got {type(product['minimumOrderQuantity'])}"
    assert isinstance(product["meta"], dict), f"'meta' should be a dict, got {type(product['meta'])}"
    assert isinstance(product["thumbnail"], str), f"'thumbnail' should be a string, got {type(product['thumbnail'])}"
    assert isinstance(product["images"], list), f"'images' should be a list, got {type(product['images'])}"

    # Step 9: Check nested fields in 'dimensions' (width, height, depth)
    dimensions = product["dimensions"]
    for field in ["width", "height", "depth"]:
        assert field in dimensions, f"Missing '{field}' in dimensions"
        assert isinstance(dimensions[field], float), f"'{field}' should be a float, got {type(dimensions[field])}"

    # Step 10: Check nested fields in 'meta' (createdAt, updatedAt, barcode, qrCode)
    meta = product["meta"]
    for field in ["createdAt", "updatedAt", "barcode", "qrCode"]:
        assert field in meta, f"Missing '{field}' in meta"
        assert isinstance(meta[field], str), f"'{field}' in meta should be a string, got {type(meta[field])}"

# Step 11: Check structure of ALL reviews
    expected_review_fields = ["rating", "comment", "date", "reviewerName", "reviewerEmail"]
    for review in product["reviews"]:
        # Check that all 5 fields exist in the review
        for field in expected_review_fields:
            assert field in review, f"Missing '{field}' in review"
        # Check data types and values of review fields
        assert isinstance(review["rating"], int), f"'rating' in review should be an integer, got {type(review['rating'])}"
        assert isinstance(review["comment"], str), f"'comment' in review should be a string, got {type(review['comment'])}"
        assert isinstance(review["date"], str), f"'date' in review should be a string, got {type(review['date'])}"
        assert isinstance(review["reviewerName"], str), f"'reviewerName' in review should be a string, got {type(review['reviewerName'])}"
        assert isinstance(review["reviewerEmail"], str), f"'reviewerEmail' in review should be a string, got {type(review['reviewerEmail'])}"
        assert 0 <= review["rating"] <= 5, f"Review rating must be 0-5, got {review['rating']}"
        assert "@" in review["reviewerEmail"], f"Email must contain '@', got {review['reviewerEmail']}"

    # Step 12: Check that tags list contains strings
    for tag in product["tags"]:
        assert isinstance(tag, str), f"Each tag should be a string, got {type(tag)}"

    # Step 13: Check that images list contains strings (URLs)
    for image in product["images"]:
        assert isinstance(image, str), f"Each image should be a string (URL), got {type(image)}"

    # Step 14: Business logic checks
    assert product["price"] > 0, f"Product price should be positive, got {product['price']}"
    assert product["stock"] >= 0, f"Product stock cannot be negative, got {product['stock']}"
    assert 0 <= product["rating"] <= 5, f"Rating must be between 0 and 5, got {product['rating']}"
    assert 0 <= product["discountPercentage"] <= 100, f"Discount percentage must be between 0 and 100, got {product['discountPercentage']}"
    assert product["weight"] > 0, f"Weight should be positive, got {product['weight']}"
    assert product["minimumOrderQuantity"] > 0, f"Minimum order quantity should be positive, got {product['minimumOrderQuantity']}"
    assert len(product["title"]) > 0, f"Title should not be empty, got {len(product['title'])}"
    assert len(product["tags"]) > 0, f"Product should have at least one tag, got {len(product['tags'])}"
    assert len(product["images"]) > 0, f"Product should have at least one image, got {len(product['images'])}"

# ---------- TEST CASE 3: Get product by invalid ID ----------

def test_get_product_by_invalid_id():
    """
    Verify that GET /products/{id} with an invalid ID returns:
    - Status code 404 (Not Found)
    - An error message in the response
    """
    # Step 1: Define an invalid product ID (one that doesn't exist)
    invalid_id = 200 # total products are 194

    # Step 2: Call the API
    response = client.get_product_by_id(invalid_id)

    # Step 3: Check the status code is 404 (Not Found)
    assert response.status_code == 404, f"Expected 404 for invalid ID, got {response.status_code}"

    # Step 4: Parse the JSON response
    data = response.json()

    # Print the full error response for visibility
    print(f"\nError response: {data}")

    # Step 5: Check that the response contains an error message
    assert "message" in data, "Error response should contain a 'message' field"

    # Step 6: Check that the message is a non-empty string
    assert isinstance(data["message"], str), f"'message' should be a string, got {type(data['message'])}"
    assert len(data["message"]) > 0, f"'message' should not be empty, got {len(data['message'])}"

    # Step 7: Check that the message mentions the invalid ID
    assert str(invalid_id) in data["message"], f"Error message should mention the invalid ID '{invalid_id}', got {data['message']}"

# ---------- TEST CASE 4: Search products by keyword ----------

def test_search_products_by_keyword():
    """
    Verify that GET /products/search?q={keyword} returns:
    - Status code 200
    - The expected JSON structure (products, total, skip, limit)
    - All returned products are relevant to the keyword
    """
    # Step 1: Define a keyword to search for
    keyword = "phone"

    # Step 2: Call the API
    response = client.search_products(keyword)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    data = response.json()

    # Print the search result for visibility
    print(f"\nSearch for '{keyword}' returned {data['total']} results")

    # Step 5: Check all top-level keys exist
    expected_top_level_keys = ["products", "total", "skip", "limit"]
    for key in expected_top_level_keys:
        assert key in data, f"Response is missing top-level key '{key}'"

    # Step 6: Check types of top-level values
    assert isinstance(data["products"], list),f"'products' should be a list, got {type(data['products'])}"
    assert isinstance(data["total"], int), f"'total' should be an integer, got {type(data['total'])}"
    assert isinstance(data["skip"], int), f"'skip' should be an integer, got {type(data['skip'])}"
    assert isinstance(data["limit"], int), f"'limit' should be an integer, got {type(data['limit'])}"

    # Step 7: Check that we got results (the keyword exists in the data)
    assert data["total"] > 0, f"Expected at least 1 result for '{keyword}'"
    assert len(data["products"]) > 0, "Products list should not be empty"

    # Step 8: Check pagination metadata is consistent
    assert data["limit"] == len(data["products"]), f"'limit' should equal the number of returned products, got {data['limit']} vs {len(data['products'])}"
    assert data["skip"] >= 0, f"'skip' should not be negative, got {data['skip']}"

    # Step 9: Check that ALL returned products are relevant to the keyword
    # (the keyword should appear in title, description, category, brand, or tags)
    for product in data["products"]:
        # Build a single searchable string from all relevant fields
        searchable_text = " ".join([
            product.get("title", ""),
            product.get("description", ""),
            product.get("category", ""),
            product.get("brand", ""),
            " ".join(product.get("tags", []))
        ]).lower()

        assert keyword.lower() in searchable_text, f"Product {product['id']} ('{product['title']}') does not contain keyword '{keyword}'" # search in searchable_text, string if keyword is in it, both lowercase

# ---------- TEST CASE 5: Test pagination ----------

def test_pagination():
    """
    pagination: feature όπου αντι να επιστρέφει το API όλα μαζί τα προιόντα, τα χωρίζει σε σελίδες (pages) με συγκεκριμένο αριθμό προιόντων ανά σελίδα (limit) και δυνατότητα να παραλείψει κάποια προιόντα (skip).
    Verify that GET /products with pagination parameters returns:
    - Status code 200
    - Exactly the requested number of products (limit)
    - The correct skip value
    - Different products on different pages
    """
    # Step 1: Define pagination parameters for page 1
    limit = 5
    skip = 0

    # Step 2: Call the API for the first page
    response_page1 = client.get_products_paginated(limit=limit, skip=skip)

    # Step 3: Check the status code
    assert response_page1.status_code == 200, f"Expected 200, got {response_page1.status_code}"

    # Step 4: Parse the JSON response
    data_page1 = response_page1.json()

    print(f"\nPage 1: limit={data_page1['limit']}, skip={data_page1['skip']}, total={data_page1['total']}")

    # Step 5: Check all top-level keys exist
    expected_top_level_keys = ["products", "total", "skip", "limit"]
    for key in expected_top_level_keys:
        assert key in data_page1, f"Response is missing top-level key '{key}'"

    # Step 6: Check that the API respected our pagination parameters
    assert data_page1["limit"] == limit, f"Expected limit={limit}, got {data_page1['limit']}"
    assert data_page1["skip"] == skip, f"Expected skip={skip}, got {data_page1['skip']}"

    # Step 7: Check that we got exactly 'limit' products
    assert len(data_page1["products"]) == limit, f"Expected {limit} products, got {len(data_page1['products'])}"

    # Step 8: Call the API for the second page
    skip_page2 = limit  # Skip the first page
    response_page2 = client.get_products_paginated(limit=limit, skip=skip_page2)

    assert response_page2.status_code == 200, f"Expected 200 for page 2, got {response_page2.status_code}"
    data_page2 = response_page2.json()

    print(f"Page 2: limit={data_page2['limit']}, skip={data_page2['skip']}, total={data_page2['total']}")

    # Step 9: Check pagination metadata of page 2
    assert data_page2["limit"] == limit, f"Expected limit={limit}, got {data_page2['limit']}"
    assert data_page2["skip"] == skip_page2, f"Expected skip={skip_page2}, got {data_page2['skip']}"
    assert len(data_page2["products"]) == limit, f"Expected {limit} products, got {len(data_page2['products'])}"

    # Step 10: Check that page 1 and page 2 contain DIFFERENT products
    # Create a list of product IDs from each page and check for overlap
    page1_ids = []
    for product in data_page1["products"]:
        page1_ids.append(product["id"])
    page2_ids = []
    for product in data_page2["products"]:
        page2_ids.append(product["id"])

    print(f"Page 1 IDs: {page1_ids}")
    print(f"Page 2 IDs: {page2_ids}")

    # No common IDs between the two pages
    # set(...) → μετατρέπει τη λίστα σε set (συλλογή χωρίς διπλοεγγραφές)
    # & → υπολογίζει την τομή (intersection) των δύο sets, δηλαδή τα κοινά στοιχεία
    # Παράδειγμα: 
    #  set([1, 2, 3, 4, 5]) & set([6, 7, 8, 9, 10])
    #  → set()  (κανένα κοινό → άδειο)
    #  set([1, 2, 3]) & set([3, 4, 5])
    #  → {3}  (κοινό το 3)
    common_ids = set(page1_ids) & set(page2_ids)
    assert len(common_ids) == 0, f"Page 1 and Page 2 should not have common products, but found: {common_ids}"

    # Step 11: Check that total is consistent across pages
    assert data_page1["total"] == data_page2["total"], f"'total'= {data_page1['total']} should be the same on both pages"

# ---------- TEST CASE 5: Test pagination_select ----------

def test_pagination_select():
    """
    Verify that GET /products with pagination + field selection returns:
    - Status code 200
    - Exactly the requested number of products (limit)
    - The correct skip value
    - ONLY the selected fields (plus 'id') are returned
    - Different products on different pages
    """
    # Step 1: Define pagination + select parameters for page 1
    limit = 10
    skip = 10
    select = "title,price"

    # Step 2: Call the API for the first page
    response_page1 = client.get_products_paginated(limit=limit, skip=skip, select=select)

    # Step 3: Check the status code
    assert response_page1.status_code == 200, f"Expected 200, got {response_page1.status_code}"

    # Step 4: Parse the JSON response
    data_page1 = response_page1.json()

    print(f"\nPage 1: limit={data_page1['limit']}, skip={data_page1['skip']}, total={data_page1['total']}")

    # Step 5: Check all top-level keys exist
    expected_top_level_keys = ["products", "total", "skip", "limit"]
    for key in expected_top_level_keys:
        assert key in data_page1, f"Response is missing top-level key '{key}'"

    # Step 6: Check that the API respected our pagination parameters
    assert data_page1["limit"] == limit, f"Expected limit={limit}, got {data_page1['limit']}"
    assert data_page1["skip"] == skip, f"Expected skip={skip}, got {data_page1['skip']}"

    # Step 7: Check that we got exactly 'limit' products
    assert len(data_page1["products"]) == limit, f"Expected {limit} products, got {len(data_page1['products'])}"

    # Step 8: Check that ONLY the selected fields (+ id) are returned
    expected_product_fields = {"id", "title", "price"}
    for product in data_page1["products"]:
        actual_fields = set(product.keys()) #η set: Στην Python τα sets γράφονται με άγκιστρα {...} (όπως τα dicts), αλλά χωρίς keys:values — μόνο τιμές.
        assert actual_fields == expected_product_fields, f"Expected fields {expected_product_fields}, got {actual_fields}"

    # Step 9: Check types of selected fields
    for product in data_page1["products"]:
        assert isinstance(product["id"], int), f"'id' should be an integer, got {type(product['id'])}"
        assert isinstance(product["title"], str), f"'title' should be a string, got {type(product['title'])}"
        assert isinstance(product["price"], float), f"'price' should be a number, got {type(product['price'])}"

    # Step 10: Check that the first product has id=11 (since we skipped 10)
    assert data_page1["products"][0]["id"] == skip + 1, f"First product should have id={skip + 1} (skipped {skip})"

    # Step 11: Call the API for the second page
    skip_page2 = skip + limit  # skip=20 (skip the first 20)
    response_page2 = client.get_products_paginated(limit=limit, skip=skip_page2, select=select)

    assert response_page2.status_code == 200, f"Expected 200 for page 2, got {response_page2.status_code}"
    data_page2 = response_page2.json()

    print(f"Page 2: limit={data_page2['limit']}, skip={data_page2['skip']}, total={data_page2['total']}")

    # Step 12: Check pagination metadata of page 2
    assert data_page2["limit"] == limit, f"Expected limit={limit}, got {data_page2['limit']}"
    assert data_page2["skip"] == skip_page2, f"Expected skip={skip_page2}, got {data_page2['skip']}"
    assert len(data_page2["products"]) == limit, f"Expected {limit} products, got {len(data_page2['products'])}"

    # Step 13: Check that page 1 and page 2 contain DIFFERENT products
    # Create a list of product IDs from each page and check for overlap
    page1_ids = []
    for product in data_page1["products"]:
        page1_ids.append(product["id"])
    page2_ids = []
    for product in data_page2["products"]:
        page2_ids.append(product["id"])

    print(f"Page 1 IDs: {page1_ids}")
    print(f"Page 2 IDs: {page2_ids}")

    common_ids = set(page1_ids) & set(page2_ids)
    assert len(common_ids) == 0, \
        f"Page 1 and Page 2 should not have common products, but found: {common_ids}"

    # Step 14: Check that total is consistent across pages
    assert data_page1["total"] == data_page2["total"], "'total' should be the same on both pages"

# ---------- TEST CASE 6: Create a new product ----------

def test_create_product():
    """
    Verify that POST /products/add creates a new product:
    - Status code 201 (Created)
    - Response contains the new product with an auto-generated ID
    - All fields we sent are returned correctly
    """
    # Step 1: Define the new product data
    new_product = {
        "title": "BMW Pencil",
        "description": "A product created for testing purposes",
        "price": 49.99,
        "discountPercentage": 10.5,
        "rating": 4.5,
        "stock": 100,
        "brand": "TestBrand",
        "category": "smartphones",
        "thumbnail": "https://example.com/thumbnail.jpg",
        "images": ["https://example.com/image1.jpg"]
    }

    # Step 2: Call the API to create the product
    response = client.create_product(new_product)

    # Step 3: Check the status code (201 = Created)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Step 4: Parse the JSON response
    created_product = response.json()

    print(f"\nCreated product: {created_product}")

    # Step 5: Check that the response is a dictionary (single product)
    assert isinstance(created_product, dict), "Response should be a single product object"

    # Step 6: Check that an ID was auto-generated
    assert "id" in created_product, "Created product should have an 'id'"
    assert isinstance(created_product["id"], int), "'id' should be an integer"
    assert created_product["id"] > 0, "'id' should be positive"

    # Step 7: Check that the fields we sent are returned correctly
    assert created_product["title"] == new_product["title"]
    assert created_product["description"] == new_product["description"]
    assert created_product["price"] == new_product["price"]
    assert created_product["discountPercentage"] == new_product["discountPercentage"]
    assert created_product["rating"] == new_product["rating"]
    assert created_product["stock"] == new_product["stock"]
    assert created_product["brand"] == new_product["brand"]
    assert created_product["category"] == new_product["category"]
    assert created_product["thumbnail"] == new_product["thumbnail"]
    assert created_product["images"] == new_product["images"]

    # Step 8: Check types of returned fields
    assert isinstance(created_product["title"], str),f"'title' should be a string, got {type(created_product['title'])}"
    assert isinstance(created_product["price"], float), f"'price' should be a number, got {type(created_product['price'])}"
    assert isinstance(created_product["stock"], int), f"'stock' should be an integer, got {type(created_product['stock'])}"
    assert isinstance(created_product["images"], list), f"'images' should be a list, got {type(created_product['images'])}"

# ---------- TEST CASE 7: Update an existing product ----------

def test_update_product():
    """
    Verify that PUT /products/{id} updates an existing product:
    - Status code 200
    - The product ID remains the same
    - The fields we sent are updated
    - Other fields remain unchanged
    """
    # Step 1: Define the product ID to update and the new data
    product_id = 1
    updated_data = {
        "title": "iPhone Galaxy +1",
        "price": 199.99,
    }

    # Step 2: Call the API to update the product
    response = client.update_product(product_id, updated_data)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    updated_product = response.json()

    print(f"\nUpdated product: {updated_product}")

    # Step 5: Check that the response is a dictionary
    assert isinstance(updated_product, dict), "Response should be a single product object"

    # Step 6: Check that the ID is the same as the one we requested
    assert updated_product["id"] == product_id, f"Expected id {product_id}, got {updated_product['id']}"

    # Step 7: Check that the fields we sent were actually updated
    assert updated_product["title"] == updated_data["title"], f"Title was not updated. Expected '{updated_data['title']}', got '{updated_product['title']}'"
    assert updated_product["price"] == updated_data["price"], f"Price was not updated. Expected {updated_data['price']}, got {updated_product['price']}"

    # Step 8: Check that other fields are still present (not deleted)
    assert "description" in updated_product, "Other fields should remain after partial update"
    assert "category" in updated_product, "Other fields should remain after partial update"
    assert "stock" in updated_product, "Other fields should remain after partial update"
    assert "brand" in updated_product, "Other fields should remain after partial update"
    assert "thumbnail" in updated_product, "Other fields should remain after partial update"
    assert "images" in updated_product, "Other fields should remain after partial update"
    assert "discountPercentage" in updated_product, "Other fields should remain after partial update"
    assert "rating" in updated_product, "Other fields should remain after partial update"

    # Step 9: Check types of updated fields
    assert isinstance(updated_product["title"], str), f"'title' should be a string, got {type(updated_product['title'])}"
    assert isinstance(updated_product["price"], float), f"'price' should be a number, got {type(updated_product['price'])}"

# ---------- TEST CASE 8: Delete a product ----------

def test_delete_product():
    """
    Verify that DELETE /products/{id} deletes a product:
    - Status code 200
    - The response contains the deleted product
    - The 'isDeleted' field is True
    - The 'deletedOn' field is a valid timestamp
    """
    # Step 1: Define the product ID to delete
    product_id = 1

    # Step 2: Call the API to delete the product
    response = client.delete_product(product_id)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    deleted_product = response.json()

    print(f"\nDeleted product: id={deleted_product['id']}, "
          f"isDeleted={deleted_product['isDeleted']}, "
          f"deletedOn={deleted_product['deletedOn']}")

    # Step 5: Check that the response is a dictionary
    assert isinstance(deleted_product, dict), "Response should be a single product object"

    # Step 6: Check that the ID is the same as the one we requested
    assert deleted_product["id"] == product_id, f"Expected id {product_id}, got {deleted_product['id']}"

    # Step 7: Check that the deletion-specific fields exist
    assert "isDeleted" in deleted_product, "Response should contain 'isDeleted' field"
    assert "deletedOn" in deleted_product, "Response should contain 'deletedOn' field"

    # Step 8: Check that 'isDeleted' is True
    assert deleted_product["isDeleted"] is True, f"'isDeleted' should be True, got {deleted_product['isDeleted']}"

    # Step 9: Check types of deletion fields
    assert isinstance(deleted_product["isDeleted"], bool), f"'isDeleted' should be a boolean, got {type(deleted_product['isDeleted'])}"
    assert isinstance(deleted_product["deletedOn"], str), f"'deletedOn' should be a string (timestamp), got {type(deleted_product['deletedOn'])}"

    # Step 10: Check that 'deletedOn' is not empty
    assert len(deleted_product["deletedOn"]) > 0, "'deletedOn' should not be empty"

    # Step 11: Check that the original product fields are still present
    assert "title" in deleted_product
    assert "price" in deleted_product
    assert "category" in deleted_product

# ---------- TEST CASE 9: Login with valid credentials ----------

def test_login_with_valid_credentials():
    """
    Verify that POST /auth/login with valid credentials returns:
    - Status code 200
    - An accessToken and refreshToken (JWT)
    - The correct user data (id, username, email, etc.)
    """
    # Step 1: Define valid credentials
    username = "emilys"
    password = "emilyspass"
    expiresInMins = 30

    # Step 2: Call the API
    response = client.login(username, password, expiresInMins)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    data = response.json()

    print(f"\nLogin response for '{username}': {data}")

    # Step 5: Check that the response is a dictionary
    assert isinstance(data, dict), "Response should be a dictionary"

    # Step 6: Check that all expected fields are present
    expected_fields = ["id", "username", "email", "firstName", "lastName",
        "gender", "image", "accessToken", "refreshToken"]
    for field in expected_fields:
        assert field in data, f"Response is missing field '{field}'"

    # Step 7: Check that the username matches the one we sent
    assert data["username"] == username, f"Expected username '{username}', got '{data['username']}'"

    # Step 8: Check types of all fields
    assert isinstance(data["id"], int), f"'id' should be an integer, got {type(data['id'])}"
    assert isinstance(data["username"], str), f"'username' should be a string, got {type(data['username'])}"
    assert isinstance(data["email"], str), f"'email' should be a string, got {type(data['email'])}"
    assert isinstance(data["firstName"], str), f"'firstName' should be a string, got {type(data['firstName'])}"
    assert isinstance(data["lastName"], str), f"'lastName' should be a string, got {type(data['lastName'])}"
    assert isinstance(data["gender"], str), f"'gender' should be a string, got {type(data['gender'])}"
    assert isinstance(data["image"], str), f"'image' should be a string, got {type(data['image'])}"
    assert isinstance(data["accessToken"], str), f"'accessToken' should be a string, got {type(data['accessToken'])}"
    assert isinstance(data["refreshToken"], str), f"'refreshToken' should be a string, got {type(data['refreshToken'])}"

    # Step 9: Check that tokens are not empty
    assert len(data["accessToken"]) > 0, "accessToken should not be empty"
    assert len(data["refreshToken"]) > 0, "refreshToken should not be empty"

    # # Step 10: Check that tokens look like JWTs (3 parts separated by dots)
    # assert data["accessToken"].count(".") == 2, \
    #     "accessToken should be a JWT (3 parts separated by '.')"
    # assert data["refreshToken"].count(".") == 2, \
    #     "refreshToken should be a JWT (3 parts separated by '.')"

    # Step 11: Check business logic on user data
    assert data["id"] > 0, f"User id should be positive, got {data['id']}"
    assert "@" in data["email"], f"Email should contain '@', got {data['email']}"
    assert len(data["firstName"]) > 0, f"firstName should not be empty, got {data['firstName']}"
    assert len(data["lastName"]) > 0, f"lastName should not be empty, got {data['lastName']}"

# ---------- TEST CASE 10: Login with invalid credentials ----------

def test_login_with_invalid_credentials():
    """
    Verify that POST /auth/login with invalid credentials returns:
    - Status code 400 (Bad Request)
    - An error message in the response
    - NO accessToken or refreshToken (no successful login)
    """
    # Test scenario 1: Wrong username, wrong password
    invalid_credentials = {
        "username": "wronguser",
        "password": "wrongpass"
    }

    # Step 1: Call the API
    response = client.login(
        invalid_credentials["username"],
        invalid_credentials["password"]
    )

    # Step 2: Check that the status code is 400 (Bad Request)
    assert response.status_code == 400, f"Expected 400 for invalid credentials, got {response.status_code}"

    # Step 3: Parse the JSON response
    data = response.json()

    print(f"\nLogin response for invalid credentials: {data}")

    # Step 4: Check that the response contains an error message
    assert "message" in data, "Error response should contain a 'message' field"

    # Step 5: Check that the message is a non-empty string
    assert isinstance(data["message"], str), "'message' should be a string"
    assert len(data["message"]) > 0, "'message' should not be empty"

    # Step 6: Check that NO authentication tokens were returned
    assert "accessToken" not in data, "Failed login should NOT return an accessToken"
    assert "refreshToken" not in data, "Failed login should NOT return a refreshToken"

    # Step 7: Check that NO user data was returned
    assert "id" not in data, "Failed login should NOT return user id"
    assert "email" not in data, "Failed login should NOT return user email"
    assert "firstName" not in data, "Failed login should NOT return firstName"

# ---------- TEST CASE 10: Login with invalid credentials ----------
# test_login_with_invalid_credentials[wronguser-wrongpass-Both wrong] PASSED
# test_login_with_invalid_credentials[emilys-wrongpass-Wrong password only] PASSED
# test_login_with_invalid_credentials[wronguser-emilyspass-Wrong username only] PASSED
# test_login_with_invalid_credentials[--Empty credentials] PASSED

@pytest.mark.parametrize("username,password,scenario", [
    ("wronguser", "wrongpass", "Both wrong"),
    ("emilys", "wrongpass", "Wrong password only"),
    ("wronguser", "emilyspass", "Wrong username only"),
    ("", "", "Empty credentials"),
])
def test_login_with_invalid_credentials_parametrized(username, password, scenario):
    """
    Verify that POST /auth/login with invalid credentials returns:
    - Status code 400 (Bad Request)
    - An error message in the response
    - NO accessToken or refreshToken
    """
    print(f"\nScenario: {scenario}")

    # Step 1: Call the API
    response = client.login(username, password)

    # Step 2: Check that the status code is 400
    assert response.status_code == 400, f"Expected 400 for '{scenario}', got {response.status_code}"

    # Step 3: Parse the JSON response
    data = response.json()

    print(f"Response: {data}")

    # Step 4: Check that the response contains an error message
    assert "message" in data, "Error response should contain a 'message' field"
    assert isinstance(data["message"], str), "'message' should be a string"
    assert len(data["message"]) > 0, "'message' should not be empty"

    # Step 5: Check that NO authentication tokens were returned
    assert "accessToken" not in data, "Failed login should NOT return an accessToken"
    assert "refreshToken" not in data, "Failed login should NOT return a refreshToken"

    # Step 6: Check that NO user data was returned
    assert "id" not in data, "Failed login should NOT return user id"
    assert "email" not in data, "Failed login should NOT return user email"
    assert "firstName" not in data, "Failed login should NOT return firstName"