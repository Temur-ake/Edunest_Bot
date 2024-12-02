import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from login import UsernameAndPasswordProvider
from models import Contact, News, engine
from models import Course, User, Level

app = Starlette()

admin = Admin(engine, title="Example: SQLAlchemy",
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")],
              )

admin.add_view(ModelView(Contact, icon='fas fa-contacts'))
admin.add_view(ModelView(News, icon='fas fa-news'))
admin.add_view(ModelView(Course, icon='fas fa-course'))
admin.add_view(ModelView(User, icon='fas fa-user'))
admin.add_view(ModelView(Level, icon='fas fa-news'))

admin.mount_to(app)
if __name__ == '__main__':
    uvicorn.run(app, host="k.temur.life", port=8033)
