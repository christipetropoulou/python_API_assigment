"""
Tests for the /comments endpoints of DummyJSON API.
"""

import pytest
from client.api_client import DummyJSONClient


# Create a client instance to be used in all tests of this file
client = DummyJSONClient()

# ---------- TEST CASE: Get all comments ----------

def test_get_all_comments():
    """
    Verify that GET /comments returns:
    - Status code 200
    - The expected JSON structure with all fields
    - A non-empty list of comments with valid data
    """
    # Step 1: Call the API
    response = client.get_all_comments()

    # Step 2: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 3: Parse the JSON response
    data = response.json()

    # Print the full response for visibility
    print(f"\n Response: {data}")

    # Step 4: Check all top-level keys
    expected_top_level_keys = ["comments", "total", "skip", "limit"]
    for key in expected_top_level_keys:
        assert key in data, f"Response is missing top-level key '{key}'"

    # Step 5: Check types of top-level values
    assert isinstance(data["comments"], list), f"'comments' should be a list, got {type(data['comments'])}"
    assert isinstance(data["total"], int), f"'total' should be an integer, got {type(data['total'])}"
    assert isinstance(data["skip"], int), f"'skip' should be an integer, got {type(data['skip'])}"
    assert isinstance(data["limit"], int), f"'limit' should be an integer, got {type(data['limit'])}"

    # Step 6: Check that 'comments' is non-empty and pagination is consistent
    assert len(data["comments"]) > 0, "Comments list should not be empty"
    assert data["limit"] == len(data["comments"]), f"'limit' should equal the number of comments returned, got {data['limit']} vs {len(data['comments'])}"
    assert data["total"] > 0, "'total' should be greater than 0"
    assert data["skip"] >= 0, "'skip' should not be negative"

    # Step 7: Check that all comments have all 5 expected fields
    expected_comment_fields = ["id", "body", "postId", "likes", "user"]
    for comment in data["comments"]:
        for field in expected_comment_fields:
            assert field in comment, f"Missing field '{field}' in comment"
        # Step 8: Check data types of comment fields
        assert isinstance(comment["id"], int), f"'id' should be an integer, got {type(comment['id'])}"
        assert isinstance(comment["body"], str), f"'body' should be a string, got {type(comment['body'])}"
        assert isinstance(comment["postId"], int), f"'postId' should be an integer, got {type(comment['postId'])}"
        assert isinstance(comment["likes"], int), f"'likes' should be an integer, got {type(comment['likes'])}"
        assert isinstance(comment["user"], dict), f"'user' should be a dictionary, got {type(comment['user'])}"
        # Step 9: Check nested fields in 'user' (id, username, fullName)
        user = comment["user"]
        for field in ["id", "username", "fullName"]:
            assert field in user, f"Missing '{field}' in user"
        assert isinstance(user["id"], int), f"'id' in user should be an integer, got {type(user['id'])}"
        assert isinstance(user["username"], str), f"'username' in user should be a string, got {type(user['username'])}"
        assert isinstance(user["fullName"], str), f"'fullName' in user should be a string, got {type(user['fullName'])}"
        # Step 10: Business logic checks
        assert comment["id"] > 0, f"Comment id should be positive, got {comment['id']}"
        assert comment["postId"] > 0, f"postId should be positive, got {comment['postId']}"
        assert comment["likes"] >= 0, f"Likes cannot be negative, got {comment['likes']}"
        assert len(comment["body"]) > 0, f"Comment body should not be empty, got '{len(comment['body'])}'"
        assert user["id"] > 0, f"User id should be positive, got {user['id']}"
        assert len(user["username"]) > 0, f"Username should not be empty, got 'len({user['username']})'"
        assert len(user["fullName"]) > 0, f"Full name should not be empty, got '{len(user['fullName'])}'"

# ---------- TEST CASE: Get a single comment ----------

