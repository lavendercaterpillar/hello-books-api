def test_get_all_books_with_no_records(client):
    # Act

    # Client fixture in conftest.py
    response = client.get("/books")
    # This sends an HTTP request to /books.
    # It returns an HTTP response object, which we store in our local variable response
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


