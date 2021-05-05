import os
import random
import re

from flask_security import current_user
from sqlalchemy import asc
from uuid import uuid4
from pathlib import Path, PurePosixPath, PureWindowsPath, PurePath
from app import db
from datetime import datetime

from config import Config


def default_thumbnail():
    return Path(os.path.join(Config.INDEX_IMAGES_PATH, random.choice(os.listdir(Config.INDEX_IMAGES_FULLPATH))))


class Post(db.Model):
    __tablename__ = 'posts'

    _uuid = db.Column(db.String(255), primary_key=True, unique=True, default=uuid4().hex)
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    body = db.Column(db.Text)
    post_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    last_modified = db.Column(db.DateTime, index=True)
    draft = db.Column(db.Boolean, default=False)
    thumbnail = db.Column(db.String(128), default=default_thumbnail())

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Many to Many
    tags = db.relationship('Tag',
                           secondary='posts_tags',
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, description, body, user_id, _uuid=None, tags=None,
                 post_date=datetime.utcnow()):
        self._uuid = uuid4().hex if _uuid is None else _uuid
        self.title = title
        self.description = description
        self.body = body
        self.post_date = datetime.utcnow() if post_date is None else post_date
        self.tags = tags
        self.thumbnail = self.generate_thumbnail()
        self.user_id = user_id

    def __repr__(self):
        return f"<Post uuid: {self._uuid}, title: {self.title}, author: {self.user_id}, tags: {self.tags}>"

    def generate_thumbnail(self):
        images = os.listdir(Config.INDEX_IMAGES_FULLPATH)
        randomized_tag = random.choice(self.normalize_tags(tags=self.tags))
        regex = re.compile(randomized_tag+r"\.")
        selected_images = list(filter(regex.match, images))

        if len(selected_images) > 0:
            return Path(os.path.join(Config.INDEX_IMAGES_PATH, random.choice(selected_images)))
        return Path(os.path.join(Config.INDEX_IMAGES_PATH, random.choice(images)))

    @staticmethod
    def delete_post(post_id):
        post_to_delete = Post.query_posts_by_id(post_id=post_id)
        if post_to_delete is None:
            return False

        db.session.remove(post_to_delete)
        db.session.commit()
        return True

    @classmethod
    def query_posts(cls):
        return cls.query

    @classmethod
    def query_posts_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def query_posts_by_id(cls, post_id):
        return cls.query.filter_by(_id=post_id).first()

    @classmethod
    def query_posts_by_date(cls):
        return cls.query.order_by(asc(Post.post_date))

    @classmethod
    def count_posts_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).count()

    @classmethod
    def count_posts(cls, tag, user_id):
        return Post.query.filter_by(tag=tag, user_id=user_id).count()

    @staticmethod
    def normalize_tags(tags):
        # print(tags)
        if len(tags) <= 0:
            return Config.BLOGGING_DEFAULT_TAG
        return [tag.name for tag in tags]

    @staticmethod
    def _from_timestamp(timestamp):
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")

    # Not used - here for reference.
    @staticmethod
    def get_index_images():
        images = os.listdir(Config.INDEX_IMAGES_FULLPATH)
        new_images = []
        for image in images:
            x = os.path.join(Config.INDEX_IMAGES_FULLPATH, image).rsplit('/')[1:]
            new_images.append(''.join(['/' + v for v in x]))
        random.shuffle(new_images)
        return images


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Tag id: {self.id}, name: {self.name}>"

    @staticmethod
    def populate_tags():
        all_tags = Tag.get_tags()
        return [[tag.id, tag.name] for tag in all_tags]

    @staticmethod
    def get_tags():
        return Tag.query.all()

    @staticmethod
    def get_tag_by_name(name):
        return Tag.query.filter_by(name=name).first()

    @staticmethod
    def get_tag_by_id(_id):
        return Tag.query.filter_by(id=_id).first()

    @staticmethod
    def create_tags(tag_list=Config.BLOGGING_TAGS):
        for tag in tag_list:
            c_tag = Tag.get_tag_by_name(name=tag)
            if c_tag is None:
                # create the new tag in the DB
                new_tag = Tag(
                    name=tag,
                    description="{} tag".format(tag)
                )
                db.session.add(new_tag)
                db.session.commit()


class PostsTags(db.Model):
    __tablename__ = 'posts_tags'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(255), db.ForeignKey('posts._uuid', ondelete='CASCADE'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'))

    def __init__(self, post_id, tag_id):
        self.post_id = post_id
        self.tag_id = tag_id
