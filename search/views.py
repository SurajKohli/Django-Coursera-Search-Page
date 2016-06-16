from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
import code
import pdb

# Create your views here.
# def index(request):
#     latest_question_list = ['suraj','kohli','delhi','noida','india']
#     output = '<br> '.join([q for q in latest_question_list])
#     return HttpResponse(output)

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'search/index.html', context) 

def index(request):
	return render(request, 'search/index.html')  


def fetchInstructors(courses):
	startUrl = 'https://api.coursera.org/api/instructors.v1?ids='
	endUrl = '&includes=firstName,lastName&fields=firstName,lastName'
	for course in courses:
		instructorIds = course['instructorIds']
		comma_separated_instructorIds = ",".join(instructorIds)
		url = startUrl + comma_separated_instructorIds + endUrl
		instructors = requests.get(url)				
		instructors = instructors.json()
		instructors = instructors["elements"]
		list_of_instructorNames = list()
		for instructor in instructors:
			name = instructor['firstName'] + ' ' + instructor['lastName']
			list_of_instructorNames.append(name)
		course['instructorNames'] = list_of_instructorNames
		# code.interact(local=locals())
	return courses

def fetchPartners(courses):
	startUrl = 'https://api.coursera.org/api/partners.v1?ids='
	for course in courses:
		partnerIds = course['partnerIds']
		comma_separated_partnerIds = ",".join(partnerIds)		
		url = startUrl + comma_separated_partnerIds
		partners = requests.get(url)
		partners = partners.json()
		partners = partners["elements"]
		list_of_partnerNames = list()		
		for partner in partners:
			name = partner['name']
			list_of_partnerNames.append(name)
		course['partnerNames'] = list_of_partnerNames
		# code.interact(local=locals())
	return courses	

def results(request):
	if 'query' in request.GET:
		message = 'You searched for: %r' % request.GET['query']
	else:
		message = 'Empty Form'
		return render( request, 'search/index.html')

	# url = 'https://api.coursera.org/api/courses.v1?q=search&query=' + request.GET['query']
	frontQuery = 'https://api.coursera.org/api/courses.v1?q=search&query='
	EndQuery = '&includes=instructorIds,partnerIds,partnerLogo&fields=instructorIds,partnerIds,partnerLogo'
	url =  frontQuery + request.GET['query'] + EndQuery
	try:
		response_dict = requests.get(url)
	except:
		return HttpResponse('<h1>No Internet Connection</h1>')		
	# r = response_dict.content
	# r = json.loads(response_dict.content)
	courses=response_dict.json()
	# courses=courses["elements"]
	# courses = courses.json()
	# updated_instructors_courses = fetchInstructors(courses)
	# updated_partners_courses = fetchPartners(updated_instructors_courses)
	# code.interact(local=locals())	
	# context = { 'courses': updated_partners_courses }
	context = { 'courses': courses }
	return render(request, 'search/results.html' , context)
	# return HttpResponse(response_dict)
