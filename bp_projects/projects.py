from flask import Blueprint, render_template

app_projects = Blueprint('projects', __name__,
                url_prefix='/projects',
                template_folder='templates/bp_projects/')

@app_projects.route('/portfolio/')
def portfolio():
    return render_template("portfolio.html")

@app_projects.route('/purpose-roles/')
def purposeAndRoles():
    return render_template("purposeAndRoles.html")