def test_get_comment_by_id():
    """
    Verify that GET /comments/{id} with a valid ID returns:
    - Status code 200
    - A single comment object (not a list)
    - The returned comment has the requested ID
    - All expected fields are present with correct types
    """
    # Step 1: Define a valid comment ID
    valid_id = 1

    # Step 2: Call the API
    response = client.get_comment_by_id(valid_id)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    comment = response.json()

    # Print the comment for visibility
    print(f"\nComment {valid_id}: {comment}")

    # Step 5: Check that the response is a dict (a single comment), not a list
    assert isinstance(comment, dict), "Response should be a single comment object"

    # Step 6: Check that the returned comment has the requested ID
    assert comment["id"] == valid_id, f"Expected comment id {valid_id}, got {comment['id']}"

    # Step 7: Check that all 5 expected fields are present
    expected_fields = ["id", "body", "postId", "likes", "user"]
    for field in expected_fields:
        assert field in comment, f"Missing field '{field}' in comment"

    # Step 8: Check data types of comment fields
    assert isinstance(comment["id"], int), f"'id' should be an integer, got {type(comment['id'])}"
    assert isinstance(comment["body"], str), f"'body' should be a string, got {type(comment['body'])}"
    assert isinstance(comment["postId"], int), f"'postId' should be an integer, got {type(comment['postId'])}"
    assert isinstance(comment["likes"], int), f"'likes' should be an integer, got {type(comment['likes'])}"
    assert isinstance(comment["user"], dict), f"'user' should be a dictionary, got {type(comment['user'])}"

    # Step 9: Check nested fields in 'user' (id, username, fullName)
    user = comment["user"]
    for field in ["id", "username", "fullName"]:
        assert field in user, f"Missing '{field}' in user"
    assert isinstance(user["id"], int), f"'id' in user should be an integer, got {type(user['id'])}"
    assert isinstance(user["username"], str), f"'username' in user should be a string, got {type(user['username'])}"
    assert isinstance(user["fullName"], str), f"'fullName' in user should be a string, got {type(user['fullName'])}"

    # Step 10: Business logic checks
    assert comment["id"] > 0, f"Comment id should be positive, got {comment['id']}"
    assert comment["postId"] > 0, f"postId should be positive, got {comment['postId']}"
    assert comment["likes"] >= 0, f"Likes cannot be negative, got {comment['likes']}"
    assert len(comment["body"]) > 0, f"Comment body should not be empty, got '{len(comment['body'])}'"
    assert user["id"] > 0, f"User id should be positive, got {user['id']}"
    assert len(user["username"]) > 0, f"Username should not be empty, got '{len(user['username'])}'"
    assert len(user["fullName"]) > 0, f"Full name should not be empty, got '{len(user['fullName'])}'"

# ---------- TEST CASE: Limit and skip comments ----------

def test_comments_pagination():
    """
    Verify that GET /comments with pagination + select returns:
    - Status code 200
    - Exactly the requested number of comments (limit)
    - The correct skip value
    - Different comments on different pages
    """
    # Step 1: Define pagination + select parameters
    limit = 10
    skip = 10
    select = "body,postId"

    # Step 2: Call the API for the first page
    response_page1 = client.get_comments_paginated(
        limit=limit, skip=skip, select=select)

    # Step 3: Check the status code
    assert response_page1.status_code == 200, f"Expected 200, got {response_page1.status_code}"

    # Step 4: Parse the JSON response
    data_page1 = response_page1.json()

    print(f"\nPage 1: limit={data_page1['limit']}, skip={data_page1['skip']}, total={data_page1['total']}")

    # Step 5: Check all top-level keys exist
    expected_top_level_keys = ["comments", "total", "skip", "limit"]
    for key in expected_top_level_keys:
        assert key in data_page1, f"Response is missing top-level key '{key}'"

    # Step 6: Check that the API respected our pagination parameters
    assert data_page1["limit"] == limit, f"Expected limit={limit}, got {data_page1['limit']}"
    assert data_page1["skip"] == skip, f"Expected skip={skip}, got {data_page1['skip']}"

    # Step 7: Check that we got exactly 'limit' comments
    assert len(data_page1["comments"]) == limit, f"Expected {limit} comments, got {len(data_page1['comments'])}"

    # Step 8: Check that the first comment has id=11 (since we skipped 10)
    assert data_page1["comments"][0]["id"] == skip + 1, f"First comment should have id={skip + 1} (skipped {skip})"

