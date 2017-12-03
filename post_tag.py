from flask import render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import tags, main, time, datetime


@app.route('/makePost', methods=['GET', 'POST'])
def makePost():
    content_name = request.form['content_name']
    file_path = request.form['file_path']
    public = request.form['ispublic']
    
    username = session['username']
    cursor = conn.cursor()
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    "need to save the image in the static folder"
    query = 'SELECT max(id) as postID FROM Content' #to get the id of this post
    cursor.execute(query)
    postID = cursor.fetchone()['postID']
    query = 'INSERT into Content (id, username, timest, file_path, content_name, public) values (%s, %s, %s, %s, %s)'
    cursor.execute(query, (postID, username, timest, file_path, content_name, public))
    
    if (public == '0'): #need to know which friendgroup to share it with if not public
        group_name = request.form['friendgroup']
        query = 'INSERT into share VALUES(postID, friend_group_name, username)'
        cursor.execute(query, (postID, group_name, username))
        conn.commit()
        cursor.close()
        return redirect(url_for('main'))


@app.route('/tagUser/<post_id>')
def tagUser(post_id):
    return render_template('tagUser.html', post_id = post_id)

@app.route('/tagUser/processing-<post_id>', methods=['GET', 'POST'])
def tagUserProcessed(post_id):
    username_taggee = request.form['username_taggee']
    
    username_tagger = session['username']
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    query = 'INSERT into tag (id, username_tagger, username_taggee, timest, status) values (%s, %s, %s, %s, %s)'
    cursor.execute(query, (post_id, username_tagger, username_taggee, timest, 0))
    conn.commit()
    cursor.close()
    return redirect(url_for('main'))