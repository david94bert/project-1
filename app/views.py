"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import datetime
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import AddProfile
from models import UserProfile
from werkzeug.security import check_password_hash

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

def date_created():
    now = datetime.datetime.now()
    return now.strftime("%c") 

@app.route('/profile', methods=['GET, POST'])
def profile():
    form = AddProfile()
    if form.methods == 'POST':
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            gender = form.gender.data
            email = form.email.data
            location = form.location.data
            bio = form.bio.data
            photo = form.photo.data
            dateCreated = date_created()
            
            filename = secure_filename(photo, filename)
            photo.save(os.path.join(app.config['UPLOAD FOLDER'], filename))
            
            userid = generateUserId(firstname, lastname)
            
            newUser = UserProfile(userid=userid, firstname=firstname, lastname=lastname, gender=gender, email=email, location=location, 
                        bio=bio, photo=photo, created_on=dateCreated)
                        
            db.session.add(newUser)
            db.session.commit()
            
            print("Successfully Operational")
            return redirect(url_for('profiles'))
            # return render_template(url_for('/profile/<userid>/'), firstname=firstname, lastname=lastname, 
            #                                         gender=gender, email=email, location=location, bio=bio, photo=photo)
        print("Not Successfully")
    return render_template('profile.html', form=form)
    
@app.route('/profiles/<userid>')
def profile():
    user = UserProfile.query.filter_by(userid=userid).first()
    return render_template('profile.html', userid=user)
    
@app.route('profiles', methods=["GET, POST"])
def profiles():
    userList = UserProfile.query.all()
    users = [{"First Name: ": user.firstname, "Last Name: ":user.lastname, "Userid: ": userid} for user in userList]
    
    if request.method == "POST":
        if userList is not None:
            respond = make_response(jsonify({"Users": users}))
            respond.headers["Content Type"] = 'application/join'
            return respond
        else:
            flash("No user Found")
            return redirect(url_for('home'))
    return render_template('profiles.html', user=userList)
    
def generateUserId(firstname, lastname):
    

# # Flash errors from the form if validation unseccessful
# def flash_errors(form):
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(u"Error in the %s field - %s" % (
#                 getattr(form, field).label.text,
#                 error
#             ), 'danger')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
