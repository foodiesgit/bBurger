#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
import requests
import pandas as pd
import os
from iBot.dataBase_activities import Sqlite
import sched, time
from sqlalchemy import create_engine


class ArbsQuery:
    SQLITE_PATH = "/Users/enriquecrespodebenito/Documents/BetBurger/bBurger/surebets.sqlite"
    def __init__(self):
        self.token = '103d99a7c2fd74fb9d0f821a35099f81'
        self.filter_id = "423552"
        self.excluded_bets = ""
        self.url = "https://rest-api-pr.betburger.com/api/v1/arbs/bot_search"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"}
        self.sqlite = Sqlite(self.SQLITE_PATH)
        self.sqliteConnection = sqlite3.connect(self.SQLITE_PATH)
        self.data = None
        self.request = None
        self.dataBase = None

    def excludedBets(self):
        self.excluded_bets = ""
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        try:
            self.filter = pd.read_sql_query(f"Select bet1_id,  bet2_id, bet3_id from arbs where started_at > '{now}' ", con=self.sqliteConnection)
            self.filter['bets'] = self.filter['bet1_id'] + "," + self.filter['bet2_id'] + ',' + self.filter['bet3_id'].fillna('')
            for eventId in self.filter['bets'].iteritems():
                if eventId:
                    self.excluded_bets = self.excluded_bets + str(eventId[1]) + ','

        except:
            self.excluded_bets = ""

    def getArbsData(self):
        self.excludedBets()
        self.data = f"search_filter[]={self.filter_id}&per_page=30&&excluded_bets[]={self.excluded_bets[:-2]}&access_token={self.token}"
        self.request = requests.post(self.url, headers=self.headers, data=self.data)
        print(self.request)
        return self.request.json()

    def processArbs(self, data):
        if self.request.json()['total_by_filter'] > 0:
            d = pd.json_normalize(data['arbs'])
            arbsdf = pd.DataFrame(d)
            arbsdf['started_at'] = pd.to_datetime(arbsdf['started_at'], unit='s')
            arbsdf['created_at'] = pd.to_datetime(arbsdf['created_at'], unit='s')
            arbsdf['updated_at'] = pd.to_datetime(arbsdf['updated_at'], unit='s')
            arbsdf = arbsdf.drop(['event_name_ru'], axis=1)
            arbsdf = arbsdf.drop(['league_ru'], axis=1)
            arbsdf = arbsdf.drop(['team1_name_ru'], axis=1)
            arbsdf = arbsdf.drop(['team2_name_ru'], axis=1)
            arbsdf = arbsdf.drop(['bk_ids'], axis=1)
            arbsdf = arbsdf.drop(['f_id'], axis=1)
            arbsdf.to_sql(name='arbs', con=self.sqliteConnection, if_exists='append', index = False)
            b = pd.json_normalize(data['bets'])
            betsdf = pd.DataFrame(b)
            betsdf['started_at'] = pd.to_datetime(betsdf['started_at'], unit='s')
            betsdf['updated_at'] = pd.to_datetime(betsdf['updated_at'], unit='s')
            betsdf = betsdf.drop(['player_ids'], axis=1)
            betsdf.to_sql(name='bets', con=self.sqliteConnection, if_exists='append', index = False)

    def run(self, sc):
        try:
            data = self.getArbsData()
            self.processArbs(data)
        except:
            pass
        s.enter(10, 1, self.run, (sc,))


if __name__ == "__main__":
    query = ArbsQuery()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(10, 1, query.run, (s,))
    s.run()
