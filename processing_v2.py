"""
http://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/
Script imports bank statements, remove duplicate transactions, generates summary reports.
TO BE IMPROVED:
create dictionary for categories.
"""
import os 
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import font_manager as fm

def listdir(statments_dir):
	"""
	returns list of files(csvs) to be parsed
	"""
	statments_full_dir = str(Path(os.getcwd()).parent)+statments_dir
	csv_list = []
	for root, dirs, files in os.walk(statments_full_dir):
		for f in files:
			if f.endswith('.csv'):
				csv_list.append(os.path.join(root, f))
	
	return csv_list

def loadcsv(csv_filename):
	# data = pd.read_csv(csv_filename, na_values=[0], skiprows=16, usecols=range(0,7))
	print csv_filename
	data = np.genfromtxt(csv_filename, dtype=None, skip_header=16, delimiter = ',', usecols=range(0,7),names=True)
	df = pd.DataFrame(data)
	df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
	# print df
	return df

def consolidate(statments_dir):
	return pd.concat([loadcsv(f) for f in listdir(statments_dir)]).drop_duplicates().fillna(0)

def monthly_report():
	c = consolidate('/statements')
	d = c[c['Transaction_Ref2']!='LeeEJ'].set_index('Transaction_Date')
	e = pd.groupby(d,by=[d.index.year,d.index.month])
	savings = e['Credit_Amount'].sum()-e['Debit_Amount'].sum()
	print e.sum()
	print e.sum().sum()
	print savings
	print savings.sum()
	# savings.plot(style='o')
	# plt.show()
	return e

def month_report(y,m):
	c = consolidate('/statements')
	d = c[c['Transaction_Ref2']!='LeeEJ'].set_index('Transaction_Date')
	e = d[(d.index.year==y)&(d.index.month==m)]
	f = pd.groupby(e,by=['Transaction_Ref1'])
	print f.sum()
	print f.sum().sum()
	print "Savings \t {} \t {:.2f}%".format(
		np.diff(f.sum().sum())[0],
		(np.diff(f.sum().sum())/f.sum().sum()[1:])[0]*100
		)
	plt.cla()
	f.sum()['Debit_Amount'].plot(autopct='%1.1f%%', kind='pie',fontsize=8)
	plt.title('Expenditure for {} {}'.format(y,m))
	plt.show()
	return f

def cat_report():
	'''
	prints longitudinal expenditure per category
	'''
	c = consolidate('/statements')
	d = c[c['Transaction_Ref2']!='LeeEJ'].set_index('Transaction_Date')
	e = pd.groupby(d,by=['Transaction_Ref1',d.index.year,d.index.month]).sum()
	return e

def cat_plot(n=2):
	'''
	plots longitudinal expenditure per category if it is repeated for more than n months.
	'''
	c = consolidate('/statements')
	d = c[c['Transaction_Ref2']!='LeeEJ']

	for key,grp in d.groupby('Transaction_Ref1'):
		g = grp.set_index('Transaction_Date')
		h = g.groupby([g.index.year,g.index.month]).sum()['Debit_Amount']
		# print key, h
		if len(h) >= n:
			plt.figure(key)
			h.plot(label=key, kind='bar')
			plt.show()

def annual_report(y):
	c = consolidate('/statements')
	d = c[c['Transaction_Ref2']!='LeeEJ'].set_index('Transaction_Date')
	e = d[d.index.year==y]
	f = pd.groupby(e,by=['Transaction_Ref1'])
	print f.sum()
	print f.sum().sum()
	print "Savings \t {} \t {:.2f}%".format(
		np.diff(f.sum().sum())[0],
		(np.diff(f.sum().sum())/f.sum().sum()[1:])[0]*100
		)
	plt.cla()
	f.sum()['Debit_Amount'].plot(autopct='%1.1f%%', kind='pie',fontsize=8)
	plt.title('Expenditure for year {}'.format(y))
	plt.show()
	return f

c = consolidate('/statements')
d = c[c['Transaction_Ref2']!='LeeEJ'].set_index('Transaction_Date')
