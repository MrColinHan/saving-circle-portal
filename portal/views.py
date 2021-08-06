"""
Author: Colin Han
Date: July 4, 2021

Description:
    This Python program incorporates graphql queries which connect to the 'The Graph':
            https://thegraph.com/legacy-explorer/subgraph/mrcolinhan/saving-circle-subgraph
    It pulls data from our saving circle smart contract on the Celo blockchain:
            https://explorer.celo.org/address/0xD8D1E94A0DB2d6a3377744d97CE7d0Df52B66667/transactions
    And eventually feeds data to a web portal that uses chart.js to visualize data:
            https://github.com/MrColinHan/saving-circle-charts

    In addition, it also includes all necessary python functions such as Django login.
"""

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import pandas as pd
from django.shortcuts import render, redirect
import os
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import mimetypes
from django.http import HttpResponse
import copy

# Inputs ========================================================================================
graph_Api_url = 'https://api.thegraph.com/subgraphs/name/mrcolinhan/saving-circle-subgraph'
# ===============================================================================================

'''===Admin Login form function==='''
def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            # now log in the user
            user = login_form.get_user()
            login(request, user)
            return redirect('/main_page')
    else:
        login_form = AuthenticationForm()

    return render(request, 'portal/login.html', {'login_form': login_form})


'''===Admin Logout function==='''
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')


'''===redirect to django admin==='''
def goto_admin_view(request):
    return redirect('/admin')


def get_x_dayList(x):  # get a list of x days counting from today
    datetime_list = pd.date_range(end=datetime.today(), periods=x).to_pydatetime().tolist()
    result = list()
    for i in datetime_list:
        result.append(i.strftime('%m-%d-%y'))
    return result

'''===passing circle data to HTML==='''
@login_required(login_url="/")
def pass_python_data_toHTML(request):
    '''===connect to the queries http on The Graph==='''
    http_transport = RequestsHTTPTransport(
        url=graph_Api_url,
        verify=True,
        retries=5,
    )
    client = Client(
        transport=http_transport
    )

    '''===graphql queries ==='''
    graphql_query = gql('''
    query {
    circleCreatedEntities {
        id
        creator
        timeStamp
    }
    depositMadeEntities {
        id
        depositor
        circle
        amount
        timeStamp
    }
    loanRequestMadeEntities {
        id
        requester
        circle
        amount
        timeStamp
        granted
    }
    }
    ''')

    graphql_query_response = client.execute(graphql_query)


# =================================== save "circle" data to a dataframe ===================================
    '''===save "circle" data to a dataframe==='''
    print(f"====== Pulling Circle Data ======")
    circles_df = pd.DataFrame(columns=['circle address', 'creator address', 'timeStamp'])
    # print(f"{len(graphql_query_response['circleCreatedEntities'])} circles have been created: ")
    for circle in graphql_query_response['circleCreatedEntities']:
        circles_df.loc[len(circles_df)] = [circle['id'], circle['creator'],
                                           datetime.fromtimestamp(int(circle['timeStamp']))]
        # print(f"{circle['id']} ----- {circle['creator']} ----- {datetime.fromtimestamp(int(circle['timeStamp']))}")
    #print(circles_df)
    circles_df.to_csv("csv_files_fromPy/circles_created.csv")  # output circle dataframe to a csv file
    # === count number of circles by day
    circle_count_byDay_df = circles_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['circle address'].count()
    circle_count_byDay_df.to_frame().rename(columns={'circle address': 'count'}).to_csv(
        "csv_files_fromPy/circle_count_byDay.csv")  # output this df to a csv file

    circle_count_byMonth_df = circles_df.groupby(pd.Grouper(key='timeStamp', freq='M'))['circle address'].count()
    circle_count_byMonth_df.to_frame().rename(columns={'circle address': 'count'}).to_csv(
        "csv_files_fromPy/circle_count_byMonth.csv")  # output this df to a csv file


# =================================== save "deposit" data to a dataframe ===================================
    '''===save "deposit_made" data to a dataframe==='''
    print(f"====== Pulling Deposit_made Data ======")
    deposit_df = pd.DataFrame(columns=['id', 'depositor', 'circle', 'amount', 'timeStamp'])
    for deposit in graphql_query_response['depositMadeEntities']:
        deposit_df.loc[len(deposit_df)] = [deposit['id'],
                                           deposit['depositor'],
                                           deposit['circle'], deposit['amount'],
                                           datetime.fromtimestamp(int(deposit['timeStamp']))]
    #print(deposit_df)
    total_deposit_amount_dollar = deposit_df['amount'].astype(int).sum()
    deposit_df.to_csv("csv_files_fromPy/deposits_made.csv")  # save as a csv file
    # === count number of deposits each day
    deposit_count_byDay_df = deposit_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['id'].count()
    deposit_count_byDay_df.to_frame().rename(columns={'id': 'count'}).to_csv("csv_files_fromPy/deposit_count_byDay.csv")


