import pytest
from app.models.author import Author

def test_get_all_authors_with_no_records(client):
    # Act

    # Client fixture in conftest.py
    response = client.get("/authors")
    # This sends an HTTP request to /authors.
    # It returns an HTTP response object, which we store in our local variable response
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_author(client, two_saved_authors):
    # Act
    response = client.get("/authors/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Ocean author"
    }


def test_create_one_author(client):
    # Act
    response = client.post("/authors", json={
        "name": "New author"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "New author"
    }

# -------- new tests --------------
# @pytest.mark.skip()
def test_update_author(client, two_saved_authors):
    # Arrange
    test_data = {
        "name": "New author"
    }

    # Act
    response = client.put("/authors/1", json=test_data)
    # response_body = response.get_json() # No response body acc. to our update endpoint method

    # Assert
    assert response.status_code == 204
    assert response.data == b''  # here checking the response has no content


# @pytest.mark.skip()
def test_update_author_with_extra_keys(client, two_saved_authors):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "New author",
        "description": "ha!",
        "another": "last value"
    }

    # Act
    response = client.put("/authors/1", json=test_data)
    # response_body = response.get_json()

    # Assert
    assert response.status_code == 204
    assert response.data == b''
#  ***************************************
#               OPTIONAL
#          Verify update in DB
#  ***************************************
    
    updated_author = Author.query.get(1)
    assert updated_author.name == "New author"
    # assert updated_author.description == "The Best!"


# @pytest.mark.skip()
def test_update_author_missing_record(client, two_saved_authors):
    # Arrange
    test_data = {
        "name": "New author"
    }

    # Act
    response = client.put("/authors/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Author 3 not found"}


# @pytest.mark.skip()
def test_update_author_invalid_id(client, two_saved_authors):
    # Arrange
    test_data = {
        "name": "New author"
    }

    # Act
    response = client.put("/authors/cat", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Author cat invalid"}


@pytest.mark.skip()
def test_delete_author(client, two_saved_authors):
    # Act
    response = client.delete("/authors/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Author #1 successfully deleted"


# @pytest.mark.skip()
def test_delete_author_missing_record(client, two_saved_authors):
    # Act
    response = client.delete("/authors/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Author 3 not found"}

# @pytest.mark.skip()
def test_delete_author_invalid_id(client, two_saved_authors):
    # Act
    response = client.delete("/authors/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Author cat invalid"}