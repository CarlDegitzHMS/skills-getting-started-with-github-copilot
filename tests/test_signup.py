def test_signup_succeeds_for_existing_activity(client):
    email = "casey@mergington.edu"

    response = client.post(
        "/activities/Art Studio/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Art Studio"}

    activities = client.get("/activities").json()
    assert email in activities["Art Studio"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "casey@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_email_returns_400(client):
    existing_email = "michael@mergington.edu"

    response = client.post(
        "/activities/Chess Clubs/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_activity_name_with_url_encoded_space(client):
    email = "encoded@mergington.edu"

    response = client.post(
        "/activities/Chess%20Clubs/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Clubs"}


def test_signup_missing_email_query_param_returns_422(client):
    response = client.post("/activities/Chess Clubs/signup")

    assert response.status_code == 422
