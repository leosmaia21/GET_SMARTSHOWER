import streamlit as st
import csv
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, time
from streamlit_calendar import calendar
import pickle
from sklearn.neighbors import LocalOutlierFactor


def load_csv():
    with open("/home/leonardo/hackaton/timeseries/VZTnyVO3TP3ILuYsN5Xw9UR0.csv") as f:
        # data = csv.reader(f)
        data = pd.read_csv(f, usecols=['ts', 'HwTStor', 'HwTAct', 'ActPow', 'HP_EnergyOutCH', 'PrimTSet'])
        # data = data[0:50000]
        #get the data for the first day
        # data = data[data['ts'].str.contains('2023-01-12')]
        if 'timestamp' in st.session_state:
            timestamp = st.session_state["timestamp"]
            data = data[data['ts'].str.contains(timestamp)]
            data['ts'] = data['ts'].str[11:16]
            data.columns = data.columns.str.replace('ts', 'Hora')
            data.columns = data.columns.str.replace('HwTStor', 'Temperatura reservatorio (ºc)')
            data.columns = data.columns.str.replace('HwTAct', 'Temperatura da agua (ºc)')
            data.columns = data.columns.str.replace('ActPow', 'Potência (%)')
            data.columns = data.columns.str.replace('HP_EnergyOutCH', 'Energia total (KWh)')
            data['mean'] = data['Temperatura reservatorio (ºc)'].mean()

            data['Temperatura reservatorio (ºc)'] = data['Temperatura reservatorio (ºc)'].rolling(20).mean()
            data2 = data.iloc[::10]
            data2['diff'] = data2['Temperatura reservatorio (ºc)'].diff()
            #  mean data2[diff]
            data2['filterDiff'] = data2['diff'].rolling(15).mean()

            data3 = data2[['Hora', 'filterDiff']]
            data3 = data3.dropna()

            data3['diffdiff'] = data3['filterDiff'].diff()
            indices_mudanca_de_sinal = []

            # for i in range(1, data3.shape[0]):
            #     if (data3['diffdiff'][i] < 0 and data3['diffdiff'][i - 1] >= 0) or (data3['diffdiff'][i] >= 0 and data3['diffdiff'][i - 1] < 0):
            #         indices_mudanca_de_sinal.append(i)
            # print(indices_mudanca_de_sinal)

            #load lof model
            # with open('lof.pkl', 'rb') as file:
            #     lof = pickle.load(file)
            #     input = np.array(data3['filterDiff'].tolist())
            #     input = input.reshape(-1, 1)
            #     ret = lof.fit_predict(input)
            #     data3['predict'] = ret
                # ret = lof.fit_predict()
            




            return data, data2, data3
    return None


# st.session_state["x"] = 0
def main():

    if st.button("PT/EN"):
        print("ola")
    perfis, estatistica, banho, dicas, feedback, dispositivo = st.tabs(["Perfis", "Estatistica", "Agendar", "Dicas", "Feedback", "Dispositivo" ])

    with perfis:
        st.button("casa")
        st.button("utilizador")
    with estatistica:
        d = st.date_input("Timestamp", value = datetime(2023, 9, 11)).strftime('%Y-%m-%d')
        st.session_state["timestamp"] = d
        data, data2, data3 = load_csv()
        col1, col2 = st.columns(2)
        col1.line_chart(data=data, x='Hora', y=['Temperatura reservatorio (ºc)', 'mean'], color=["#00FF00", "#0000FF"])
        col1.line_chart(data=data2, x='Hora', y='filterDiff', color=["#00FF00"])
        # col1.line_chart(data=data3, x='Hora', y='predict', color=["#00FF00"])
        col2.line_chart(data=data, x='Hora', y='Temperatura da agua (ºc)')
        col2.line_chart(data=data, x='Hora', y='Potência (%)')

    with banho:
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
                    {"id": "a", "building": "Pessoas", "title": "Davide"},
                    {"id": "b", "building": "Pessoas", "title": "Lara"},
                    {"id": "c", "building": "Pessoas", "title": "Leonardo"},
                ],
            },
                'calendar_events' : [{
                "start": "2023-10-04T15:30:00",
                "title": "Davide",
                "end": "2023-10-04T16:00:00",
                "resourceId": "a",
            } ]
            }
        calendar(events=st.session_state['calendario']['calendar_events'], options=st.session_state['calendario']['calendar_options'])
        col1, col2, col3 = st.columns(3)
        with col1:
            option = st.selectbox(
            'Quem vai tomar banho?',
            ('Davide', 'Lara', 'Leonardo'))
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
        
        
    with dicas:
        st.image("dicas.png")


    with feedback:
        st.write("Feedback")
        st.write("Gostou da temperatura da água?")
        s = st.select_slider( 'Escolha', options=['Não', 'Sim', 'Indiferente'])
        if st.button("Enviar!"):
            st.write("Guardado", s)

    with dispositivo:

        st.write("Tempo restante", "1:30")
        values = st.slider(
            'Tempo para tomar banho (minutos)',
            0, 30)
        st.button("Iniciar")


main()
