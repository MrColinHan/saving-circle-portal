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
    }
    ''')

    graphql_query_response = client.execute(graphql_query)

    '''===save "circle" data to a dataframe==='''
    print(f"====== Pulling Circle Data ======")
    circles_df = pd.DataFrame(columns=['circle address', 'creator address', 'timeStamp'])
    # print(f"{len(graphql_query_response['circleCreatedEntities'])} circles have been created: ")
    for circle in graphql_query_response['circleCreatedEntities']:
        circles_df.loc[len(circles_df)] = [circle['id'], circle['creator'],
                                           datetime.fromtimestamp(int(circle['timeStamp']))]
        # print(f"{circle['id']} ----- {circle['creator']} ----- {datetime.fromtimestamp(int(circle['timeStamp']))}")
    print(circles_df)
    circles_df.to_csv("csv_files_fromPy/circles_created.csv")  # output circle dataframe to a csv file
    # === count number of circles by day
    circle_count_byDay_df = circles_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['circle address'].count()
    circle_count_byDay_df.to_frame().rename(columns={'circle address': 'count'}).to_csv(
        "csv_files_fromPy/circle_count_byDay.csv")  # output this df to a csv file

    '''===save "deposit_made" data to a dataframe==='''
    print(f"====== Pulling Deposit_made Data ======")
    deposit_df = pd.DataFrame(columns=['id', 'depositor', 'circle', 'amount', 'timeStamp'])
    for deposit in graphql_query_response['depositMadeEntities']:
        deposit_df.loc[len(deposit_df)] = [deposit['id'],
                                           deposit['depositor'],
                                           deposit['circle'], deposit['amount'],
                                           datetime.fromtimestamp(int(deposit['timeStamp']))]
    print(deposit_df)
    deposit_df.to_csv("csv_files_fromPy/deposits_made.csv")  # save as a csv file
    # === count number of deposits each day
    deposit_count_byDay_df = deposit_df.groupby(pd.Grouper(key='timeStamp', freq='D'))['id'].count()
    deposit_count_byDay_df.to_frame().rename(columns={'id': 'count'}).to_csv("csv_files_fromPy/deposit_count_byDay.csv")

    '''===save "loan request" data to a dataframe==='''
    print(f"====== Pulling_request Data ======")

    pass_data = {
        'amount_of_circles': len(graphql_query_response['circleCreatedEntities']),
        'circle_created_dates_list': ['7/5/21','7/6/21','7/7/21','7/8/21','7/9/21','7/10.21'],#circle_count_byDay_df.to_frame().rename(columns={'circle address': 'count'}).index.to_list(),
        'circle_dailyCount_list': circle_count_byDay_df.to_frame().rename(columns={'circle address': 'count'})['count'].to_list(),

        'deposit_created_dates_list': ['7/5/21','7/6/21','7/7/21','7/8/21','7/9/21','7/10.21'],#deposit_count_byDay_df.to_frame().rename(columns={'id': 'count'}).index.to_list(),
        'deposit_dailyCount_list': [0,0,0,0,1,2]#deposit_count_byDay_df.to_frame().rename(columns={'id': 'count'})['count'].to_list()
    }
    return render(request, 'portal/main_page.html', pass_data)







