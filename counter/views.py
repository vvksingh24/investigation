# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import requests
import pprint


from bs4 import BeautifulSoup
from .client import DiffbotClient,DiffbotCrawl
from .config import API_TOKEN
from urllib.parse import quote

from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomePage(TemplateView):
	template_name = 'index.html'


def results(request,query):
	context = []
	results = {'availability': "", 'name': "", 'amount': "",'category': "", 'image': "",'link':""}
	url = 'https://www.google.co.in/search?q='
	user_agent = {'User-agent': 'Mozilla/5.0'}
	for i in range(4):
		url = url + quote(query)+'&start='+str(i)+'0&sa=N'
		req = requests.get(url,headers=user_agent)
		soup = BeautifulSoup(req.content,'html.parser',from_encoding='utf-8')
		for link in soup.select('h3.r a'):
			link = link['href'].split('q=')[1]
			link = re.split('&',link)[0]
			if link.startswith('http'):
				diffbot = DiffbotClient()
				token = API_TOKEN
				api = "analyze"
				response = diffbot.request(link, token, api)
				try:
					results['availability'] = response['objects'][0]['availability']
					# print (results['availability'])
					results['name'] = response['objects'][0]['title']
					try:
						results['amount'] = response['objects'][0]['offerPriceDetails']['text']
					except KeyError:
						try:
							results['amount'] = response['objects'][0]['regulaPriceDetails']['text']
						except KeyError	:
							results['amount'] = ""
					results['category'] = response['objects'][0]['category']
					try:
						results['image'] = response['objects'][0]['images'][0]['url']
					except Exception as e:
						results['image'] = "image not available"
					
					results['link'] = response['objects'][0]['pageUrl']
					print ("\nresults\n")
					print (results)
					context.append(results.copy())
				except:
					print (response)
			print ("\ncontext\n")
			print (context)
	context = {
		'objects':context
	}

	return render(request,'results.html',context=context)
