from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, validators


class AddWord(FlaskForm):
	get_word = StringField("Enter word: ")
	back = SubmitField("Back")
	comment = TextAreaField("Notes", [validators.Length(min=0, max=300)])
	search_word = SubmitField("Search word")
	add_word = SubmitField("Add word")

class EditWord(FlaskForm):
	new_comment = TextAreaField("Enter new comment: ", [validators.Length(min=0, max=300)])
	update_comment = SubmitField("Update notes")