# Step 9: Check ALL comments — fields, types, nested user, and business logic
    expected_comment_fields = ["id", "body", "postId", "likes", "user"]
    for comment in data_page1["comments"]:
        # Check that all 5 fields exist
        for field in expected_comment_fields:
            assert field in comment, f"Missing field '{field}' in comment"
        # Check data types of comment fields
        assert isinstance(comment["id"], int), f"'id' should be an integer, got {type(comment['id'])}"
        assert isinstance(comment["body"], str), f"'body' should be a string, got {type(comment['body'])}"
        assert isinstance(comment["postId"], int), f"'postId' should be an integer, got {type(comment['postId'])}"
        assert isinstance(comment["likes"], int), f"'likes' should be an integer, got {type(comment['likes'])}"
        assert isinstance(comment["user"], dict), f"'user' should be a dictionary, got {type(comment['user'])}"
        # Check nested fields in 'user' (id, username, fullName)
        user = comment["user"]
        for field in ["id", "username", "fullName"]:
            assert field in user, f"Missing '{field}' in user"
        assert isinstance(user["id"], int), f"'id' in user should be an integer, got {type(user['id'])}"
        assert isinstance(user["username"], str), f"'username' in user should be a string, got {type(user['username'])}"
        assert isinstance(user["fullName"], str), f"'fullName' in user should be a string, got {type(user['fullName'])}"
        # Business logic checks
        assert comment["id"] > 0, f"Comment id should be positive, got {comment['id']}"
        assert comment["postId"] > 0, f"postId should be positive, got {comment['postId']}"
        assert comment["likes"] >= 0, f"Likes cannot be negative, got {comment['likes']}"
        assert len(comment["body"]) > 0, f"Comment body should not be empty, got length {len(comment['body'])}"
        assert user["id"] > 0, f"User id should be positive, got {user['id']}"
        assert len(user["username"]) > 0, f"Username should not be empty, got length {len(user['username'])}"
        assert len(user["fullName"]) > 0, f"Full name should not be empty, got length {len(user['fullName'])}"

    # Step 10: Call the API for the second page
    skip_page2 = skip + limit  # skip=20 (skip the first 20)
    response_page2 = client.get_comments_paginated(
        limit=limit, skip=skip_page2, select=select)

    assert response_page2.status_code == 200
    data_page2 = response_page2.json()

    print(f"Page 2: limit={data_page2['limit']}, skip={data_page2['skip']}, total={data_page2['total']}")

    # Step 11: Check pagination metadata of page 2
    assert data_page2["limit"] == limit, f"Expected limit={limit}, got {data_page2['limit']}"
    assert data_page2["skip"] == skip_page2, f"Expected skip={skip_page2}, got {data_page2['skip']}"
    assert len(data_page2["comments"]) == limit, f"Expected {limit} comments on page 2, got {len(data_page2['comments'])}"

    # Step 12: Check that page 1 and page 2 contain DIFFERENT comments
    # Create a list of product IDs from each page and check for overlap
    page1_ids = []
    for comment in data_page1["comments"]:
        page1_ids.append(comment["id"])
    page2_ids = []
    for comment in data_page2["comments"]:
        page2_ids.append(comment["id"])

    print(f"Page 1 IDs: {page1_ids}")
    print(f"Page 2 IDs: {page2_ids}")

    # set(...) → μετατρέπει τη λίστα σε set (συλλογή χωρίς διπλοεγγραφές)
    # & → υπολογίζει την τομή (intersection) των δύο sets, δηλαδή τα κοινά στοιχεία
    # Παράδειγμα: 
    #  set([1, 2, 3, 4, 5]) & set([6, 7, 8, 9, 10])
    #  → set()  (κανένα κοινό → άδειο)
    #  set([1, 2, 3]) & set([3, 4, 5])
    #  → {3}  (κοινό το 3)
    common_ids = set(page1_ids) & set(page2_ids)
    assert len(common_ids) == 0, f"Page 1 and Page 2 should not have common comments, but found: {common_ids}"

    # Step 13: Check that total is consistent across pages
    assert data_page1["total"] == data_page2["total"], f"'total' should be the same on both pages, got {data_page1['total']} and {data_page2['total']}"

