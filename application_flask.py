""" 
1. The flask MODULE render_template as its name suggests, well...renders a template
   the template can be found in the /templates subdirectory

2. The flask MODULE request alows us to manage several type of requests (methods)
   Here we will use only two type of requests (methods): GET and POST:
  	  * GET should be used when no user-information is being used to produce the page
  	  *	POST should be used when the user is sending information to the server before 
			 a page is returned

3. The flask MODULE redirect as its name suggests redirects the application
    to another page
"""


from flask import Flask,render_template,request,redirect

# Create the Flask object
app_simpleApp = Flask(__name__)


# The object Flask() allows setting dictionaries to collect information from the user
# We set an empty dictonary that will collect name and age of user.
app_simpleApp.vars={}

# We set another dictionary for the questions asked in the form that will be displayed 
# in the web application
app_simpleApp.questions={}

# We populate the dictionary with questions and options
app_simpleApp.questions['How many eyes do you have?']=('1','2','3')
app_simpleApp.questions['Which fruit do you like best?']=('banana','mango','pineapple')
app_simpleApp.questions['Do you like cupcakes?']=('yes','no','maybe')

# We get the number of questions from the length of the dictionary
app_simpleApp.nquestions=len(app_simpleApp.questions)


@app_simpleApp.route('/index_simpleApp',methods=['GET','POST'])
# The app will be launched at 127.0.0.1:5000/index_simpleApp
def index_simpleApp():

	"""
	This function displays the corresponding HTML page that presents
	the survey and its questions. It also stores the answers provided
	by the user into a txt file
	"""

	# The number questions, nquestions, is gotten from the previous
	# app_simpleApp.nquestions
	nquestions = app_simpleApp.nquestions
	# Recall that GET should be used when no user-information is being sent to produce a page
	# If that is the case...
	if request.method == 'GET':
		# ... render_template looks for the HTML template in the /template subdirectory
		# The HTML code stored in 'userinfo_simpleApp.html' invokes, in turn, the format
		# style_simpleApp.css stored in the /static subdirectory.
		return render_template('userinfo_simpleApp.html',num=nquestions)
	# Also recall that if we use POST when the user is sending information to the server before
	# a page is return. Since the user will be sending name and age we use it now.
	elif request.method == 'POST':
		# Request was a POST and collect 'name' and 'age' from the user
		# The variables 'name_simpleApp' and 'age_simpleApp' on the right-hand side of
		# the next two lines are used in the HTML code 'userinfo_simpleApp.html' found in 
		# the /templates subdirectory. Such a HTML allows collecting such information 
		# from the user.

		# The left-hand side of such lines correspond to the Python dictionary set 
		# at the begining of this code
		app_simpleApp.vars['name'] = request.form['name_simpleApp']
		app_simpleApp.vars['age'] = request.form['age_simpleApp']

		# After the user has provided the requested info, we open a txt file with the name
		# and age of user. For instance Batman_45.txt ...
		f = open('%s_%s.txt'%(app_simpleApp.vars['name'],app_simpleApp.vars['age']),'w')
		# ... and write to it the name and age of user:
		# Name: Batman
		# Age: 45
		f.write('Name: %s\n'%(app_simpleApp.vars['name']))
		f.write('Age: %s\n\n'%(app_simpleApp.vars['age']))
		# File is closed
		f.close()

		# redirect function in Flask allows a decorated function 
		# (a function with @app_simpleApp.route('/index_simpleApp') 
		# or similar preceding the function) to return the HTML template that 
		# another function will produce. 
		# Instead of calling render_template to make an HTML page, we call redirect 
		# and insert the URL for another decorator function, 
		# which will call that decorated function and return the associated HTML code.
		return redirect('/main_simpleApp')

# This is the function called by the 'redirect' statement provided by the 
# previous function
@app_simpleApp.route('/main_simpleApp')
def main_simpleApp():

	"""
	This function presents the HTML page corresponding to the end of the
	survey
	"""
	# If there are no questions left in the survey then present (render_template)
	# the end of the survey. The HTML code corresponding to the end of the 
	# survey is found in 'end_simpleApp.html' and found in the \templates
	# subdirectory.
	if len(app_simpleApp.questions)==0 : return render_template('end_simpleApp.html')
	# In case there are still questions left we redirect to the template containing 
	# next question in the survey
	# IMPORTANT.- 'nextQ_simpleApp' is referred in the 'action' field found in the
	#			  'layout_simpleApp.html' HTML file found in the subdirectory /templates

	# It finally redirects to the next question, which is managed by the next function
	return redirect('/nextQ_simpleApp')

@app_simpleApp.route('/nextQ_simpleApp',methods=['GET','POST'])
def nextQ_simpleApp(): 
	"""
	This function manages the next question in the survey provided to the
	user
	"""
	# Remember GET is used when no user-information is being used to produce the page
	# while POST is used when the user is sending information to the server before 
	# a page is returned

	# When the question in turn is shown to the user...
	if request.method == 'GET':
		# We update the number of the question in turn
		n = app_simpleApp.nquestions - len(app_simpleApp.questions) + 1
		# Grab the question itself and save it to question_
		# Notice that question_ is used in the render to be displayed through the 
		# 'layout_simpleApp.html' HTML code
		question_ = app_simpleApp.questions.keys()[0] 
		# The options corresponding to such a question are also stored
		a1, a2, a3 = app_simpleApp.questions.values()[0] 
		# And save the current question key
		app_simpleApp.currentq = question_

		# We render the tempplate to show the question in the template
		return render_template('layout_simpleApp.html',num=n,question=question_,ans1=a1,ans2=a2,ans3=a3)

	# When the answers to the question in turn are going to be sent ...
	elif request.method == 'POST':
		# We collect data from the user.
		# Then, we return to the main function, so it can tell us whether to
		# display another question page, or to show the end page.

		# Open the text file and append (a is for append) ...
		f = open('%s_%s.txt'%(app_simpleApp.vars['name'],app_simpleApp.vars['age']),'a') 
		# ... the question shown in the page ...
		f.write('%s\n'%(app_simpleApp.currentq))
		# ... as well as the corresponding answer
		# 'answer_from_layout_simpleApp' is used in 'layout_simpleApp.html' HTML code 
		# contained in the /template subdirectory
		f.write('%s\n\n'%(request.form['answer_from_layout_simpleApp'])) 
		# Close file
		f.close()

		# Remove current question from dictionary
		del app_simpleApp.questions[app_simpleApp.currentq]

		# Finally redirect to main_simpleApp; it will check if there are any questions
		# left in the survey.
		return redirect('/main_simpleApp')


if __name__ == "__main__":
	# Run the code
	app_simpleApp.run(debug=True)
