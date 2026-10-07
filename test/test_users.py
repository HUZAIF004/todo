from starlette import testclient
from starlette import testclient
from starlette import testclient
from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status
from ..models import Users

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/users/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'huzaif' 
    assert response.json()['email'] ==  'hzf2379@gmail.com'
    assert response.json()['first_name'] == 'Mohammed'
    assert response.json()['last_name'] == 'Huzaif'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'

def test_change_password_success(test_user):
    response = client.put('/users/change_password',json = {'password':'test1234','new_password':'test123'})
    assert  response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid(test_user):
    response = client.put('/users/change_password',json = {'password':'wrongpass','new_password':'test123'})
    assert  response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Error on password change'}

def test_phone_number_change(test_user):
    response = client.put('/users/update_phone_number/1212121212')
    assert response.status_code == status.HTTP_204_NO_CONTENT



