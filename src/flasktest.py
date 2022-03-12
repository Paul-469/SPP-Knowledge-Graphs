import spacy
from corpus import location
from fb4.app import AppWrap
from fb4.sqldb import db
from flask_wtf import FlaskForm
from sqlalchemy import Column
import sqlalchemy.types as types
from flask import redirect,render_template, request, flash, Markup, url_for, abort
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

import dblpTable
from mergeTables import merge_tables


class Message2(db.Model):
    id = Column(types.Text, primary_key=True)
    text = Column(types.Text, nullable=False)
    author = Column(types.String(100), nullable=False)
    category = Column(types.String(100), nullable=False)
    draft = Column(types.Boolean, default=False, nullable=False)
    create_time = Column(types.Integer, nullable=False, unique=True)



class HelloWeb(AppWrap):
    '''
    a sample web application
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(host='localhost')

        AppWrap.addTemplatePath(self, "../templates")
        db.init_app(self.app)
        self.db = db

        self.app.secret_key = 'dev'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
        self.app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

        @self.app.before_first_request
        def before_first_request_func():
            self.initDB()

        @self.app.route('/table/<message_id>/view')
        def view_message(message_id):
            return self.message_view(message_id)

        @self.app.route('/table/<message_id>/edit')
        def edit_message(message_id):
            return self.message_edit(message_id)

        @self.app.route('/table/<message_id>/delete', methods=['POST'])
        def delete_message(message_id):
            return self.message_delete(message_id)


        @self.app.route('/table/<msg>', methods=['GET', 'POST'])
        def test_table(msg):
            print(msg)
            print(type(msg))
            return self.table(msg)


        @self.app.route('/table/', methods=['GET', 'POST'])
        def test_table1():
            return self.table1()

        @self.app.route('/')
        def home():
            return self.home()

    def initDB(self,limit=20):
        '''
        initialize the database
        '''
        self.db.drop_all()
        self.db.create_all()
        ll = location.LocationLookup()  # initialize locationlookup
        nlp = spacy.load("en_core_web_trf")  # run "python -m spacy download en_core_web_trf" if it fails.


        res = [dblpTable.buildFromRESTful(ll, nlp, 'HPCC')]
        list = [1]
        res = merge_tables(res,list)
        dictToMessages(res, self)

    def message_delete(self, message_id):
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return f'Message {message_id} has been deleted. Return to <a href="/table">table</a>.'
        return f'Message {message_id} did not exist and could therefore not be deleted. Return to <a href="/table">table</a>.'

    def message_edit(self, message_id):
        message = Message.query.get(message_id)
        if message:
            message.draft = not message.draft
            db.session.commit()
            return f'Message {message_id} has been edited by toggling draft status. Return to <a href="/table">table</a>.'
        return f'Message {message_id} did not exist and could therefore not be edited. Return to <a href="/table">table</a>.'

    def message_view(self, message_id):
        message = Message.query.get(message_id)
        if message:
            return f'Viewing {message_id} with text "{message.text}". Return to <a href="/table">table</a>.'
        return f'Could not view message {message_id} as it does not exist. Return to <a href="/table">table</a>.'

    def initMessages(self, limit=20):
        '''
        create an initial set of message with the given limit
        Args:
            limit(int): the number of messages to create
        '''

        for i in range(limit):
            m = Message(
                text='Test message {}'.format(i + 1),
                author='Author {}'.format(i + 1),
                category='Category {}'.format(i + 1),
                create_time=4321 * (i + 1)
            )
            if i % 4:
                m.draft = True
            self.db.session.add(m)
        self.db.session.commit()

    def table(self, msg):
        '''
        test table
        '''

        page = request.args.get('page', 1, type=int)
        pagination = Message.query.paginate(page, per_page=20)
        messages = pagination.items
        titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('draft', 'Draft'),
                  ('create_time', 'Create Time')]
        return render_template('table.html', messages=messages, titles=None)



    def home(self):
        '''
        render the home page of the HelloWeb application
        '''
        html = render_template("input.html", title="HelloWeb demo application",
                               content="Welcome to the Flask + Bootstrap4 Demo web application", form=ButtonForm(), error=None)
        return html

    def table1(self):
        '''
        render the home page of the HelloWeb application
        '''
        html = render_template("input.html", title="HelloWeb demo application",
                               content="Welcome to the Flask + Bootstrap4 Demo web application", form=ButtonForm(), error=None)
        return html


helloWeb = HelloWeb()
app = helloWeb.app


class LoginForm(FlaskForm):
    '''
    a form with username/password
    '''
    username = StringField('Username', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    rememberMe = BooleanField('Remember me')
    submit = SubmitField('Login')

class Message(db.Model):
    acronym = Column(types.String(100), primary_key=True)
    acronym2 = Column(types.String(100), nullable=True)
    ordinal = Column(types.String(100), nullable=True)
    year = Column(types.String(100), nullable=True)
    from_date = Column(types.String(100), nullable=True)
    to_date = Column(types.String(100), nullable=True)
    country = Column(types.String(100), nullable=True)
    region = Column(types.String(100), nullable=True)
    city = Column(types.String(100), nullable=True)
    gnd = Column(types.String(100), nullable=True)
    dblp = Column(types.String(100), nullable=True)
    wikicfpID = Column(types.String(100), nullable=True)
    or_id = Column(types.String(100), nullable=True)
    wikidata = Column(types.String(100), nullable=True)
    confref = Column(types.String(100), nullable=True)
    seriesAcronym = Column(types.String(100), nullable=True)
    title = Column(types.String(100), nullable=True)


class ButtonForm(FlaskForm):
    query = StringField('Query:', validators=[DataRequired(), Length(1, 20)])
    Search = SubmitField()



def dictToMessages(ldict, app):
    for x in range(1, len(ldict)):

        m = Message(
            acronym=ldict[x]['acronym'],
            acronym2=ldict[x]['acronym2'],
            ordinal=ldict[x]['ordinal'],
            year=ldict[x]['year'],
            country=ldict[x]['country'],
            from_date=ldict[x]['from'],
            to_date = ldict[x]['to'],
            region = ldict[x]['region'],
            city = ldict[x]['city'],
            gnd = ldict[x]['gnd'],
            dblp = ldict[x]['dblp'],
            wikicfpID = ldict[x]['wikicfpID'],
            or_id = ldict[x]['or'],
            wikidata = ldict[x]['wikidata'],
            confref = ldict[x]['confref'],
            seriesAcronym = ldict[x]['seriesAcronym'],
            title = ldict[x]['title'],
        )

        app.db.session.add(m)
    app.db.session.commit()


if __name__ == '__main__':
    parser = helloWeb.getParser("Flask + Bootstrap4 Demo Web Application")
    args = parser.parse_args()
    helloWeb.optionalDebug(args)
    helloWeb.run(args)