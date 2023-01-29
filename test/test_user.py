import uuid


def get_user_json(name, email, address):
    return {"user": {"name": name, "email": email, "address": address}}


# app_client configured with pytest
def test_main_user_flow(app_client):
    # create a user
    random_id = uuid.uuid1()
    user_email = f"{random_id}@testmail.com"
    name = f"test_user {random_id}"
    address = f"test_user address {random_id}"

    input_json = get_user_json(name, user_email, address)

    response = app_client.post("/user/", json=input_json)

    assert response.status_code == 200
    output = response.json()

    assert output["name"] == name
    assert output["email"] == user_email
    assert output["address"] == address

    user_id = output.get("id")
    assert user_id is not None

    # list the user
    response = app_client.get(f"/user/")
    assert response.status_code == 200
    output = response.json()
    assert len(output) > 0

    # update the user

    new_name = f"test_user modified {random_id}"
    new_address = f"test_user address modified {random_id}"
    new_email = f"{random_id}@modified.email.com"
    input_json = get_user_json(new_name, new_email, new_address)

    response = app_client.put(f"/user/{user_id}", json=input_json)
    assert response.status_code == 200
    output = response.json()
    assert output["name"] == new_name
    assert output["email"] == new_email
    assert output["address"] == new_address

    # delete the user
    response = app_client.delete(f"/user/{user_id}")
    assert response.status_code == 200


def test_should_validate_create(app_client):
    # create a user
    random_id = uuid.uuid1()
    name = f"test_invalid_user {random_id}"
    address = f"test_invalid_user address {random_id}"
    user_email = f"{random_id}testmailcom"

    input_json = get_user_json(name, user_email, address)
    response = app_client.post("/user/", json=input_json)
    assert response.status_code == 422
    output = response.json()
    user_id = output.get("id")
    try:
        assert output["detail"][0]["loc"] == ['body', 'user', 'email']
    finally:
        # delete the user
        app_client.delete(f"/user/{user_id}")

