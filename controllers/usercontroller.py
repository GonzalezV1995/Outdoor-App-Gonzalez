from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.activities import Activites
from flask_app.models.user import User

# main page that gives you option to write a comment 
@app.route('/userdashboard')
def userdashboard():
    
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_id(
        {
        'id': session['user_id']
        }
    )

    comment = Activites.get_all()
    return render_template('userdashboard.html', user=user,comment=comment)

@app.route('/new_comment')
def new_comment():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('add_comment.html')


@app.route('/add_comment', methods=['POST'])
def add_comment():
    
    Activites.save(
        {
        'user_id': session['user_id'],
        'location': request.form['location'],
        'description': request.form['description'],
        } 
    )
    
    if 'user_id' not in session:
        return redirect('/')
    if not Activites.validate_comment(request.form):
        return redirect('/new_comment')
    return redirect('/comment_list')

@app.route('/comment_list')
def comment_list():
    
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_id(
        {
        'id': session['user_id']
        }
    )
    comment = Activites.get_all()
    return render_template('commentlist.html',comments=comment, user=user)


@app.route('/edit_comment/<int:id>')
def edit_comment(id):
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_id(
        {
        'id': session['user_id']
        }
    )
    comment = Activites.get_id( { 'id': id } )
    return render_template('editcomments.html',comment=comment, user=user)

@app.route('/update_comment/<int:id>', methods=['POST'])
def update_comment(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Activites.validate_comment(request.form):
        return redirect('/edit_comment/<int:id>')

    comment_data = {
        
        'id' : id,
        'user_id': session['user_id'],
        'location': request.form['location'],
        'description': request.form['description'],
        
    }
    Activites.update_comment(comment_data)
    return redirect('/comment_list')

@app.route('/view_comment/<int:comment_id>')
def view_comment(comment_id):
    data ={
        "id" : comment_id
    }
    user_data = {
        "id" :session['user_id']
    }
    user=User.get_id(user_data)
    comment=Activites.get_id(data)
    return render_template('view_comment.html', user=user, comment=comment)

@app.route('/delete_comment/<int:id>')
def delete_comment(id):
    if 'user_id' not in session:
        return redirect('/')

    Activites.delete_comment({'id':id})
    return redirect('/comment_list')