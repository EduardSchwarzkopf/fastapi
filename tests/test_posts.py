from typing import List
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
