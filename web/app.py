import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
import itsdangerous
from starlette_admin.contrib.sqla import Admin, ModelView

from db.models import Contact, engine, News
from web.login import UsernameAndPasswordProvider

app = Starlette()

admin = Admin(engine, title="Example: SQLAlchemy",
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")],
              )

admin.add_view(ModelView(Contact, icon='fas fa-contacts'))
admin.add_view(ModelView(News, icon='fas fa-news'))

admin.mount_to(app)
if __name__ == '__main__':
    uvicorn.run(app, host="0", port=8017)
