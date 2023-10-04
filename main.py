import streamlit as st
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter 
from datetime import datetime, timedelta, time
from streamlit_calendar import calendar


# envrioment variables


def load_csv():
    with open("/home/leonardo/hackaton/timeseries/VZTnyVO3TP3ILuYsN5Xw9UR0.csv") as f:
        # data = csv.reader(f)
        data = pd.read_csv(f, usecols=['ts', 'HwTStor', 'HwTAct', 'ActPow', 'HP_EnergyOutCH'])
        # data = data[0:4000]
        #get the data for the first day
        # data = data[data['ts'].str.contains('2023-01-12')]
        if 'timestamp' in st.session_state:
            print("state", st.session_state["timestamp"])
            timestamp = st.session_state["timestamp"]
            print("data", timestamp)
            #convert to string
            # timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d')
            print(type(timestamp))
            data = data[data['ts'].str.contains(timestamp)]
            data['ts'] = data['ts'].str[11:16]
            # print("maravilha", data)
        # filter timestamp
            return data
    return None


# st.session_state["x"] = 0
def main():

    tab1, tab2, tab3 = st.tabs(["Estatistica", "Marcar Banho", "Owl"])

    with tab1:
        d = st.date_input("Timestamp").strftime('%Y-%m-%d')
        st.session_state["timestamp"] = d
        data = load_csv()
        col1, col2 = st.columns(2)
        col1.line_chart(data=data, x='ts', y='HwTStor')
        col1.line_chart(data=data, x='ts', y='HwTAct')
        col2.line_chart(data=data, x='ts', y='ActPow')
        col2.line_chart(data=data, x='ts', y='HP_EnergyOutCH')

    with tab2:
        if 'calendario' not in st.session_state:
            st.session_state['calendario'] = { 'calendar_options' : {
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
                },
                "slotMinTime": "06:00:00",
                "slotMaxTime": "18:00:00",
                "initialView": "resourceTimelineDay",
                "resources": [
                    {"id": "a", "building": "Pessoas", "title": "Morgado"},
                    {"id": "b", "building": "Pessoas", "title": "Sara"},
                    {"id": "c", "building": "Pessoas", "title": "Leonardo"},
                ],
            },
                'calendar_events' : [ ]
            }
        calendar(events=st.session_state['calendario']['calendar_events'], options=st.session_state['calendario']['calendar_options'])
        col1, col2, col3 = st.columns(3)
        print("tipo", type(datetime.now()))
        with col1:
            option = st.selectbox(
            'Quem vai tomar banho?',
            ('Morgado', 'Sara', 'Leonardo'))
            # if st.button("Morgado"):
            #     st.session_state['calendario']['calendar_events'].append({"resourceId": "a", "title" : "maravilha", "start": "2023-10-04T06:00:00", "end": "2023-10-04T07:00:00"})
        with col2:
            if 'horas' not in st.session_state:
                st.session_state['horas'] = { 'inicio' : datetime.now().time(), 'fim' : (datetime.now() + timedelta(minutes=60 * 4)).time() }
            selectedTime = st.slider("Dia?", value=(st.session_state['horas']['inicio'], st.session_state['horas']['fim']), min_value = time(0, 0), max_value = time(23, 59), format="HH:MM")
            st.session_state['horas'] = { 'inicio' : selectedTime[0], 'fim' : selectedTime[1] }
        with col2:
            d = st.date_input("Dia").strftime('%Y-%m-%d')
            st.session_state['diaSelecionado'] = d

        if st.button("Marcar"):
            st.session_state['calendario']['calendar_events'].append({"resourceId": "a", "title" : option, "start": st.session_state['diaSelecionado'] + "T" + str(st.session_state['horas']['inicio']), "end": st.session_state['diaSelecionado'] + "T" + str(st.session_state['horas']['fim'])})











main()
