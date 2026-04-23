def test_unregister_succeeds_for_registered_student(client):
    email = "emma@mergington.edu"

    response = client.delete(
        "/activities/Programming Class/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from Programming Class"
    }

    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown Activity/signup",
        params={"email": "casey@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_non_member_returns_404(client):
    response = client.delete(
        "/activities/Science Olympiad/signup",
        params={"email": "not.enrolled@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Student not registered for this activity"}


def test_unregister_repeated_delete_returns_404_after_first_success(client):
    email = "lucas@mergington.edu"

    first = client.delete(
        "/activities/Music Ensemble/signup",
        params={"email": email},
    )
    assert first.status_code == 200

    second = client.delete(
        "/activities/Music Ensemble/signup",
        params={"email": email},
    )
    assert second.status_code == 404
    assert second.json() == {"detail": "Student not registered for this activity"}


def test_unregister_missing_email_query_param_returns_422(client):
    response = client.delete("/activities/Programming Class/signup")

    assert response.status_code == 422
