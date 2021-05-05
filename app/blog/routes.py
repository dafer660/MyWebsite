import datetime
import os
import shutil
import math
import imghdr

from uuid import uuid4
from flask_wtf.csrf import CSRFError

from app import db
from config import Config

from flask import current_app, render_template, request, redirect, \
    url_for, send_from_directory, jsonify, flash

from flask_security import login_required, current_user
from flask_principal import PermissionDenied

# from werkzeug.contrib.atom import AtomFeed
from werkzeug.utils import secure_filename

from app.blog import bp

from app.blog.utils import ensureUtf
from app.blog.forms import BlogEditor, FileUploader

from app.models.posts import Post, Tag, PostsTags
from app.models.roles import Role

from app.main.forms import PostForm

from app.functions.post_img import get_post_img


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    _format = imghdr.what(None, header)

    if not _format:
        return None
    return '.' + (_format if _format != 'jpeg' else 'jpg')


@login_required
@bp.route('/posts', methods=['GET', 'POST'])
def posts():
    post_uuid = uuid4().hex
    posts = Post.query_posts_by_date()
    tags = PostsTags.query.all()
    page = request.args.get('page')
    search = request.args.get('search_post')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if search:
        posts = Post.query.filter(
            Post.title.contains(search) |
            Post.description.contains(search) |
            Post.author.contains(search)
        )
        posts = posts.paginate(page=page, per_page=Config.BLOGGING_POSTS_PER_PAGE)
    else:
        posts = posts.paginate(page=page, per_page=Config.BLOGGING_POSTS_PER_PAGE)

    return render_template('blog/index_post.html', posts=posts, post_uuid=post_uuid, tags=tags)


@bp.route('/post/<string:post_uuid>', methods=['GET'])
@login_required
def view_post(post_uuid):
    pass


@bp.route('/new_post/<string:post_uuid>', methods=['GET', 'POST'])
@login_required
def new_post(post_uuid):
    form = BlogEditor()

    try:
        uploaded_files = os.listdir(os.path.join(Config.FILEUPLOAD_PATH, post_uuid))
        # Just in case we need to check the files
        # print(uploaded_files)
    except Exception as e:
        uploaded_files = []

    files_dict = dict(enumerate(uploaded_files, start=1))

    if request.method == 'POST' and form.is_submitted():

        if form.upload.data and form.is_submitted():
            image = request.files['image']
            filename = secure_filename(image.filename)
            post_dir = os.path.join(Config.FILEUPLOAD_PATH, post_uuid)

            if not os.path.exists(post_dir):
                os.makedirs(post_dir)

            image_url = os.path.join(post_dir, filename)

            image.save(image_url)
            image_resp = os.path.join(Config.FILEUPLOADED_PATH, post_uuid, filename)

            response = dict(
                {'filename': filename,
                 'post_uuid': post_uuid,
                 'title': form.title.data,
                 'description': form.description.data,
                 'body': form.body.data,
                 'tags': form.tags.data
                 })

            try:
                files = os.listdir(os.path.join(Config.FILEUPLOAD_PATH, post_uuid))
                files_dict = dict(enumerate(files, start=1))
                response['files'] = files
                response['files_dict'] = files_dict
            except Exception as e:
                print(e)
                files = []
                response['files'] = files

            if filename in uploaded_files:
                flash("Image already uploaded...", "info")
            else:
                flash("Image uploaded to {} !!".format(image_resp), "success")

            form.title.data = response.get('title')
            form.description.data = response.get('description')
            form.body.data = response.get('body')
            form.tags.choices = Tag.populate_tags()
            form.tags.data = response.get('tags')

            # print(response)
            # return jsonify(response)
            return render_template('blog/new_post.html', form=form, post_uuid=post_uuid, files_dict=files_dict)

        if form.submit.data and form.is_submitted():

            tags = [Tag.get_tag_by_id(int(tag)) for tag in form.tags.data]

            post = Post(
                title=form.title.data,
                description=form.description.data,
                body=form.body.data,
                user_id=current_user.id,
                _uuid=post_uuid,
                post_date=datetime.datetime.utcnow(),
                tags=tags
            )

            db.session.add(post)
            db.session.commit()

            flash("Post submitted successfully!!", "success")
            return redirect(url_for('blog.posts', page=1))

        if form.cancel.data and form.is_submitted():
            image_dir = os.path.join(Config.FILEUPLOAD_PATH, post_uuid)
            if os.path.exists(image_dir):
                shutil.rmtree(image_dir, ignore_errors=True)
            flash("Post disposed", "danger")

            return redirect(url_for('blog.posts', page=1))

    form.tags.choices = Tag.populate_tags()

    return render_template('blog/new_post.html', form=form, post_uuid=post_uuid, files_dict=files_dict)


