from fastapi.testclient import TestClient
import pytest 
from app import app
from fastapi import HTTPException 

import sys
import os

print("cwd:", os.getcwd())
print("sys.path:")
for p in sys.path:
    print(" ", p)

# @pytest.fixture
# def client():
#     return TestClient(app)

# # @pytest.fixture
# # def registered_user(client: TestClient) -> str:
# #     res = client.post(
# #         "/api/auth/signup",
# #         json={
# #             "email": "test@test.com",
# #             "password": "test123"
# #         }
# #     )

# #     return res.json()
    

# def test_succesful_sign_up(client: TestClient):
#     res = client.post(
#         "/api/auth/signup",
#         json={
#             "email": "test@test.com",
#             "password": "test123"
#         }
#     )
#     assert res.status_code == 200 
#     assert res.json()['auth_id']

