import os

from app import db, create_app

from app.models.user import User
from app.models.posts import Post, Tag, PostsTags
from app.models.roles import Role, UserRoles

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'UserRoles': UserRoles,
        'Post': Post,
        'Tag': Tag,
        'PostsTags': PostsTags,
    }


# this will allow function calls on Jinja2
@app.context_processor
def utility_processor():
    def check_ping(hostname):
        response = os.system("ping " + hostname + " -n 1")
        if response == 0:
            return True
        return False

    return dict(check_ping=check_ping)


# Used for SSL
# if __name__ == "__main__":
#     app.run(ssl_context='adhoc')


if __name__ == "__main__":
    app.run(debug=True,  port=5001)
