from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
import code
def index(request):
	return render(request, 'search/index.html')  


# def fetchInstructors(courses):
# 	startUrl = 'https://api.coursera.org/api/instructors.v1?ids='
# 	endUrl = '&includes=firstName,lastName&fields=firstName,lastName'
# 	for course in courses:
# 		instructorIds = course['instructorIds']
# 		comma_separated_instructorIds = ",".join(instructorIds)
# 		url = startUrl + comma_separated_instructorIds + endUrl
# 		instructors = requests.get(url)				
# 		instructors = instructors.json()
# 		instructors = instructors["elements"]
# 		list_of_instructorNames = list()
# 		for instructor in instructors:
# 			name = instructor['firstName'] + ' ' + instructor['lastName']
# 			list_of_instructorNames.append(name)
# 		course['instructorNames'] = list_of_instructorNames
# 		# code.interact(local=locals())
# 	return courses

# def fetchPartners(courses):
# 	startUrl = 'https://api.coursera.org/api/partners.v1?ids='
# 	for course in courses:
# 		partnerIds = course['partnerIds']
# 		comma_separated_partnerIds = ",".join(partnerIds)		
# 		url = startUrl + comma_separated_partnerIds
# 		partners = requests.get(url)
# 		partners = partners.json()
# 		partners = partners["elements"]
# 		list_of_partnerNames = list()		
# 		for partner in partners:
# 			name = partner['name']
# 			list_of_partnerNames.append(name)
# 		course['partnerNames'] = list_of_partnerNames
# 		# code.interact(local=locals())
# 	return courses	

def results(request):
	if 'query' in request.GET:
		message = 'You searched for: %r' % request.GET['query']
	else:
		message = 'Empty Form'
		return render( request, 'search/index.html')

	frontQuery = 'https://api.coursera.org/api/courses.v1?q=search&query='
	EndQuery = '&includes=instructorIds,partnerIds,partnerLogo&fields=instructorIds,partnerIds,partnerLogo'
	url =  frontQuery + request.GET['query'] + EndQuery
	try:
		response_dict = requests.get(url)
	except:
		return HttpResponse('<h1>No Internet Connection</h1>')		
	courses=response_dict.json()
	context = { 'courses': courses }
	return render(request, 'search/results.html' , context)
