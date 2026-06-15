def register(client, email: str) -> dict:
    response = client.post(
        "/api/auth/register",
        json={"name": "Usuário Teste", "email": email, "password": "senha-segura-123"},
    )
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_full_campaign_flow(client):
    headers = register(client, "owner@example.com")
    created = client.post(
        "/api/campaigns",
        headers=headers,
        json={
            "title": "Agentes de IA para empresas",
            "theme": "Como agentes de IA reduzem tarefas repetitivas",
            "input_type": "theme",
            "audience": "empresários e gestores",
            "objective": "gerar leads",
            "tone": "consultivo",
            "cta": "Solicite um diagnóstico",
        },
    )
    assert created.status_code == 201
    campaign_id = created.json()["id"]

    generated = client.post(f"/api/campaigns/{campaign_id}/generate", headers=headers)
    assert generated.status_code == 200
    body = generated.json()
    assert body["status"] == "generated"
    assert len(body["assets"]) == 8
    assert body["quality_score"] == 8

    linkedin = next(item for item in body["assets"] if item["asset_type"] == "linkedin_post")
    edited = client.patch(
        f"/api/assets/{linkedin['id']}",
        headers=headers,
        json={"content": "Conteúdo revisado pela equipe.", "status": "review"},
    )
    assert edited.status_code == 200
    assert edited.json()["content"] == "Conteúdo revisado pela equipe."

    approved = client.post(f"/api/campaigns/{campaign_id}/approve", headers=headers)
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"


def test_user_cannot_access_another_users_campaign(client):
    owner = register(client, "owner2@example.com")
    outsider = register(client, "outsider@example.com")
    campaign = client.post(
        "/api/campaigns",
        headers=owner,
        json={"title": "Campanha privada", "theme": "Tema privado"},
    )
    response = client.get(f"/api/campaigns/{campaign.json()['id']}", headers=outsider)
    assert response.status_code == 404
