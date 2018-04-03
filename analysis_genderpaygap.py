#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import csv
from collections import OrderedDict
import scraperwiki

grouplinksurl='https://raw.githubusercontent.com/edudatalab/genderpaygap/master/data/unedited/grouplinks_edubaseallacademiesandfree20170403.csv'
paygapurl='https://raw.githubusercontent.com/edudatalab/genderpaygap/master/data/unedited/UK%20Gender%20Pay%20Gap%20Data%20-%202017%20to%202018.csv'
workforceurl='https://raw.githubusercontent.com/edudatalab/genderpaygap/master/data/edited/SFR25_2017_Underlying_Data.csv'

# READ SOURCE FILES
grouplinkscsv=requests.get(grouplinksurl)
grouplinkscsv=grouplinkscsv.iter_lines()      # is required in order for csv file to be read correctly, without errors caused by new-line characters
reader=csv.DictReader(grouplinkscsv)
for row in reader:
    if row['Group Type']=='Single-academy trust' or row['Group Type']=='Multi-academy trust':
        school=OrderedDict([])
        school['Group Name']=row['Group Name'].replace('\xa0', ' ').replace('\x92', '\'')       # hacky, but successfully replaces characters that prevent saving
        school['CompanyNumber']=row['Companies House Number']
        school['URN']=row['URN']
        scraperwiki.sql.save(['URN'],school,"grouplinks")

paygapcsv=requests.get(paygapurl)
paygapcsv=paygapcsv.iter_lines()      # is required in order for csv file to be read correctly, without errors caused by new-line characters
reader = csv.DictReader(paygapcsv)
i=1
for row in reader:
    employer=OrderedDict([])
    employer['EmployerName']=row['EmployerName'].replace('\xbd', '').replace('\xbf', '').replace('\xef', 'i').replace('\xe2', 'a').replace('\x80', '').replace('\x99', ' ').replace('\x0b', '').replace('\xc3', 'A').replace('\xa9', '').replace('\x93', '\"').replace('\x89', '').replace('\x96', '').replace('\xae', '').replace('\x88', '').replace('\xb6', '').replace('\xa1', '').replace('\x98', '').replace('\x82', '').replace('\xac', '')
    employer['Address']=row['Address'].replace('\xbd', '').replace('\xbf', '').replace('\xef', 'i').replace('\xe2', 'a').replace('\x80', '').replace('\x99', ' ').replace('\x0b', '').replace('\xc3', 'A').replace('\xa9', '').replace('\x93', '\"').replace('\x89', '').replace('\x96', '').replace('\xae', '').replace('\x88', '').replace('\xb6', '').replace('\xa1', '').replace('\x98', '').replace('\x82', '').replace('\xac', '')
    employer['SicCodes']=row['SicCodes']
    if row['CompanyNumber']!='':
        employer['CompanyNumber']=row['CompanyNumber']
    else:       # create spoof co. number
        employer['CompanyNumber']='X'+str(i)
        i+=1
    employer['DiffMeanHourlyPercent']=row['DiffMeanHourlyPercent']
    employer['DiffMedianHourlyPercent']=row['DiffMedianHourlyPercent']
    employer['DiffMeanBonusPercent']=row['DiffMeanBonusPercent']
    employer['DiffMedianBonusPercent']=row['DiffMedianBonusPercent']
    employer['MaleBonusPercent']=row['MaleBonusPercent']
    employer['FemaleBonusPercent']=row['FemaleBonusPercent']
    employer['MaleLowerQuartile']=row['MaleLowerQuartile']
    employer['FemaleLowerQuartile']=row['FemaleLowerQuartile']
    employer['MaleLowerMiddleQuartile']=row['MaleLowerMiddleQuartile']
    employer['FemaleLowerMiddleQuartile']=row['FemaleLowerMiddleQuartile']
    employer['MaleUpperMiddleQuartile']=row['MaleUpperMiddleQuartile']
    employer['FemaleUpperMiddleQuartile']=row['FemaleUpperMiddleQuartile']
    employer['MaleTopQuartile']=row['MaleTopQuartile']
    employer['FemaleTopQuartile']=row['FemaleTopQuartile']
    employer['CompanyLinkToGPGInfo']=row['CompanyLinkToGPGInfo'].replace('\xbd', '').replace('\xbf', '').replace('\xef', 'i').replace('\xe2', 'a').replace('\x80', '').replace('\x99', ' ').replace('\x0b', '').replace('\xc3', 'A').replace('\xa9', '').replace('\x93', '\"').replace('\x89', '').replace('\x96', '').replace('\xae', '').replace('\x88', '').replace('\xb6', '').replace('\xa1', '').replace('\x98', '').replace('\x82', '').replace('\xac', '')
    employer['ResponsiblePerson']=row['ResponsiblePerson'].replace('\xbd', '').replace('\xbf', '').replace('\xef', 'i').replace('\xe2', 'a').replace('\x80', '').replace('\x99', ' ').replace('\x0b', '').replace('\xc3', 'A').replace('\xa9', '').replace('\x93', '\"').replace('\x89', '').replace('\x96', '').replace('\xae', '').replace('\x88', '').replace('\xb6', '').replace('\xa1', '').replace('\x98', '').replace('\x82', '').replace('\xac', '')
    employer['EmployerSize']=row['EmployerSize']
    employer['CurrentName']=row['CurrentName'].replace('\xbd', '').replace('\xbf', '').replace('\xef', 'i').replace('\xe2', 'a').replace('\x80', '').replace('\x99', ' ').replace('\x0b', '').replace('\xc3', 'A').replace('\xa9', '').replace('\x93', '\"').replace('\x89', '').replace('\x96', '').replace('\xae', '').replace('\x88', '').replace('\xb6', '').replace('\xa1', '').replace('\x98', '').replace('\x82', '').replace('\xac', '')
    scraperwiki.sql.save(['CompanyNumber'],employer,"paygap")

