from flask import (Flask, render_template, redirect, url_for,
					abort, flash, g)


import models
import forms


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


app = Flask(__name__)
app.secret_key = 'sSGqw6217@#]2skJ8nmashShbh4587s#4FSs32d3#*&[]'


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    # g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
def index():
	"""Homepage & List all entries"""
	entries = models.Entry.select().limit(5)
	return render_template('entries.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def new_entry():
	"""Create new entry"""
	form = forms.JournalEntryForm(csrf_enabled=False)
	if form.validate_on_submit():
		models.Entry.create(title=form.title.data,
							date=form.date.data,
							timespent=form.timespent.data,
                           content=form.content.data.strip(),
                           resources=form.resources.data.strip())
		return redirect(url_for('index'))
	return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def view_entry(id):
	"""View a specific entry"""
	try:
		post = models.Entry.get(models.Entry.entry_id == id)
	except models.DoesNotExist:
		abort(404)
	return render_template('detail.html', post=post)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit_entry(id):
	"""Edit or update an entry"""
	try:
		post = models.Entry.get(models.Entry.entry_id == id)
		print(post.entry_id)
	except models.DoesNotExist:
		abort(404)

	form = forms.JournalEntryForm(csrf_enabled=False)

	if form.validate_on_submit():
		post.title = form.title.data
		post.date = form.date.data
		post.timespent = form.timespent.data
		post.content = form.content.data.strip()
		post.resources = form.resources.data.strip()
		post.save()
		return redirect(url_for('index'))

	return render_template('edit.html', form=form, post=post)


@app.route('/entries/<int:id>/delete')
def delete_entry(id):
	"""Delete an entry"""
	entry = models.Entry.get(models.Entry.entry_id == id)
	entry.delete_instance()
	return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, host=HOST, port=PORT)
