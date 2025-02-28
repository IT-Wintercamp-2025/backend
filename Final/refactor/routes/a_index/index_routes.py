from flask import render_template, Blueprint

# __name__ = "index"
index_blueprint = Blueprint("index", __name__, template_folder="templates")

@index_blueprint.route("/")
def home():
    return render_template("index.html")


@index_blueprint.route('/index')
def index():
    return render_template('index.html')


def register_routes(app):
    app.register_blueprint(index_blueprint)