workforcecsv=requests.get(workforceurl)
workforcecsv=workforcecsv.iter_lines()      # is required in order for csv file to be read correctly, without errors caused by new-line characters
reader = csv.DictReader(workforcecsv)
for row in reader:
    school=OrderedDict([])
    school['URN']=row['URN']
    school['Total School Workforce (Headcount)']=row['Total School Workforce (Headcount)']
    scraperwiki.sql.save(['URN'],school,"workforce")


# ANALYSIS
# Trusts that can be found in pay gap data
print scraperwiki.sqlite.execute('''
    SELECT
      count(1)
    FROM paygap p
    where
        exists (select distinct CompanyNumber from grouplinks g where p.CompanyNumber=g.CompanyNumber) or
        EmployerName in ('Aquinas CE Education Trust','Beckfoot Trust','Bradford College','Emlc Academy Trust','Focus Academy Trust (UK) Ltd','Hastings Academies Trust','Lighthouse Schools Partnership','NINESTILES ACADEMY TRUST LIMITED','RIver Learning Trust','Southend East Community Academy Trust','Trent Academies Group','University of Brighton Academies Trust')
    order by EmployerName
''')['data'][0][0]
trustsgenderpaygapkeys=[]       # done this way to create a list containing one tuple, which writer.writerows can easily use
trustsgenderpaygapkeys.append(tuple(scraperwiki.sqlite.execute('''
    SELECT
      p.*
    FROM paygap p
    where
      exists (select distinct CompanyNumber from grouplinks g where p.CompanyNumber=g.CompanyNumber) or
      EmployerName in ('Aquinas CE Education Trust','Beckfoot Trust','Bradford College','Emlc Academy Trust','Focus Academy Trust (UK) Ltd','Hastings Academies Trust','Lighthouse Schools Partnership','NINESTILES ACADEMY TRUST LIMITED','RIver Learning Trust','Southend East Community Academy Trust','Trent Academies Group','University of Brighton Academies Trust')
''')['keys']))
trustsgenderpaygapdata=scraperwiki.sqlite.execute('''
    SELECT
      p.*
    FROM paygap p
    where
      exists (select distinct CompanyNumber from grouplinks g where p.CompanyNumber=g.CompanyNumber) or
      EmployerName in ('Aquinas CE Education Trust','Beckfoot Trust','Bradford College','Emlc Academy Trust','Focus Academy Trust (UK) Ltd','Hastings Academies Trust','Lighthouse Schools Partnership','NINESTILES ACADEMY TRUST LIMITED','RIver Learning Trust','Southend East Community Academy Trust','Trent Academies Group','University of Brighton Academies Trust')
''')['data']


