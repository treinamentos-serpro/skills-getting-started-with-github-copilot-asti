def test_get_activities_returns_expected_activity_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities

    activity = activities["Chess Club"]
    assert set(activity) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert isinstance(activity["participants"], list)
