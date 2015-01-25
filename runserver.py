from email_service.factory import create_app
import os

if 'PRODUCTION_CHECK' in os.environ:
    application = create_app()
else:
    app = create_app()
    app.run()

