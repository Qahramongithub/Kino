import uvicorn

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
from db.modules import User, engine, Kino, Kanal
from web.provider import UsernameAndPasswordProvider

app = Starlette()

admin = Admin(engine, title="Example: SQLAlchemy",
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")],
              )

# Add view
admin.add_view(ModelView(User, icon='fas fa-users'))
admin.add_view(ModelView(Kino, icon='fas fa-film'))
admin.add_view(ModelView(Kanal, icon='fa fa-link'))

admin.mount_to(app)
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