# ---------- TEST CASE: Get all comments by post ID ----------

def test_get_comments_by_post():
    """
    Verify that GET /comments/post/{postId} returns:
    - Status code 200
    - The expected JSON structure
    - All returned comments belong to the requested post
    """
    # Step 1: Define a valid post ID
    post_id = 6

    # Step 2: Call the API
    response = client.get_comments_by_post(post_id)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    data = response.json()

    print(f"\nComments for post {post_id}: total={data['total']}")

    # Step 5: Check all top-level keys
    expected_top_level_keys = ["comments", "total", "skip", "limit"]
    for key in expected_top_level_keys:
        assert key in data, f"Response is missing top-level key '{key}'"

    # Step 6: Check types of top-level values
    assert isinstance(data["comments"], list), f"'comments' should be a list, got {type(data['comments'])}"
    assert isinstance(data["total"], int), f"'total' should be an integer, got {type(data['total'])}"
    assert isinstance(data["skip"], int), f"'skip' should be an integer, got {type(data['skip'])}"
    assert isinstance(data["limit"], int), f"'limit' should be an integer, got {type(data['limit'])}"

    # Step 7: Check pagination consistency
    assert data["limit"] == len(data["comments"]), f"'limit' should equal the number of comments returned, got {data['limit']} and {len(data['comments'])}"
    assert data["skip"] >= 0, f"'skip' should not be negative, got {data['skip']}"
    assert data["total"] >= 0, f"'total' should not be negative, got {data['total']}"

    # Step 8: Check that we got at least one comment
    assert len(data["comments"]) > 0, f"Expected at least 1 comment for post {post_id}"

    # Step 9: Check ALL comments — fields, types, nested user, business logic
    # AND most importantly: that every comment belongs to the requested post
    expected_comment_fields = ["id", "body", "postId", "likes", "user"]
    for comment in data["comments"]:
        # Check that all 5 fields exist
        for field in expected_comment_fields:
            assert field in comment, f"Missing field '{field}' in comment"

        # Check data types of comment fields
        assert isinstance(comment["id"], int), f"'id' should be an integer, got {type(comment['id'])}"
        assert isinstance(comment["body"], str), f"'body' should be a string, got {type(comment['body'])}"
        assert isinstance(comment["postId"], int), f"'postId' should be an integer, got {type(comment['postId'])}"
        assert isinstance(comment["likes"], int), f"'likes' should be an integer, got {type(comment['likes'])}"
        assert isinstance(comment["user"], dict), f"'user' should be a dictionary, got {type(comment['user'])}"
        # Check nested fields in 'user' (id, username, fullName)
        user = comment["user"]
        for field in ["id", "username", "fullName"]:
            assert field in user, f"Missing '{field}' in user"
        assert isinstance(user["id"], int), f"'id' in user should be an integer, got {type(user['id'])}"
        assert isinstance(user["username"], str), f"'username' in user should be a string, got {type(user['username'])}"
        assert isinstance(user["fullName"], str), f"'fullName' in user should be a string, got {type(user['fullName'])}"
        # FILTER LOGIC: Every comment must belong to the requested post
        assert comment["postId"] == post_id, f"Comment {comment['id']} has postId={comment['postId']}, expected {post_id}"

        # Business logic checks
        assert comment["id"] > 0, "Comment id should be positive"
        assert comment["likes"] >= 0, "Likes cannot be negative"
        assert len(comment["body"]) > 0, "Comment body should not be empty"
        assert user["id"] > 0, "User id should be positive"
        assert len(user["username"]) > 0, "Username should not be empty"
        assert len(user["fullName"]) > 0, "Full name should not be empty"

# ---------- TEST CASE: Add a comment ----------

