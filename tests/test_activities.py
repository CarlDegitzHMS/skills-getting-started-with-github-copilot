def test_get_activities_returns_full_activity_map(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Clubs" in data
    assert "Programming Class" in data

    chess = data["Chess Clubs"]
    assert set(chess.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert isinstance(chess["participants"], list)


def test_get_activities_handles_empty_participants_list(client):
    clear_resp = client.delete(
        "/activities/Tennis Club/signup",
        params={"email": "ava@mergington.edu"},
    )
    assert clear_resp.status_code == 200

    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json()["Tennis Club"]["participants"] == []


def test_get_activities_reflects_signup_mutation(client):
    email = "new.student@mergington.edu"

    signup = client.post(
        "/activities/Robotics Club/signup",
        params={"email": email},
    )
    assert signup.status_code == 200

    response = client.get("/activities")
    assert response.status_code == 200
    assert email in response.json()["Robotics Club"]["participants"]
