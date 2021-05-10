from django.shortcuts import render, redirect
from .models import *
import requests
# Create your views here.


def home(request):

    url = 'https://api.covid19india.org/data.json'
    data = ((requests.get(url)).json())
    dialy_confirmed = data['cases_time_series'][-1]['dailyconfirmed']
    dialy_deceased = data['cases_time_series'][-1]['dailydeceased']
    dialy_recovered = data['cases_time_series'][-1]['dailyrecovered']
    date = data['cases_time_series'][-1]['date']
    total_confirmed = data['cases_time_series'][-1]['totalconfirmed']
    total_deceased = data['cases_time_series'][-1]['totaldeceased']
    total_recovered = data['cases_time_series'][-1]['totalrecovered']
    yest_confirmed = data['cases_time_series'][-2]['dailyconfirmed']
    yest_deceased = data['cases_time_series'][-2]['dailydeceased']
    yest_recovered = data['cases_time_series'][-2]['dailyrecovered']

    last10_days = data['cases_time_series'][-9:]

    last10_days_dialy_confirmed = []
    last10_days_dialy_deceased = []
    last10_days_dialy_recovered = []
    last10_days_date = []

    for i in last10_days:
        last10_days_dialy_confirmed.append(int(i['dailyconfirmed']))
        last10_days_dialy_deceased.append(int(i['dailydeceased']))
        last10_days_dialy_recovered.append(int(i['dailyrecovered']))
        last10_days_date.append(i['date'])

    confirm_percentage = round(((int(dialy_confirmed) -
                                 int(yest_confirmed))/int(yest_confirmed))*100, 2)
    deceased_percentage = round(((int(dialy_deceased) -
                                  int(yest_deceased))/int(yest_deceased))*100, 2)

    recovered_percentage = round(((int(dialy_recovered) -
                                   int(yest_recovered))/int(yest_recovered))*100, 2)

    total_active = int(total_confirmed)-int(total_recovered)

    dsfc = len(data['cases_time_series'])

    dofc = data['cases_time_series'][0]['date']

    context = {'dofc': dofc, 'dsfc': dsfc, 'total_active': total_active, 'recovered_percentage': recovered_percentage, 'last10_days_dialy_confirmed': last10_days_dialy_confirmed, 'last10_days_dialy_deceased': last10_days_dialy_deceased, 'last10_days_dialy_recovered': last10_days_dialy_recovered, 'last10_days_date': last10_days_date, 'dialy_confirmed': dialy_confirmed, 'dialy_deceased': dialy_deceased, 'dialy_recovered': dialy_recovered,
               'date': date, 'total_confirmed': total_confirmed, 'total_deceased': total_deceased, 'total_recovered': total_recovered, 'confirm_percentage': confirm_percentage, 'deceased_percentage': deceased_percentage}

    return render(request, 'dashboard.html', context)


def state(request):

    url = 'https://api.covid19india.org/data.json'
    data = ((requests.get(url)).json())
    state_wise = data['statewise']

    state_name = []
    active = []
    confirmed = []
    recovered = []
    death = []

    for i in state_wise:
        if i['state'] == "Total":
            pass
        else:
            state_name.append(i['state'])
            active.append(i['active'])
            confirmed.append(i['deltaconfirmed'])
            recovered.append(i['deltarecovered'])
            death.append(i['deltadeaths'])

    state_wise_data = zip(state_name, active, confirmed, recovered, death)

    return render(request, 'tables.html', {'state_wise_data': state_wise_data})


def district(request, statename):

    url = 'https://api.covid19india.org/state_district_wise.json'
    data = ((requests.get(url)).json())

    district_wise = data[statename]['districtData']

    district_name = []
    active = []
    confirmed = []
    recovered = []
    death = []

    for key, value in district_wise.items():
        district_name.append(key)
        active.append(value['active'])
        confirmed.append(value['delta']['confirmed'])
        recovered.append(value['delta']['recovered'])
        death.append(value['delta']['deceased'])

    district_wise_data = zip(district_name, active,
                             confirmed, recovered, death)

    return render(request, 'district.html', {'statename': statename, 'district_wise_data': district_wise_data})