def test_create_comment():
    """
    Verify that POST /comments/add creates a new comment:
    - Status code 201 (Created)
    - Response contains the new comment with an auto-generated ID
    - The fields we sent are returned correctly
    - The user object is populated based on the userId we sent
    """
    # Step 1: Define the new comment data
    new_comment = {
        "body": "This makes all sense to me!",
        "postId": 3,
        "userId": 5
    }

    # Step 2: Call the API to create the comment
    response = client.create_comment(new_comment)

    # Step 3: Check the status code (201 = Created)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Step 4: Parse the JSON response
    created_comment = response.json()

    print(f"\nCreated comment: {created_comment}")

    # Step 5: Check that the response is a dictionary
    assert isinstance(created_comment, dict), "Response should be a single comment object"

    # Step 6: Check that an ID was auto-generated
    assert "id" in created_comment, "Created comment should have an 'id'"
    assert isinstance(created_comment["id"], int), "'id' should be an integer"
    assert created_comment["id"] > 0, "'id' should be positive"

    # Step 7: Check that the fields we sent are returned correctly
    assert created_comment["body"] == new_comment["body"], f"Body mismatch. Expected '{new_comment['body']}', got '{created_comment['body']}'"
    assert created_comment["postId"] == new_comment["postId"], f"postId mismatch. Expected {new_comment['postId']}, got {created_comment['postId']}"

    # Step 8: Check types of returned fields
    assert isinstance(created_comment["body"], str), f"'body' should be a string, got {type(created_comment['body'])}"
    assert isinstance(created_comment["postId"], int), f"'postId' should be an integer, got {type(created_comment['postId'])}"
    assert isinstance(created_comment["user"], dict), f"'user' should be a dictionary, got {type(created_comment['user'])}"

    # Step 9: Check the nested 'user' object
    user = created_comment["user"]
    for field in ["id", "username", "fullName"]:
        assert field in user, f"Missing '{field}' in user"
    assert isinstance(user["id"], int), f"'id' in user should be an integer, got {type(user['id'])}"
    assert isinstance(user["username"], str), f"'username' in user should be a string, got {type(user['username'])}"
    assert isinstance(user["fullName"], str), f"'fullName' in user should be a string, got {type(user['fullName'])}"

    # Step 10: ⭐ The user.id should match the userId we sent
    assert user["id"] == new_comment["userId"], f"user.id mismatch. Expected {new_comment['userId']}, got {user['id']}"

    # Step 11: Business logic checks
    assert len(created_comment["body"]) > 0, "Comment body should not be empty"
    assert len(user["username"]) > 0, "Username should not be empty"
    assert len(user["fullName"]) > 0, "Full name should not be empty"

# ---------- TEST CASE: Update a comment ----------

def test_update_comment():
    """
    Verify that PUT /comments/{id} updates an existing comment:
    - Status code 200
    - The comment ID remains the same
    - The field we sent (body) is updated
    - Other fields (postId, likes, user) remain unchanged
    """
    # Step 1: Define the comment ID to update and the new data
    comment_id = 1
    updated_data = {"body": "I think I should shift to the moon"}

    # Step 2: Call the API to update the comment
    response = client.update_comment(comment_id, updated_data)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    updated_comment = response.json()

    print(f"\nUpdated comment: {updated_comment}")

    # Step 5: Check that the response is a dictionary
    assert isinstance(updated_comment, dict), "Response should be a single comment object"

    # Step 6: Check that the ID is the same as the one we requested
    assert updated_comment["id"] == comment_id, f"Expected id {comment_id}, got {updated_comment['id']}"

    # Step 7: Check that the field we sent was actually updated
    assert updated_comment["body"] == updated_data["body"], f"Body was not updated. Expected '{updated_data['body']}', got '{updated_comment['body']}'"

    # Step 8: Check that the other fields are still present (not deleted)
    assert "postId" in updated_comment, "postId should remain after partial update"
    assert "likes" in updated_comment, "likes should remain after partial update"
    assert "user" in updated_comment, "user should remain after partial update"

    # Step 9: Check types of all fields
    assert isinstance(updated_comment["id"], int), f"'id' should be an integer, got {type(updated_comment['id'])}"
    assert isinstance(updated_comment["body"], str), f"'body' should be a string, got {type(updated_comment['body'])}"
    assert isinstance(updated_comment["postId"], int), f"'postId' should be an integer, got {type(updated_comment['postId'])}"
    assert isinstance(updated_comment["likes"], int), f"'likes' should be an integer, got {type(updated_comment['likes'])}"
    assert isinstance(updated_comment["user"], dict), f"'user' should be a dictionary, got {type(updated_comment['user'])}"

    # Step 10: Check nested 'user' object structure
    user = updated_comment["user"]
    for field in ["id", "username", "fullName"]:
        assert field in user, f"Missing '{field}' in user"
    assert isinstance(user["id"], int)
    assert isinstance(user["username"], str)
    assert isinstance(user["fullName"], str)

    # Step 11: Business logic checks
    assert len(updated_comment["body"]) > 0, "Comment body should not be empty"
    assert updated_comment["postId"] > 0, "postId should be positive"
    assert updated_comment["likes"] >= 0, "Likes cannot be negative"

