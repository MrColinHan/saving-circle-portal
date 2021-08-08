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

import csv
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

# =================================== global variables: track all active users and circles ===================================

all_active_users_dict = dict() # keep track all activities within each user

all_active_circles_dict = dict()  # keep track all activities within each circle


'''===passing circle data to HTML==='''
@login_required(login_url="/")
def pass_python_data_toHTML(request):

    global all_active_users_dict, all_active_circles_dict

    # reset
    all_active_circles_dict = dict()
    all_active_users_dict = dict()

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
        circles_df.loc[len(circles_df)] = [circle['id'], circle['creator'], datetime.fromtimestamp(int(circle['timeStamp']))]

        # initiate this circle, record this activity as a inner list
        all_active_circles_dict[circle['id']] = [['created circle',
                                                 datetime.fromtimestamp(int(circle['timeStamp'])), circle['creator']]]

        # track this user, record this activity
        if circle['creator'] not in all_active_users_dict:  # if this is a new user, initiate tracking
            all_active_users_dict[circle['creator']] = [
                ['created circle', datetime.fromtimestamp(int(circle['timeStamp'])), circle['id']]]
        else:  # this user is already in the system, append this activity
            all_active_users_dict[circle['creator']].append(
                ['created circle', datetime.fromtimestamp(int(circle['timeStamp'])), circle['id']])


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

        # record this activity
        # make sure this circle exists
        if deposit['circle'] not in all_active_circles_dict:
            all_active_circles_dict[deposit['circle']] = [
                ['deposit made', datetime.fromtimestamp(int(deposit['timeStamp'])), deposit['depositor'],
                 deposit['amount']]]
        else:  # circle existed
            all_active_circles_dict[deposit['circle']].append(
                ['deposit made', datetime.fromtimestamp(int(deposit['timeStamp'])), deposit['depositor'],
                 deposit['amount']])

        # track this user, record this activity
        if deposit['depositor'] not in all_active_users_dict:  # if this is a new user, initiate tracking
            all_active_users_dict[deposit['depositor']] = [
                ['deposit made', datetime.fromtimestamp(int(deposit['timeStamp'])), deposit['circle'],
                 deposit['amount']]]
        else:  # this user is already in the system, append this activity
            all_active_users_dict[deposit['depositor']].append(
                ['deposit made', datetime.fromtimestamp(int(deposit['timeStamp'])), deposit['circle'],
                 deposit['amount']])

    total_deposit_amount_dollar = deposit_df['amount'].astype(int).sum()
    deposit_df.to_csv("csv_files_fromPy/deposits_made.csv")  # save as a csv file
    # === count number of deposits each day ===
    deposit_count_byDay_df = deposit_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['id'].count()
    deposit_count_byDay_df.to_frame().rename(columns={'id': 'count'}).to_csv("csv_files_fromPy/deposit_count_byDay.csv")

    # === total dollar amount of deposit each day ===
    deposit_df['amount'] = deposit_df['amount'].astype(float) # change string to float in order to do sum
    deposit_amount_byDay_df = deposit_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['amount'].sum()
    deposit_amount_byDay_df.to_frame().rename(columns={'amount': 'sum'}).to_csv("csv_files_fromPy/deposit_amount_byDay.csv")

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

        # record this activity
        # make sure this circle exists
        if loan_request['circle'] not in all_active_circles_dict:
            all_active_circles_dict[loan_request['circle']] = [['loan requested',
                                                                datetime.fromtimestamp(int(loan_request['timeStamp'])),
                                                                loan_request['requester'], loan_request['amount']]]
        else:  # circle existed
            all_active_circles_dict[loan_request['circle']].append(['loan requested',
                                                                    datetime.fromtimestamp(
                                                                        int(loan_request['timeStamp'])),
                                                                    loan_request['requester'], loan_request['amount']])

        # track this user, record this activity
        if loan_request['requester'] not in all_active_users_dict:  # if this is a new user, initiate tracking
            all_active_users_dict[loan_request['requester']] = [
                ['deposit made',
                 datetime.fromtimestamp(int(loan_request['timeStamp'])), loan_request['circle'],
                 loan_request['amount']]]
        else:  # this user is already in the system, append this activity
            all_active_users_dict[loan_request['requester']].append(
                ['deposit made',
                 datetime.fromtimestamp(int(loan_request['timeStamp'])), loan_request['circle'],
                 loan_request['amount']])

    # print(deposit_df)
    total_request_amount_dollar = request_df['amount'].astype(int).sum()
    request_df.to_csv("csv_files_fromPy/requests_made.csv")  # save as a csv file
    # === count number of requests each day
    request_count_byDay_df = request_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['id'].count()
    request_count_byDay_df.to_frame().rename(columns={'id': 'count'}).to_csv("csv_files_fromPy/request_count_byDay.csv")

    # === total dollar amount of request each day ===
    request_df['amount'] = request_df['amount'].astype(float)  # change string to float in order to do sum
    request_amount_byDay_df = request_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['amount'].sum()
    request_amount_byDay_df.to_frame().rename(columns={'amount': 'sum'}).to_csv(
        "csv_files_fromPy/request_amount_byDay.csv")


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
    empty_7days_dict = dict.fromkeys(get_x_dayList(7), 0)

    # IMPORTANT
    circle_date_count_dict_30days = copy.deepcopy(empty_30days_dict)
    circle_date_count_dict_90days = copy.deepcopy(empty_90days_dict)
    circle_date_count_dict_7days = copy.deepcopy(empty_7days_dict)
    for k in circle_date_count_dict:
        if k in circle_date_count_dict_30days:
            circle_date_count_dict_30days[k] = circle_date_count_dict[k]
        if k in circle_date_count_dict_90days:
            circle_date_count_dict_90days[k] = circle_date_count_dict[k]
        if k in circle_date_count_dict_7days:
            circle_date_count_dict_7days[k] = circle_date_count_dict[k]

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
    deposit_date_count_dict_7days = copy.deepcopy(empty_7days_dict)
    for k in deposit_date_count_dict:
        if k in deposit_date_count_dict_30days:
            deposit_date_count_dict_30days[k] = deposit_date_count_dict[k]
        if k in deposit_date_count_dict_90days:
            deposit_date_count_dict_90days[k] = deposit_date_count_dict[k]
        if k in deposit_date_count_dict_7days:
            deposit_date_count_dict_7days[k] = deposit_date_count_dict[k]

