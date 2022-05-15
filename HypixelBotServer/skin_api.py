from io import BytesIO

import aiohttp
import flask

from .database.__all_models import UrlCounter
from .database.db_session import create_session

blueprint = flask.Blueprint("skin_api", __name__)
session = create_session()


async def get_skin_image(url) -> BytesIO:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            buffer = BytesIO(await resp.read())

    return buffer


@blueprint.route("/api/image/<int:url_counter_id>", methods=["GET"])
async def get_image(url_counter_id):
    url = session.query(UrlCounter).get(url_counter_id).base_url
    image = await get_skin_image(url)

    return flask.send_file(image, mimetype="image/x-png")


@blueprint.route("/api/avatar/<uuid>", methods=["GET"])
def get_avatar_url(uuid):
    print("HELLO")
    url_counter = UrlCounter(
        base_url=f"https://crafatar.com/avatars/{uuid}?overlay",
    )
    session.add(url_counter)
    session.commit()

    return flask.jsonify({"url": f"/api/image/{url_counter.id}"})


@blueprint.route("/api/skin/<uuid>", methods=["GET"])
def get_skin_url(uuid):
    url_counter = UrlCounter(
        base_url=f"https://crafatar.com/renders/body/{uuid}?overlay",
    )
    session.add(url_counter)
    session.commit()

    return flask.jsonify({"url": f"/api/image/{url_counter.id}"})


@blueprint.route("/api/head/<uuid>", methods=["GET"])
def get_head_url(uuid):
    url_counter = UrlCounter(
        base_url=f"https://crafatar.com/renders/head/{uuid}?overlay",
    )
    session.add(url_counter)
    session.commit()

    return flask.jsonify({"url": f"/api/image/{url_counter.id}"})