@login_required
@bp.route('/upload_files', methods=['GET', 'POST'])
def upload_files():
    form = BlogEditor()

    try:
        post_uuid = request.referrer.split('/')[-1]
    except Exception as err_uuid:
        print(err_uuid)

    try:
        files = os.listdir(os.path.join(Config.FILEUPLOAD_PATH, post_uuid))
    except Exception as e:
        files = []

    if request.method == 'POST':
        image = request.files['image']
        filename = secure_filename(image.filename)
        post_dir = os.path.join(Config.FILEUPLOAD_PATH, post_uuid)

        if not os.path.exists(post_dir):
            os.makedirs(post_dir)

        image_url = os.path.join(post_dir, filename)

        image.save(image_url)
        image_resp = os.path.join(Config.FILEUPLOADED_PATH, post_uuid, filename)

        response = dict(
            {'image_resp': image_resp,
             'post_dir': post_dir,
             'filename': filename})
        response['files'] = files

        try:
            files = os.listdir(os.path.join(Config.FILEUPLOAD_PATH, post_uuid))
            response['files'] = files
        except Exception as e:
            print(e)
            files = []

        return redirect(request.url)

    return render_template('blog/new_post.html', form=form, files=files, post_uuid=post_uuid)


@bp.route('/fileuploads/<post_uuid>/<filename>', methods=['GET'])
def get_upload(post_uuid, filename):
    image_dir = os.path.join(Config.FILEUPLOAD_PATH, post_uuid)
    return send_from_directory(image_dir, filename)


@bp.errorhandler(CSRFError)
def csrf_error(e):
    return e.description, 400


@bp.route('/blog', methods=['GET'])
def blog():
    form = BlogEditor()
    return render_template('blog/editor.html', form=form)


@bp.route('/post/<post_id>', methods=['GET'])
@login_required
def post(post_id):
    post = Post.query_posts_by_id(post_id=post_id)
    return render_template('blog/index_post.html', post=post)


