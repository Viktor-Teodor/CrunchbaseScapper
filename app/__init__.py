from flask import Flask, render_template
from app.config import Config
from app.forms import DetailsForm
from GetAllData import doStuff
app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=("GET","POST"))
@app.route("/index", methods=("GET","POST"))
def index():
    form = DetailsForm()

    if form.validate_on_submit():
        doStuff(form.description.data,
                form.headquarters.data,
                form.industry.data)

        return render_template('index.html', form=form, availableForDownload = True)
    return render_template('index.html', form = form, availableForDownload = False)