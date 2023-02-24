import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates
import datetime as dt

def plus_recession(ax):
    recession = pd.read_csv('./data/us/recession_date.csv')
    x_date = matplotlib.dates.num2date(plt.gca().get_xlim()[0])
    x2_date = matplotlib.dates.num2date(plt.gca().get_xlim()[-1])
    start_date = dt.datetime(x_date.year,x_date.month,x_date.day)
    end_date = dt.datetime(x2_date.year,x2_date.month,x2_date.day)

    recession['Start'] = pd.to_datetime(recession['Start'])
    recession['End'] = pd.to_datetime(recession['End'])
    
    for i in recession.index:
        if recession['Start'][i] > start_date and recession['End'][i] < end_date:
            ax.axvspan(recession['Start'][i], recession['End'][i],color="gray",alpha=0.5)



data_list = pd.read_csv('./data/macro/list.csv')
name_list = list(data_list['name'])
# name_list = [x[1:] for x in name_list]
index_list = list(data_list['index'])

st.header("Data1")
select = st.selectbox(
    "select",list(name_list)
)
# st.write(name_list)
# st.write(name_list.index(select))
# st.write(select)
method_select = st.selectbox(
    "select",['none','yoy']
)
code = data_list.set_index(data_list['name']).loc[select]['list']
data = pd.read_csv('./data/macro/'+str(code[1:])+'.csv',index_col='date')['actual']
if method_select == 'yoy':
    data = data/data.shift(12)-1

st.header("Data2")

select2 = st.selectbox(
    "select2",list(name_list)
)

method_select2 = st.selectbox(
    "method2",['none','yoy']
)


code2 = data_list.set_index(data_list['name']).loc[select2]['list']
data2 = pd.read_csv('./data/macro/'+str(code2[1:])+'.csv',index_col='date')['actual']
data.index= pd.to_datetime(data.index)
data2.index = pd.to_datetime(data2.index)
if method_select2 == 'yoy':
    data2 = data2/data2.shift(12)-1

if data.index[0]>data2.index[0]:
    start = data2.index[0]
else:
    start = data.index[0]

if data.index[-1] > data2.index[-1]:
    end = data.index[-1]
else:
    end = data2.index[-1]

st.write(int(start.timestamp()))
start = dt.datetime.fromtimestamp(int(start.timestamp()))
end = dt.datetime.fromtimestamp(int(end.timestamp()))

time_range = st.slider(
    "Time range:",
    value=(start, end))

recession = st.checkbox("Recession")

data = data[data.index >= time_range[0]]
data2 = data2[data2.index >= time_range[0]]

data = data[data.index <= time_range[1]]
data2 = data2[data2.index <= time_range[1]]

fig = plt.figure()
ax1 = plt.subplot(1,1,1)
ax1.plot(data,label=select,color="k")
ax1.legend(loc='upper left')
ax2=ax1.twinx()
ax2.plot(data2,label=select2,color="gray")
ax2.legend(loc="lower right")
if recession:
    plus_recession(ax1)
plt.tight_layout()
st.pyplot(fig)


# fig = plt.figure(figsize=(12,7))
# plt.suptitle(title

# ax1 = plt.subplot(1,1,1)
# ax1.plot(data1,label=data1_label,color="k")
# ax1.legend(loc='upper left')

# ax2 = ax1.twinx()
# ax2.plot(data2,label=data2_label)
# ax2.legend(loc="upper right")