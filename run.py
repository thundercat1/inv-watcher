#!/home/mch/.virtualenvs/mega/bin/python
from app import app

#If you want profiling, uncomment this stuff
#from werkzeug.contrib.profiler import ProfilerMiddleware
#app.config['PROFILE'] = True
#app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

app.run(debug=True, host='0.0.0.0')
