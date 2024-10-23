def test_search_by_name(client):
    response = client.get("/search/name/?name=Albert Einstein")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["firstname"] == "Albert"
    assert data[0]["surname"] == "Einstein"

def test_search_by_category(client):
    response = client.get("/search/category/?category=physics")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "physics" in data[0]["category"].lower()

def test_search_by_description(client):
    response = client.get("/search/description/?description=photoelectric effect")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

    # Loop through each document, then through each laureate inside it
    for prize in data:
        for laureate in prize["laureates"]:
            assert "motivation" in laureate, "Motivation field missing in laureate"
            assert "photoelectric effect" in laureate["motivation"].lower()
