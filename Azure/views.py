from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
import json
from reportlab.pdfgen import canvas
import urllib2
# Create your views here.

def index(request):
    args = {}
    args.update(csrf(request))
    return render(request, 'predictive.html')

def analysis(request):
    args = {}
    args.update(csrf(request))
    return render(request, 'analysis.html')


def predict(request):
    if request.method == "POST":
        crime = request.POST.get('crime')
        year = request.POST.get('year')
        data_list = []
        data_list.append(year)
        data_list.append(crime)
        data_list.append(0)
        url = 'https://ussouthcentral.services.azureml.net/workspaces/8d93ec8e51c34fec918267f9c7b4f9d1/services/7ec401844ac8479cac344615ab94cb57/execute?api-version=2.0&details=true'
        api_key = 'tULo40ekhIxQr6s1Fz1lbCTDoWMz8sfUaiIeke4G4hyenQuR3vrdF73dJ7jPHD5aey435zMNMhTc2irYA/e+Tw==' # Replace this with the API key for the web service
        col = ["Year", "Crime Type", "Crime Rate"]
        return makeRequest(data_list,col, url, api_key)


def predictTimeFrame(request):
    if request.method == "POST":
        timeFrame = request.POST.get('shift')
        year = request.POST.get('year')
        crime = request.POST.get('crime')
        data_list = []
        data_list.append(timeFrame)
        data_list.append(year)
        data_list.append(crime)
        data_list.append(0)
        col = ["Shift", "Year", "Crime Type", "Crime Rate"]

    url = 'https://ussouthcentral.services.azureml.net/workspaces/8d93ec8e51c34fec918267f9c7b4f9d1/services/d948b3e8ff3945f793c1fe95c749d2b8/execute?api-version=2.0&details=true'
    api_key = 'l+CW1T/NB0n4jk81/RYP4qpMYfLYDD/IEQ7imJSb5dO3QL1My06XmU9ITHCWcTu1BlAksA97KiUaSI1Bo9l28A==' # Replace this with the API key for the web service

    return makeRequest(data_list,col, url, api_key)




## IS SE NECHAY JANA DANGEROUS HAI


def makeRequest(data_list, col, my_url, api):
    data =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": col,
                    "Values": [ data_list, ]
                },        },
            "GlobalParameters": {
}
    }

    body = str.encode(json.dumps(data))

    url = my_url
    api_key = api # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib2.Request(url, body, headers) 

    try:
        response = urllib2.urlopen(req)
        result = response.read()
    except urllib2.HTTPError, error:
        return HttpResponse("The request failed with status code: " + str(error.code))
    return HttpResponse(result)