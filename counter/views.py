# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import requests
import pprint


from bs4 import BeautifulSoup
from .client import DiffbotClient,DiffbotCrawl
from .config import API_TOKEN
from urllib.parse import quote, unquote

from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.
class HomePage(TemplateView):
	template_name = 'index.html'


def results(request,query,pages):
	context = []
	results = {'availability': "", 'name': "", 'amount': "",'category': "", 'image': "",'link':""}
	url = 'https://www.google.co.in/search?q='
	user_agent = {'User-agent': 'Mozilla/5.0'}
	pages=int(pages)
	for i in range(pages):
		url = url + quote(query)+'&start='+str(i)+'0&sa=N'
		req = requests.get(url,headers=user_agent)
		soup = BeautifulSoup(req.content,'html.parser',from_encoding='utf-8')
		for link in soup.select('h3.r a'):
			print(link['href'])
			link = link['href'].split('q=')[1]
			link = re.split('&',link)[0]
			link = unquote(link)
			print (link)
			if link.startswith('http'):
				diffbot = DiffbotClient()
				token = API_TOKEN
				api = "analyze"
				try:
					response = diffbot.request(link, token, api)
					if response['objects'][0]['availability'] == "True":
						results['availability'] = "Unavailable"
					else:
						results['availability'] = "Available"

					# print (results['availability'])
					results['name'] = response['objects'][0]['title']
					try:
						results['amount'] = response['objects'][0]['offerPriceDetails']['text']
					except KeyError:
						try:
							results['amount'] = response['objects'][0]['regulaPriceDetails']['text']
						except KeyError	:
							results['amount'] = "NA"
					results['category'] = response['objects'][0]['category']
					try:
						results['image'] = response['objects'][0]['images'][0]['url']
					except Exception as e:
						results['image'] = "image not available"
					
					results['link'] = response['objects'][0]['pageUrl']
					context.append(results.copy())
				except:
					results['image'] = "image not available"
					results['category'] = ""
					results['name'] = "link only"
					results['link'] = link
					results['amount'] = ""
					results["availability"]= ""
					context.append(results.copy())
	context = {
		'objects':context
	}

	return render(request,'results.html',context=context)
