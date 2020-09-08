from flask import Blueprint, redirect, url_for,render_template, flash, session, request
from flask_login import login_user, current_user, logout_user, login_required
from mywords.words.forms import AddWord, EditWord
from mywords import db
from mywords.models import Words
# other import
from PyDictionary import PyDictionary

dictionary = PyDictionary()

words = Blueprint("words",__name__)


@words.route("/add word", methods=['GET', 'POST'])
@login_required
def add_word():
	session["page"] = "addword"	
	form = AddWord()
	if form.add_word.data:
		print(session["worddata"])
		word_data = session["worddata"]
		#word=form.get_word.data
		word = session["word"]
		#def __init__(self, user_id, word, word_data, comment):
		add_word = Words(current_user.id,word,word_data, form.comment.data.strip())
		db.session.add(add_word)
		db.session.commit()
		session["worddata"]="No data"
		session["word"] = "No data"
		flash("Word added successfully!!")
		form.get_word.data = ""
		return render_template("addword.html", form=form, search=False)
	if form.validate_on_submit():		
		word = form.get_word.data.lower()
		word_data = ""				
		current_words = Words.query.filter_by(user_id=current_user.id,word=word).all()
		if current_words:
			current_word = current_words[0]
			word_data = current_word.word_data.split("*_*")[0]
			synonyms = current_word.word_data.split("*_*")[1]
			word_there = True
			return render_template("addword.html",  word_there=word_there, form=form, search=True, word=current_word.word.capitalize(), word_data=word_data,synonyms=synonyms )
		meaning = dictionary.meaning(word)
		word_there = False	
		keys=list(meaning.keys())
		word_data=""
		for key in keys:
			word_data=word_data+str(key)+": "
			for line in meaning[str(key)]:
				word_data=word_data+str(line)+","
			word_data = word_data[:-2]+"."
			word_data = word_data+ "\n"

		syn = dictionary.synonym(word)
		synonyms = ""
		for ele in syn:
			synonyms = synonyms +", "+ele
		synonyms=synonyms[1:]
		synonyms = "Synonyms: "+synonyms
		session["worddata"]=word_data+"*_*"+synonyms
		session["word"]=word
		return render_template("addword.html", word_there=word_there, form=form, search=True, word=word.capitalize(), word_data=word_data,synonyms=synonyms )
	return render_template("addword.html", form=form)

@words.route("/my words", methods=['GET', 'POST'])
@login_required
def my_words():	
	rule = request.url_rule
	print(rule)
	session["page"] = "mywords"
	page = request.args.get('page', 1, type=int)	
	words  = Words.query.filter_by(user_id=current_user.id)
	words = words.paginate(page=page, per_page=10)
	return render_template("mywords.html",words=words, query="")

@words.route("/edit word/<word>", methods=['GET', 'POST'])
@login_required
def edit_word(word):
	session['page']="editword"
	form = EditWord()
	word  = Words.query.filter_by(id=word).first()
	#form.new_comment.data=word.comment
	if form.validate_on_submit():

		updated_comment = form.new_comment.data.strip()
		print(form.new_comment.data)
		word.comment = updated_comment
		db.session.add(word)
		db.session.commit()
		words  = Words.query.filter_by(user_id=current_user.id).all()
		return redirect(url_for("words.my_words", words=words))
	elif request.method == 'GET':
		form.new_comment.data=word.comment
		
	return render_template("editword.html",word=word, form=form)

@words.route("/delete word/<word>", methods=['GET', 'POST'])
@login_required
def delete_word(word):
	word  = Words.query.filter_by(user_id=current_user.id,id=word).all()
	db.session.delete(word)
	db.session.commit()
	return redirect(url_for("words.my_words"))

@words.route("/search", methods=['GET', 'POST'])
@login_required
def search_word():	
	rule = str(request.url_rule)[1:]
	print(rule)
	page = request.args.get('page', 1, type=int)	
	words  = Words.query.filter_by(user_id=current_user.id)
	words = words.paginate(page=page, per_page=10)
	filter = []
	query = request.form.get("search")
	if query == "":
		return redirect(url_for("words.my_words"))
	#print(query)
	#print(type(words))
	for word in words.items:
		if query in word.word.lower():
			filter.append(word)
	print(len(filter))
	return render_template("mywords.html",words=words, query=query,no_of_words=(len(filter)),page=rule)

@words.route("/wordofday/<word>", methods=['GET', 'POST'])
@login_required
def wordofday(word):

	current_words = Words.query.filter_by(user_id=current_user.id,word=word).all()
	print(current_words)
	if current_words:	
			flash("word already present")
			return redirect(url_for("users.user"))
	session["page"] = "wordofday"	
	print(session["worddata"])
	word_data = session["worddata"]
	#word=form.get_word.data
	word = session["word"]
	#def __init__(self, user_id, word, word_data, comment):
	#add_word = Words(current_user.id,word.lower(),word_data, form.comment.data.strip())
	db.session.add(add_word)
	db.session.commit()
	session["worddata"]="No data"
	session["word"] = "No data"
	flash("Word added successfully!!")
	form.get_word.data = ""
	return redirect(url_for("users.user"))




@words.route("/profile")
@login_required
def profile():
	no_of_words = Words.query.filter_by(user_id=current_user.id).all()
	no_of_words = len(no_of_words)
	return render_template("profile.html", no_of_words=no_of_words)