# =================================== save "request" data to a dataframe ===================================
    '''===save "loan request" data to a dataframe==='''
    print(f"====== Pulling_request Data ======")
    request_df = pd.DataFrame(columns=['id', 'requester', 'circle', 'amount', 'timeStamp', 'granted'])
    for loan_request in graphql_query_response['loanRequestMadeEntities']:
        request_df.loc[len(request_df)] = [loan_request['id'],
                                           loan_request['requester'],
                                           loan_request['circle'], loan_request['amount'],
                                           datetime.fromtimestamp(int(loan_request['timeStamp'])),
                                           loan_request['granted']]
    # print(deposit_df)
    total_request_amount_dollar = request_df['amount'].astype(int).sum()
    request_df.to_csv("csv_files_fromPy/requests_made.csv")  # save as a csv file
    # === count number of requests each day
    request_count_byDay_df = request_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['id'].count()
    request_count_byDay_df.to_frame().rename(columns={'id': 'count'}).to_csv("csv_files_fromPy/request_count_byDay.csv")


# =================================== parse circle count data to chart.js ===================================
    '''===passing data to js==='''
    print(f"====== passing data to js ======")
    # convert circle datetime to str-date
    circle_created_dates_list = circle_count_byDay_df.to_frame().rename(columns={'circle address': 'count'}).index.to_list()
    str_circle_created_dates_list = list()  # all days
    for i in circle_created_dates_list:
        str_circle_created_dates_list.append(i.strftime('%m-%d-%y'))

    circle_dailyCount_list = circle_count_byDay_df.to_frame().rename(columns={'circle address': 'count'})['count'].to_list()

    # IMPORTANT
    circle_date_count_dict = dict(zip(str_circle_created_dates_list, circle_dailyCount_list))

    empty_30days_dict = dict.fromkeys(get_x_dayList(30), 0)
    empty_90days_dict = dict.fromkeys(get_x_dayList(90), 0)
    empty_365days_dict = dict.fromkeys(get_x_dayList(365), 0)

    # IMPORTANT
    circle_date_count_dict_30days = copy.deepcopy(empty_30days_dict)
    circle_date_count_dict_90days = copy.deepcopy(empty_90days_dict)
    circle_date_count_dict_365days = copy.deepcopy(empty_365days_dict)
    for k in circle_date_count_dict:
        circle_date_count_dict_30days[k] = circle_date_count_dict[k]
        circle_date_count_dict_90days[k] = circle_date_count_dict[k]
        circle_date_count_dict_365days[k] = circle_date_count_dict[k]

    # important
    '''NEED TO UPDATE THIS PART'''
    all_active_users_list = ['0xdfdfb95cfed85320ead3713daa4f4de1f7ca05ee']

# =================================== parse deposit count data to chart.js ===================================
    # convert deposit datetime to str-date
    deposit_created_dates_list = deposit_count_byDay_df.to_frame().rename(columns={'id': 'count'}).index.to_list()
    str_deposit_created_dates_list = list()  # all days
    for i in deposit_created_dates_list:
        str_deposit_created_dates_list.append(i.strftime('%m-%d-%y'))

    deposit_dailyCount_list = deposit_count_byDay_df.to_frame().rename(columns={'id': 'count'})['count'].to_list()

    # IMPORTANT
    deposit_date_count_dict = dict(zip(str_deposit_created_dates_list, deposit_dailyCount_list))

    # IMPORTANT
    deposit_date_count_dict_30days = copy.deepcopy(empty_30days_dict)
    deposit_date_count_dict_90days = copy.deepcopy(empty_90days_dict)
    deposit_date_count_dict_365days = copy.deepcopy(empty_365days_dict)
    for k in deposit_date_count_dict:
        deposit_date_count_dict_30days[k] = deposit_date_count_dict[k]
        deposit_date_count_dict_90days[k] = deposit_date_count_dict[k]
        deposit_date_count_dict_365days[k] = deposit_date_count_dict[k]



