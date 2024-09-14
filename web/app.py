import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
import db
from .login import UsernameAndPasswordProvider

app = Starlette()

admin = Admin(db.models.engine, title="Example: SQLAlchemy",
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")],
              )

admin.add_view(ModelView(db.models.Contact, icon='fas fa-contacts'))
admin.add_view(ModelView(db.models.News, icon='fas fa-news'))

admin.mount_to(app)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8017)
