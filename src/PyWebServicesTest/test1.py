'''
Created on Jul 16, 2012

@author: leal
'''


import web

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
        if not name: 
            name = 'world'
        return '<h1>Hello, ' + name + '!</h1>\n'

if __name__ == "__main__":
    app.run()