# =================================== parse request count data to chart.js ===================================
    # convert request datetime to str-date
    request_created_dates_list = request_count_byDay_df.to_frame().rename(columns={'id': 'count'}).index.to_list()
    str_request_created_dates_list = list()  # all days
    for i in request_created_dates_list:
        str_request_created_dates_list.append(i.strftime('%m-%d-%y'))

    request_dailyCount_list = request_count_byDay_df.to_frame().rename(columns={'id': 'count'})['count'].to_list()

    # IMPORTANT
    request_date_count_dict = dict(zip(str_request_created_dates_list, request_dailyCount_list))

    # IMPORTANT
    request_date_count_dict_30days = copy.deepcopy(empty_30days_dict)
    request_date_count_dict_90days = copy.deepcopy(empty_90days_dict)
    request_date_count_dict_365days = copy.deepcopy(empty_365days_dict)
    for k in request_date_count_dict:
        request_date_count_dict_30days[k] = request_date_count_dict[k]
        request_date_count_dict_90days[k] = request_date_count_dict[k]
        request_date_count_dict_365days[k] = request_date_count_dict[k]

# =================================== pass all data to chart.js ===================================
    pass_data = {
        'amount_of_circles': len(graphql_query_response['circleCreatedEntities']),
        'amount_of_users': len(all_active_users_list),

        'circle_created_dates_list': circle_date_count_dict.keys(),
        'circle_dailyCount_list': circle_date_count_dict.values(),
        '30days_circle_created_dates_list': circle_date_count_dict_30days.keys(),
        '30days_circle_dailyCount_list': circle_date_count_dict_30days.values(),
        '90days_circle_created_dates_list': circle_date_count_dict_90days.keys(),
        '90days_circle_dailyCount_list': circle_date_count_dict_90days.values(),
        '365days_circle_created_dates_list': circle_date_count_dict_365days.keys(),
        '365days_circle_dailyCount_list': circle_date_count_dict_365days.values(),

        'amount_of_deposits': len(graphql_query_response['depositMadeEntities']),
        'dollar_amount_of_deposits': total_deposit_amount_dollar,

        'deposit_created_dates_list': deposit_date_count_dict.keys(),
        'deposit_dailyCount_list': deposit_date_count_dict.values(),
        '30days_deposit_created_dates_list': deposit_date_count_dict_30days.keys(),
        '30days_deposit_dailyCount_list': deposit_date_count_dict_30days.values(),
        '90days_deposit_created_dates_list': deposit_date_count_dict_90days.keys(),
        '90days_deposit_dailyCount_list': deposit_date_count_dict_90days.values(),
        '365days_deposit_created_dates_list': deposit_date_count_dict_365days.keys(),
        '365days_deposit_dailyCount_list': deposit_date_count_dict_365days.values(),

        'amount_of_requests': len(graphql_query_response['loanRequestMadeEntities']),
        'dollar_amount_of_requests': total_deposit_amount_dollar,

        'request_created_dates_list': request_date_count_dict.keys(),
        'request_dailyCount_list': request_date_count_dict.values(),
        '30days_request_created_dates_list': request_date_count_dict_30days.keys(),
        '30days_request_dailyCount_list': request_date_count_dict_30days.values(),
        '90days_request_created_dates_list': request_date_count_dict_90days.keys(),
        '90days_request_dailyCount_list': request_date_count_dict_90days.values(),
        '365days_request_created_dates_list': request_date_count_dict_365days.keys(),
        '365days_request_dailyCount_list': request_date_count_dict_365days.values(),

        '30days_list': get_x_dayList(30),
        '90days_list': get_x_dayList(90),
        '365days_list': get_x_dayList(365)

    }
    return render(request, 'portal/main_page.html', pass_data)


def download_circle_file(request):
    f1_path = "csv_files_fromPy/circles_created.csv"
    f1 = open(f1_path, 'r')
    mime_type, _ = mimetypes.guess_type(f1_path)
    response = HttpResponse(f1, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=circles_created.csv"
    return response


def download_deposit_file(request):
    f1_path = "csv_files_fromPy/deposits_made.csv"
    f1 = open(f1_path, 'r')
    mime_type, _ = mimetypes.guess_type(f1_path)
    response = HttpResponse(f1, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=deposits_made.csv"
    return response

def download_request_file(request):
    f1_path = "csv_files_fromPy/requests_made.csv"
    f1 = open(f1_path, 'r')
    mime_type, _ = mimetypes.guess_type(f1_path)
    response = HttpResponse(f1, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=requests_made.csv"
    return response