# ---------- TEST CASE: Delete a comment ----------

def test_delete_comment():
    """
    Verify that DELETE /comments/{id} deletes a comment:
    - Status code 200
    - The response contains the deleted comment
    - The 'isDeleted' field is True
    - The 'deletedOn' field is a valid timestamp
    - The original comment fields are still present
    """
    # Step 1: Define the comment ID to delete
    comment_id = 1

    # Step 2: Call the API to delete the comment
    response = client.delete_comment(comment_id)

    # Step 3: Check the status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Step 4: Parse the JSON response
    deleted_comment = response.json()

    print(f"\nDeleted comment: id={deleted_comment['id']}, {deleted_comment} "
          f"isDeleted={deleted_comment['isDeleted']}, "
          f"deletedOn={deleted_comment['deletedOn']}")

    # Step 5: Check that the response is a dictionary
    assert isinstance(deleted_comment, dict), "Response should be a single comment object"

    # Step 6: Check that the ID is the same as the one we requested
    assert deleted_comment["id"] == comment_id, f"Expected id {comment_id}, got {deleted_comment['id']}"

    # Step 7: Check that the deletion-specific fields exist
    assert "isDeleted" in deleted_comment, "Response should contain 'isDeleted' field"
    assert "deletedOn" in deleted_comment, "Response should contain 'deletedOn' field"

    # Step 8: Check that 'isDeleted' is True
    assert deleted_comment["isDeleted"] is True, f"'isDeleted' should be True, got {deleted_comment['isDeleted']}"

    # Step 9: Check types of deletion fields
    assert isinstance(deleted_comment["isDeleted"], bool), f"'isDeleted' should be a boolean, got {type(deleted_comment['isDeleted'])}"
    assert isinstance(deleted_comment["deletedOn"], str), f"'deletedOn' should be a string (timestamp), got {type(deleted_comment['deletedOn'])}"

    # Step 10: Check that 'deletedOn' is not empty
    assert len(deleted_comment["deletedOn"]) > 0, "'deletedOn' should not be empty"

    # Step 11: Check that the original comment fields are still present
    expected_fields = ["id", "body", "postId", "likes", "user"]
    for field in expected_fields:
        assert field in deleted_comment, f"Original field '{field}' should still be present after delete"

    # Step 12: Check types of original fields
    assert isinstance(deleted_comment["body"], str)
    assert isinstance(deleted_comment["postId"], int)
    assert isinstance(deleted_comment["likes"], int)
    assert isinstance(deleted_comment["user"], dict)

    # Step 13: Check nested 'user' object
    user = deleted_comment["user"]
    for field in ["id", "username", "fullName"]:
        assert field in user, f"Missing '{field}' in user"
    assert isinstance(user["id"], int)
    assert isinstance(user["username"], str)
    assert isinstance(user["fullName"], str)
    assert user["id"] > 0, "User id should be positive"
    assert len(user["username"]) > 0, "Username should not be empty"
    assert len(user["fullName"]) > 0, "Full name should not be empty"