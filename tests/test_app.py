import requests


def test_read_main():
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_expenses():
    response = requests.get("http://localhost:8000/expenses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_expense():
    response = requests.get("http://localhost:8000/expenses/1")
    assert response.status_code == 200
    assert "id" in response.json()


def test_read_expense_not_found():
    response = requests.get("http://localhost:8000/expenses/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_create_expense():
    expense_data = {"amount": 100.0, "description": "Test expense", "category": "food"}
    response = requests.post("http://localhost:8000/expenses/", json=expense_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Test expense"


def test_create_expense_invalid():
    expense_data = {
        "amount": -50.0,
        "description": "Invalid expense",
        "category": "food",
    }
    response = requests.post("http://localhost:8000/expenses/", json=expense_data)
    assert response.status_code == 422


def test_update_expense():
    expense_data = {
        "amount": 150.0,
        "description": "Updated expense",
        "category": "transport",
    }
    response = requests.put("http://localhost:8000/expenses/1", json=expense_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated expense"


def test_update_expense_invalid():
    expense_data = {
        "amount": -50.0,
        "description": "Invalid update",
        "category": "food",
    }
    response = requests.put("http://localhost:8000/expenses/1", json=expense_data)
    assert response.status_code == 422


def test_update_expense_not_found():
    expense_data = {
        "amount": 150.0,
        "description": "Updated expense",
        "category": "transport",
    }
    response = requests.put("http://localhost:8000/expenses/999", json=expense_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_delete_expense():
    response = requests.delete("http://localhost:8000/expenses/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Expense deleted successfully"}


def test_delete_expense_not_found():
    response = requests.delete("http://localhost:8000/expenses/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"


def test_read_expenses_by_category():
    response = requests.get("http://localhost:8000/expenses/?category=food")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for expense in response.json():
        assert expense["category"] == "food"


def test_read_expenses_by_invalid_category():
    response = requests.get("http://localhost:8000/expenses/?category=invalid")
    assert response.status_code == 422
