"""
Created on 2021-01-08
This is a demo application for https://github.com/WolfgangFahl/pyFlaskBootstrap4
@author: wf
"""
import os

from fb4.app import AppWrap
from flask import render_template


class HelloWeb(AppWrap):
    '''
    a sample web application
    '''

    def __init__(self):
        '''
        Constructor
        '''
        os.getcwd()

        os.chdir('../templates')

        super().__init__(template_folder=os.getcwd())

        @self.app.route('/')
        def home():
            return self.home()

    def home(self):
        '''
        render the home page of the HelloWeb application
        '''

        html = render_template("bootstrap.html", title="what", content="abcd", error=None)
        return html


helloWeb=HelloWeb()
app=helloWeb.app


if __name__ == '__main__':
    parser=helloWeb.getParser("")
    args=parser.parse_args()
    helloWeb.optionalDebug(args)
    helloWeb.run(args)