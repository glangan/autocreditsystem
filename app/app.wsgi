import os
import bottle
import sys
from bottle import route, run, template, request, static_file, redirect


sys.path.insert(0, "/var/www/app")
import main

os.chdir(os.path.dirname(__file__))


@route('/')
def index():
    return template('index')


@route('/compare_new', method='GET')
def compare():
	return template('compare_new')


@route('/compare_new', method='POST')
def results():
	utasunit = request.forms.get("utasunits")
	uni = request.forms.get("uni")
	code = request.forms.get("code")
	level = request.forms.get("level")
	description = request.forms.get("description")
	lo = request.forms.get("lo")
	
	result = main.get_recommendation(utasunit, level, description, lo)	
	message = ''
	if result[1] == 0:
		message = 'Not Similar'
	elif result[1] == 1:
		message = 'Cannot be decided'
	else:
		message = 'Similar'
	
	lo_results = main.compare_units(utasunit, lo, 'LO')
	lo_keywords = lo_results[1]
	
	main.save_history(utasunit, description, result, message, uni, code, lo, lo_keywords)
	
	if ((uni is not '') and (code is not '')):
		main.save_unit(utasunit, description, result, message, uni, code, lo, lo_keywords)

	return template('result', data=result, desc = description, message=message, lo=lo, lo_keywords = lo_keywords)

@route('/history')
def history():
	data = main.get_history()
	return template('history', data = data)


@route('/history/<id>')
def get_history(id):
	one_data = main.get_history_by_id(id)
	if 'LO' in one_data:
		lo = one_data['LO']
	else:
		lo = ''
	if 'lo_keywords' in one_data:
		lo_keywords = one_data['lo_keywords']
	else:
		lo_keywords = ''
	return template('result', data=one_data['Result'], desc = one_data['Description'], message = one_data['Message'], lo = lo, lo_keywords = lo_keywords)

@route('/units')
def units():
	data = main.get_units()
	return template('units', data = data)

@route('/units/<id>')
def get_unit(id):
        one_data = main.get_unit_by_id(id)
        if 'LO' in one_data:
                lo = one_data['LO']
        else:
                lo = ''
        if 'lo_keywords' in one_data:
                lo_keywords = one_data['lo_keywords']
        else:
                lo_keywords = ''
        return template('result', data=one_data['Result'], desc = one_data['Description'], message= one_data['Message'], lo = lo, lo_keywords = lo_keywords)


@route('/units/delete/<id>')
def delete_unit(id):
	main.delete_unit_by_id(id)
	redirect('/units')

@route('/history/delete/<id>')
def delete_history(id):
	main.delete_history_by_id(id)
	redirect('/history')

#for CSS files
@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./static')
application = bottle.default_app()
