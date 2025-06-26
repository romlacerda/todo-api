from .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_user.username
    assert response.json()['email'] == test_user.email
    assert response.json()['first_name'] == test_user.first_name
    assert response.json()['last_name'] == test_user.last_name
    assert response.json()['phone_number'] == test_user.phone_number
    
    
def test_change_password_success(test_user):
    response = client.put("/user/change-password", json={
        "current_password": "testpassword",
        "new_password": "newpassword",
        "new_password_confirm": "newpassword"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change-password", json={
        "current_password": "wrongpassword",
        "new_password": "newpassword",
        "new_password_confirm": "newpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == "Current password is incorrect"

def test_change_password_mismatch_new_password(test_user):
    response = client.put("/user/change-password", json={
        "current_password": "testpassword",
        "new_password": "newpassword",
        "new_password_confirm": "wrongpassword"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_change_phone_number_success(test_user):
    response = client.put('/user/change-phone-number', json={
        "phone_number": "2212312213"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT
