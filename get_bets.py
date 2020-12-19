#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

import requests
import pandas as pd
import os
from iBotAutomation.dataBase_activities import Sqlite
import sched,time


class ArbsQuery:
    def __init__(self):
        self.token = '52de173b6b08870dfb070f3ee3e98d92'
        self.filter_id = "423552"
        self.excluded_bets = ""
        self.url = "https://rest-api-pr.betburger.com/api/v1/arbs/bot_search"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"}
        self.data = None
        self.request = None
        self.csv = "/Users/enriquecrespodebenito/Desktop/Betburger API/surebets.csv"
        self.dataBase = None
        self.sqlite = Sqlite("/Users/enriquecrespodebenito/Desktop/Betburger API/surebets.sqlite")

    def excludedBets(self):
        self.excluded_bets = ""
        print(self.dataBase[(self.dataBase.started_at > datetime.now())])
        try:
            self.dataBase = pd.read_csv(self.csv)
            self.dataBase['bets'] = self.dataBase['bet1_id'] + "," + self.dataBase['bet1_id']
            for eventId in self.dataBase['bets'].iteritems():
                self.excluded_bets = self.excluded_bets + str(eventId[1]) + ','
        except:
            self.excluded_bets = ""

    def getData(self):
        self.excludedBets()
        self.data = f"search_filter[]={self.filter_id}&per_page=30&&excluded_bets[]={self.excluded_bets[:-1]}&access_token={self.token}"
        self.request = requests.post(self.url, headers=self.headers, data=self.data)
        return self.request.json()

    def processData(self, data):
        print(self.request)
        if self.request.json()['total_by_filter'] > 0:
            d = pd.json_normalize(data['arbs'])
            df = pd.DataFrame(d)
            df['started_at'] = pd.to_datetime(df['started_at'], unit='s')
            df['created_at'] = pd.to_datetime(df['created_at'], unit='s')
            df['updated_at'] = pd.to_datetime(df['updated_at'], unit='s')
            df.to_csv(self.csv, mode='a', header=True, index=False)
            for arb in data['arbs']:
                try:
                    self.sqlite.Insert("arbs", arb)
                except:
                    pass
            for bet in data['bets']:
                try:
                    self.sqlite.Insert("bets", bet)
                except:
                    pass
            self.dataBase = pd.read_csv(self.csv)
            print("DataBase Size:", self.dataBase.size)

    def run(self, sc):
        try:
            data = self.getData()
            self.processData(data)
        except:
            pass
        s.enter(10, 1, self.run, (sc,))


if __name__ == "__main__":
    query = ArbsQuery()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, query.run, (s,))
    s.run()
