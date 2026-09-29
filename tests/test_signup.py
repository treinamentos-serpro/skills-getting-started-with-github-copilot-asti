def test_signup_adds_student_to_activity(client):
    email = "new.student@mergington.edu"

    response = client.post(
        "/activities/Art Club/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up new.student@mergington.edu for Art Club"
    }
    assert email in client.get("/activities").json()["Art Club"]["participants"]


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_student(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    participant_count = len(client.get("/activities").json()[activity_name]["participants"])

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert len(client.get("/activities").json()[activity_name]["participants"]) == participant_count


def test_cancel_signup_removes_student_from_activity(client):
    activity_name = "Art Club"
    email = "student@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Canceled signup for student@mergington.edu from Art Club"
    }
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_cancel_signup_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_cancel_signup_rejects_student_who_is_not_signed_up(client):
    response = client.delete(
        "/activities/Art Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
