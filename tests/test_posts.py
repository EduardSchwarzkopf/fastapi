import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostResult(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.Post(**res.json())

    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content
    assert res.status_code == 200


def test_get_one_post_not_exits(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/9999999")

    assert res.status_code == 404


@pytest.mark.parametrize(
    "title, content",
    [
        ("awesome title", "awesome content"),
        ("title", "content"),
        ("best pizza in town", "my favorites places are..."),
        ("my title", "my content"),
    ],
)
def test_create_post(authorized_client, test_user, title, content):
    res = authorized_client.post("/posts/", json={"title": title, "content": content})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner.id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "new title", "content": "content"}
    )

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.published == True
    assert created_post.owner.id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user):
    res = client.post("/posts/", json={"title": "new title", "content": "content"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_none_exists(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/999999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403