# =================================== parse deposit Amount data to chart.js ===================================

    deposit_dailyAmount_list = deposit_amount_byDay_df.to_frame().rename(columns={'amount': 'sum'})['sum'].to_list()

    # IMPORTANT
    deposit_date_amount_dict = dict(zip(str_deposit_created_dates_list, deposit_dailyAmount_list))

    # IMPORTANT
    deposit_date_amount_dict_30days = copy.deepcopy(empty_30days_dict)
    deposit_date_amount_dict_90days = copy.deepcopy(empty_90days_dict)
    deposit_date_amount_dict_7days = copy.deepcopy(empty_7days_dict)
    for k in deposit_date_amount_dict:
        if k in deposit_date_amount_dict_30days:
            deposit_date_amount_dict_30days[k] = deposit_date_amount_dict[k]
        if k in deposit_date_amount_dict_90days:
            deposit_date_amount_dict_90days[k] = deposit_date_amount_dict[k]
        if k in deposit_date_amount_dict_7days:
            deposit_date_amount_dict_7days[k] = deposit_date_amount_dict[k]


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
    request_date_count_dict_7days = copy.deepcopy(empty_7days_dict)
    for k in request_date_count_dict:
        if k in request_date_count_dict_30days:
            request_date_count_dict_30days[k] = request_date_count_dict[k]
        if k in request_date_count_dict_90days:
            request_date_count_dict_90days[k] = request_date_count_dict[k]
        if k in request_date_count_dict_7days:
            request_date_count_dict_7days[k] = request_date_count_dict[k]

# =================================== parse deposit Amount data to chart.js ===================================

    request_dailyAmount_list = request_amount_byDay_df.to_frame().rename(columns={'amount': 'sum'})['sum'].to_list()

    # IMPORTANT
    request_date_amount_dict = dict(zip(str_request_created_dates_list, request_dailyAmount_list))

    # IMPORTANT
    request_date_amount_dict_30days = copy.deepcopy(empty_30days_dict)
    request_date_amount_dict_90days = copy.deepcopy(empty_90days_dict)
    request_date_amount_dict_7days = copy.deepcopy(empty_7days_dict)
    for k in request_date_amount_dict:
        if k in request_date_amount_dict_30days:
            request_date_amount_dict_30days[k] = request_date_amount_dict[k]
        if k in request_date_amount_dict_90days:
            request_date_amount_dict_90days[k] = request_date_amount_dict[k]
        if k in request_date_amount_dict_7days:
            request_date_amount_dict_7days[k] = request_date_amount_dict[k]