# Data for chart, 10 largest MATs
trustsgenderpaygapforchartkeys=[]       # done this way to create a list containing one tuple, which writer.writerows can easily use
trustsgenderpaygapforchartkeys.append(tuple(scraperwiki.sqlite.execute('''
    SELECT
      EmployerName,
      DiffMedianHourlyPercent
    FROM paygap p
    where
      EmployerName in ('Academies Enterprise Trust','Reach2 Academy Trust','United Learning Trust','Oasis Community Learning','The Kemnal Academies Trust','Harris Federation','Delta Academies Trust','Ark Schools','Plymouth Cast','The David Ross Education Trust','Ormiston Academies Trust','The Diocese Of Ely Multi-Academy Trust','Greenwood Academies Trust','The Diocese Of Norwich Education And Academies Trust','Oxford Diocesan Schools Trust','The Elliot Foundation Academies Trust','Glf Schools','The Enquire Learning Trust','The Bath And Wells Diocesan Academies Trust')      -- Hamwic Education Trust excluded: doesn't feature in the data as while it's now one of the biggest trusts it seems to have been very small 12 months ago
    order by
        EmployerName
''')['keys']))
trustsgenderpaygapforchartdata=scraperwiki.sqlite.execute('''
    SELECT
      EmployerName,
      DiffMedianHourlyPercent
    FROM paygap p
    where
        EmployerName in ('Academies Enterprise Trust','Reach2 Academy Trust','United Learning Trust','Oasis Community Learning','The Kemnal Academies Trust','Harris Federation','Delta Academies Trust','Ark Schools','Plymouth Cast','The David Ross Education Trust','Ormiston Academies Trust','The Diocese Of Ely Multi-Academy Trust','Greenwood Academies Trust','The Diocese Of Norwich Education And Academies Trust','Oxford Diocesan Schools Trust','The Elliot Foundation Academies Trust','Glf Schools','The Enquire Learning Trust','The Bath And Wells Diocesan Academies Trust')      -- Hamwic Education Trust excluded: doesn't feature in the data as while it's now one of the biggest trusts it seems to have been very small 12 months ago
    order by
        EmployerName
''')['data']


# Trusts with more than 250 employees that don't appear in pay gap data
print scraperwiki.sqlite.execute('''
    SELECT
        count(1)
    from
    (SELECT
    CompanyNumber,
    [Group Name]
    FROM workforce w
      INNER JOIN grouplinks g ON
        w.urn=g.urn
    where
      not exists (select CompanyNumber from paygap p where g.CompanyNumber=p.CompanyNumber) and
      [Group Name] not in ('Aquinas Church of England Education Trust Limited','Beckfoot Trust','Bradford College Education Trust','EMLC Academy Trust','Focus Academy Trust (UK) Ltd','Hastings Academies Trust','Lighthouse Schools Partnership','Ninestiles Academy Trust Limited','River Learning Trust','Southend East Community Academy Trust','Trent Academies Group','University of Brighton Academies Trust')
    group by
        CompanyNumber,
        [Group Name]
    having sum([Total School Workforce (Headcount)])>=250
    ) q
''')['data'][0][0]
missingtrustskeys=[]        # done this way to create a list containing one tuple, which writer.writerows can easily use
missingtrustskeys.append(tuple(scraperwiki.sqlite.execute('''
    SELECT
      CompanyNumber,
      [Group Name]
    FROM workforce w
      INNER JOIN grouplinks g ON
        w.urn=g.urn
    where
      not exists (select CompanyNumber from paygap p where g.CompanyNumber=p.CompanyNumber) and
      [Group Name] not in ('Aquinas Church of England Education Trust Limited','Beckfoot Trust','Bradford College Education Trust','EMLC Academy Trust','Focus Academy Trust (UK) Ltd','Hastings Academies Trust','Lighthouse Schools Partnership','Ninestiles Academy Trust Limited','River Learning Trust','Southend East Community Academy Trust','Trent Academies Group','University of Brighton Academies Trust')
    group by
      CompanyNumber,
      [Group Name]
    having sum([Total School Workforce (Headcount)])>=250
''')['keys']))
missingtrustsdata=scraperwiki.sqlite.execute('''
    SELECT
      CompanyNumber,
      [Group Name]
    FROM workforce w
      INNER JOIN grouplinks g ON
        w.urn=g.urn
    where
      not exists (select CompanyNumber from paygap p where g.CompanyNumber=p.CompanyNumber) and
      [Group Name] not in ('Aquinas Church of England Education Trust Limited','Beckfoot Trust','Bradford College Education Trust','EMLC Academy Trust','Focus Academy Trust (UK) Ltd','Hastings Academies Trust','Lighthouse Schools Partnership','Ninestiles Academy Trust Limited','River Learning Trust','Southend East Community Academy Trust','Trent Academies Group','University of Brighton Academies Trust')
    group by
      CompanyNumber,
      [Group Name]
    having sum([Total School Workforce (Headcount)])>=250
''')['data']


# SAVE RESULT OF ANALYSIS
with open('trustsgenderpaygap.csv', 'wb') as trustsgenderpaygapcsv:
    writer=csv.writer(trustsgenderpaygapcsv)
    writer.writerows(trustsgenderpaygapkeys)
    writer.writerows(trustsgenderpaygapdata)

with open('trustsgenderpaygapforchart.csv', 'wb') as trustsgenderpaygapforchartcsv:
    writer=csv.writer(trustsgenderpaygapforchartcsv)
    writer.writerows(trustsgenderpaygapforchartkeys)
    writer.writerows(trustsgenderpaygapforchartdata)

with open('missingtrusts.csv', 'wb') as missingtrustscsv:
    writer=csv.writer(missingtrustscsv)
    writer.writerows(missingtrustskeys)
    writer.writerows(missingtrustsdata)