# def page_by_id(post_id, slug):
#     blogging_engine = _get_blogging_engine(current_app)
#     storage = blogging_engine.storage
#     config = blogging_engine.config
#     post = storage.get_post_by_id(post_id)
#     meta = {}
#     meta["is_user_blogger"] = _is_blogger(blogging_engine.blogger_permission)
#
#     render = config.get("BLOGGING_RENDER_TEXT", True)
#     meta["post_id"] = post_id
#     meta["slug"] = slug
#     page_by_id_fetched.send(blogging_engine.app, engine=blogging_engine,
#                             post=post, meta=meta)
#     if post is not None:
#         blogging_engine.process_post(post, render=render)
#         page_by_id_processed.send(blogging_engine.app, engine=blogging_engine,
#                                   post=post, meta=meta)
#         return render_template("blogging/page.html", post=post, config=config,
#                                meta=meta)
#     else:
#         flash("The page you are trying to access is not valid!", "warning")
#         return redirect(url_for("blogging.index"))
#
#
# def posts_by_tag(tag, count, page):
#     blogging_engine = _get_blogging_engine(current_app)
#     storage = blogging_engine.storage
#     config = blogging_engine.config
#     count = count or config.get("BLOGGING_POSTS_PER_PAGE", 10)
#     meta = _get_meta(storage, count, page, tag=tag)
#     offset = meta["offset"]
#     meta["is_user_blogger"] = _is_blogger(blogging_engine.blogger_permission)
#     meta["tag"] = tag
#     meta["count"] = count
#     meta["page"] = page
#     render = config.get("BLOGGING_RENDER_TEXT", True)
#     posts = storage.get_posts(count=count, offset=offset, tag=tag,
#                               include_draft=False, user_id=None, recent=True)
#     posts_by_tag_fetched.send(blogging_engine.app, engine=blogging_engine,
#                               posts=posts, meta=meta)
#     if len(posts):
#         for post in posts:
#             blogging_engine.process_post(post, render=render)
#         posts_by_tag_processed.send(blogging_engine.app,
#                                     engine=blogging_engine,
#                                     posts=posts, meta=meta)
#         return render_template("blogging/index.html", posts=posts, meta=meta,
#                                config=config)
#     else:
#         flash("No posts found for this tag!", "warning")
#         return redirect(url_for("blogging.index", post_id=None))
#
#
# def posts_by_author(user_id, count, page):
#     blogging_engine = _get_blogging_engine(current_app)
#     storage = blogging_engine.storage
#     config = blogging_engine.config
#     count = count or config.get("BLOGGING_POSTS_PER_PAGE", 10)
#     meta = _get_meta(storage, count, page, user_id=user_id)
#     offset = meta["offset"]
#     meta["is_user_blogger"] = _is_blogger(blogging_engine.blogger_permission)
#     meta["user_id"] = user_id
#     meta["count"] = count
#     meta["page"] = page
#
#     posts = storage.get_posts(count=count, offset=offset, user_id=user_id,
#                               include_draft=False, tag=None, recent=True)
#     render = config.get("BLOGGING_RENDER_TEXT", True)
#     posts_by_author_fetched.send(blogging_engine.app, engine=blogging_engine,
#                                  posts=posts, meta=meta)
#     if len(posts):
#         for post in posts:
#             blogging_engine.process_post(post, render=render)
#         posts_by_author_processed.send(blogging_engine.app,
#                                        engine=blogging_engine, posts=posts,
#                                        meta=meta)
#         return render_template("blogging/index.html", posts=posts, meta=meta,
#                                config=config)
#     else:
#         flash("No posts found for this user!", "warning")
#         return redirect(url_for("blogging.index", post_id=None))
#
#
# @login_required
# def editor(post_id):
#     blogging_engine = _get_blogging_engine(current_app)
#     cache = blogging_engine.cache
#     if cache:
#         _clear_cache(cache)
#     try:
#         with blogging_engine.blogger_permission.require():
#             post_processor = blogging_engine.post_processor
#             config = blogging_engine.config
#             storage = blogging_engine.storage
#             if request.method == 'POST':
#                 form = BlogEditor(request.form)
#                 if form.validate():
#                     post = storage.get_post_by_id(post_id)
#                     if (post is not None) and \
#                             (PostProcessor.is_author(post, current_user)) and \
#                             (str(post["post_id"]) == post_id):
#                         pass
#                     else:
#                         post = {}
#                     escape_text = config.get("BLOGGING_ESCAPE_MARKDOWN", False)
#                     pid = _store_form_data(form, storage, current_user, post,
#                                            escape_text)
#                     editor_post_saved.send(blogging_engine.app,
#                                            engine=blogging_engine,
#                                            post_id=pid,
#                                            user=current_user,
#                                            post=post)
#                     flash("Blog posted successfully!", "info")
#                     slug = post_processor.create_slug(form.title.data)
#                     return redirect(url_for("blogging.page_by_id", post_id=pid,
#                                             slug=slug))
#                 else:
#                     flash("There were errors in blog submission", "warning")
#                     return render_template("blogging/editor.html", form=form,
#                                            post_id=post_id, config=config)
#             else:
#                 if post_id is not None:
#                     post = storage.get_post_by_id(post_id)
#                     if (post is not None) and \
#                             (PostProcessor.is_author(post, current_user)):
#                         tags = ", ".join(post["tags"])
#                         form = BlogEditor(title=post["title"],
#                                           text=post["text"], tags=tags)
#                         editor_get_fetched.send(blogging_engine.app,
#                                                 engine=blogging_engine,
#                                                 post_id=post_id,
#                                                 form=form)
#                         return render_template("blogging/editor.html",
#                                                form=form, post_id=post_id,
#                                                config=config)
#                     else:
#                         flash("You do not have the rights to edit this post",
#                               "warning")
#                         return redirect(url_for("blogging.index",
#                                                 post_id=None))
#
#             form = BlogEditor()
#             return render_template("blogging/editor.html", form=form,
#                                    post_id=post_id, config=config)
#     except PermissionDenied:
#         flash("You do not have permissions to create or edit posts", "warning")
#         return redirect(url_for("blogging.index", post_id=None))
#
#
# @login_required
# def delete(post_id):
#     blogging_engine = _get_blogging_engine(current_app)
#     cache = blogging_engine.cache
#     if cache:
#         _clear_cache(cache)
#     try:
#         with blogging_engine.blogger_permission.require():
#             storage = blogging_engine.storage
#             post = storage.get_post_by_id(post_id)
#             if (post is not None) and \
#                     (PostProcessor.is_author(post, current_user)):
#                 success = storage.delete_post(post_id)
#                 if success:
#                     flash("Your post was successfully deleted", "info")
#                     post_deleted.send(blogging_engine.app,
#                                       engine=blogging_engine,
#                                       post_id=post_id,
#                                       post=post)
#                 else:
#                     flash("There were errors while deleting your post",
#                           "warning")
#             else:
#                 flash("You do not have the rights to delete this post",
#                       "warning")
#             return redirect(url_for("blogging.index"))
#     except PermissionDenied:
#         flash("You do not have permissions to delete posts", "warning")
#         return redirect(url_for("blogging.index", post_id=None))
#
#
# def sitemap():
#     blogging_engine = _get_blogging_engine(current_app)
#     storage = blogging_engine.storage
#     config = blogging_engine.config
#     posts = storage.get_posts(count=None, offset=None, recent=True,
#                               user_id=None, tag=None, include_draft=False)
#     sitemap_posts_fetched.send(blogging_engine.app, engine=blogging_engine,
#                                posts=posts)
#
#     if len(posts):
#         for post in posts:
#             blogging_engine.process_post(post, render=False)
#         sitemap_posts_processed.send(blogging_engine.app,
#                                      engine=blogging_engine, posts=posts)
#     sitemap_xml = render_template("blogging/sitemap.xml", posts=posts,
#                                   config=config)
#     response = make_response(sitemap_xml)
#     response.headers["Content-Type"] = "application/xml"
#     return response
#
#
# def feed():
#     blogging_engine = _get_blogging_engine(current_app)
#     storage = blogging_engine.storage
#     config = blogging_engine.config
#     count = config.get("BLOGGING_FEED_LIMIT")
#     posts = storage.get_posts(count=count, offset=None, recent=True,
#                               user_id=None, tag=None, include_draft=False)
#
#     feed = AtomFeed(
#         '%s - All Articles' % config.get("BLOGGING_SITENAME",
#                                          "Flask-Blogging"),
#         feed_url=request.url, url=request.url_root, generator=None)
#
#     feed_posts_fetched.send(blogging_engine.app, engine=blogging_engine,
#                             posts=posts)
#     if len(posts):
#         for post in posts:
#             blogging_engine.process_post(post, render=True)
#             feed.add(post["title"], ensureUtf(post["rendered_text"]),
#                      content_type='html',
#                      author=post["user_name"],
#                      url=config.get("BLOGGING_SITEURL", "")+post["url"],
#                      updated=post["last_modified_date"],
#                      published=post["post_date"])
#         feed_posts_processed.send(blogging_engine.app, engine=blogging_engine,
#                                   feed=feed)
#     response = feed.get_response()
#     response.headers["Content-Type"] = "application/xml"
#     return response
#
#
# def unless(blogging_engine):
#     # disable caching for bloggers. They can change state!
#     def _unless():
#         return _is_blogger(blogging_engine.blogger_permission)
#     return _unless
#
#
# def cached_func(blogging_engine, func):
#     cache = blogging_engine.cache
#     if cache is None:
#         return func
#     else:
#         unless_func = unless(blogging_engine)
#         config = blogging_engine.config
#         cache_timeout = config.get("BLOGGING_CACHE_TIMEOUT", 60)  # 60 seconds
#         memoized_func = cache.memoize(
#             timeout=cache_timeout, unless=unless_func)(func)
#         return memoized_func
#
#
# def create_blueprint(import_name, blogging_engine):
#
#     blog_app = Blueprint("blogging", import_name, template_folder='templates')
#
#     # register index
#     index_func = cached_func(blogging_engine, index)
#     blog_app.add_url_rule("/", defaults={"count": None, "page": 1},
#                           view_func=index_func)
#     blog_app.add_url_rule("/<int:count>/", defaults={"page": 1},
#                           view_func=index_func)
#     blog_app.add_url_rule("/<int:count>/<int:page>/", view_func=index_func)
#
#     # register page_by_id
#     page_by_id_func = cached_func(blogging_engine, page_by_id)
#     blog_app.add_url_rule("/page/<post_id>/", defaults={"slug": ""},
#                           view_func=page_by_id_func)
#     blog_app.add_url_rule("/page/<post_id>/<slug>/",
#                           view_func=page_by_id_func)
#
#     # register posts_by_tag
#     posts_by_tag_func = cached_func(blogging_engine, posts_by_tag)
#     blog_app.add_url_rule("/tag/<tag>/", defaults=dict(count=None, page=1),
#                           view_func=posts_by_tag_func)
#     blog_app.add_url_rule("/tag/<tag>/<int:count>/", defaults=dict(page=1),
#                           view_func=posts_by_tag_func)
#     blog_app.add_url_rule("/tag/<tag>/<int:count>/<int:page>/",
#                           view_func=posts_by_tag_func)
#
#     # register posts_by_author
#     posts_by_author_func = cached_func(blogging_engine, posts_by_author)
#     blog_app.add_url_rule("/author/<user_id>/",
#                           defaults=dict(count=None, page=1),
#                           view_func=posts_by_author_func)
#     blog_app.add_url_rule("/author/<user_id>/<int:count>/",
#                           defaults=dict(page=1),
#                           view_func=posts_by_author_func)
#     blog_app.add_url_rule("/author/<user_id>/<int:count>/<int:page>/",
#                           view_func=posts_by_author_func)
#
#     # register editor
#     editor_func = editor  # For now lets not cache this
#     blog_app.add_url_rule('/editor/', methods=["GET", "POST"],
#                           defaults={"post_id": None},
#                           view_func=editor_func)
#     blog_app.add_url_rule('/editor/<post_id>/', methods=["GET", "POST"],
#                           view_func=editor_func)
#
#     # register delete
#     delete_func = delete  # For now lets not cache this
#     blog_app.add_url_rule("/delete/<post_id>/", methods=["POST"],
#                           view_func=delete_func)
#
#     # register sitemap
#     sitemap_func = cached_func(blogging_engine, sitemap)
#     blog_app.add_url_rule("/sitemap.xml", view_func=sitemap_func)
#
#     # register feed
#     feed_func = cached_func(blogging_engine, feed)
#     blog_app.add_url_rule('/feeds/all.atom.xml', view_func=feed_func)
#
#     return blog_app