# =================================== pass all data to chart.js ===================================
    pass_data = {
        'amount_of_circles': len(graphql_query_response['circleCreatedEntities']),
        'amount_of_users': len(all_active_users_dict),

        'circle_created_dates_list': circle_date_count_dict.keys(),
        'circle_dailyCount_list': circle_date_count_dict.values(),
        '30days_circle_created_dates_list': circle_date_count_dict_30days.keys(),
        '30days_circle_dailyCount_list': circle_date_count_dict_30days.values(),
        '90days_circle_created_dates_list': circle_date_count_dict_90days.keys(),
        '90days_circle_dailyCount_list': circle_date_count_dict_90days.values(),
        '7days_circle_created_dates_list': circle_date_count_dict_7days.keys(),
        '7days_circle_dailyCount_list': circle_date_count_dict_7days.values(),

        'amount_of_deposits': len(graphql_query_response['depositMadeEntities']),
        'dollar_amount_of_deposits': total_deposit_amount_dollar,

        'deposit_created_dates_list': deposit_date_count_dict.keys(),
        'deposit_dailyCount_list': deposit_date_count_dict.values(),
        '30days_deposit_created_dates_list': deposit_date_count_dict_30days.keys(),
        '30days_deposit_dailyCount_list': deposit_date_count_dict_30days.values(),
        '90days_deposit_created_dates_list': deposit_date_count_dict_90days.keys(),
        '90days_deposit_dailyCount_list': deposit_date_count_dict_90days.values(),
        '7days_deposit_created_dates_list': deposit_date_count_dict_7days.keys(),
        '7days_deposit_dailyCount_list': deposit_date_count_dict_7days.values(),

        'deposit_dailyAmount_list': deposit_date_amount_dict.values(),
        '30days_deposit_dailyAmount_list': deposit_date_amount_dict_30days.values(),
        '90days_deposit_dailyAmount_list': deposit_date_amount_dict_90days.values(),
        '7days_deposit_dailyAmount_list': deposit_date_amount_dict_7days.values(),

        'amount_of_requests': len(graphql_query_response['loanRequestMadeEntities']),
        'dollar_amount_of_requests': total_deposit_amount_dollar,

        'request_created_dates_list': request_date_count_dict.keys(),
        'request_dailyCount_list': request_date_count_dict.values(),
        '30days_request_created_dates_list': request_date_count_dict_30days.keys(),
        '30days_request_dailyCount_list': request_date_count_dict_30days.values(),
        '90days_request_created_dates_list': request_date_count_dict_90days.keys(),
        '90days_request_dailyCount_list': request_date_count_dict_90days.values(),
        '7days_request_created_dates_list': request_date_count_dict_7days.keys(),
        '7days_request_dailyCount_list': request_date_count_dict_7days.values(),

        'request_dailyAmount_list': request_date_amount_dict.values(),
        '30days_request_dailyAmount_list': request_date_amount_dict_30days.values(),
        '90days_request_dailyAmount_list': request_date_amount_dict_90days.values(),
        '7days_request_dailyAmount_list': request_date_amount_dict_7days.values(),

        '30days_list': get_x_dayList(30),
        '90days_list': get_x_dayList(90),
        '7days_list': get_x_dayList(7)

    }

    # write each user file
    for each_active_user in all_active_users_dict:
        with open(f"csv_files_fromPy/Users&Circles/{each_active_user}.csv", "w") as user_f:
            user_w = csv.writer(user_f)
            user_w.writerows(
                [['activity', 'time', 'circle address',  'amount']] + all_active_users_dict[each_active_user])
            user_f.close()

    # write each circle file
    for each_active_circle in all_active_circles_dict:
        with open(f"csv_files_fromPy/Users&Circles/{each_active_circle}.csv", "w") as circle_f:
            circle_w = csv.writer(circle_f)
            circle_w.writerows(
                [['activity', 'time', 'user address',  'amount']] + all_active_circles_dict[each_active_circle])
            circle_f.close()

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


def download_specific_user_circle_data(request):
    input_address = request.POST['user_circle_address']
    #return render(request, 'portal/main_page.html')
    try:
        f1_path = f"csv_files_fromPy/Users&Circles/{input_address}.csv"
        f1 = open(f1_path, 'r')
        mime_type, _ = mimetypes.guess_type(f1_path)
        response = HttpResponse(f1, content_type=mime_type)
        response['Content-Disposition'] = f"attachment; filename={input_address}.csv"
        return response
    except:
        print("FILE NAME NOT VALID")
        return redirect('/main_page')
