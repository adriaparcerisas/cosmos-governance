#!/usr/bin/env python
# coding: utf-8

# In[5]:


#!/usr/bin/env python
# coding: utf-8

# In[18]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
import altair as alt

sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[19]:


st.title('Osmosis Governance Activity')


# In[20]:


st.markdown('This page shows the basic governance activity trends on **Osmosis** chain. It is intended to provide an overview of the current activity and usage since inception.')


# In[5]:


st.markdown('To do that, we are gonna track the basic activity metrics registered such as:') 


st.write('- How did the voting power of the top 66% of the active set validators change')
st.write('- Power share distribution by validators rank')
st.write('- How did the Nakamoto Coefficient change?')
st.write('- Validators and delegators activity')
st.write('')


# In[10]:


sql = f"""
 WITH 
stakes1 as (
  SELECT 
   block_timestamp,
   tx_id,
    REDELEGATE_SOURCE_VALIDATOR_ADDRESS as validator,
    (amount / power(10,6))*(-1) as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is not null
),
   stakes2 as (
  SELECT 
    block_timestamp,
   tx_id,
    validator_address as validator,
    CASE WHEN action = 'undelegate' then (amount / power(10,6))*(-1) 
    else amount/power(10,6) end as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is NULL
), 
   stakes12 as (
  SELECT 
   block_timestamp,
   tx_id,
    validator_address as validator,
    (amount / power(10,6)) as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is not null
),
   stakes3 as (
  SELECT * FROM stakes1 UNION SELECT * FROM stakes2 UNION SELECT * FROM stakes12
), 
monthly as (
   SELECT 
   trunc(block_timestamp,'day') as days,
   tx_id,
   validator,
   sum(staked) as osmo_staked
FROM stakes3 WHERE staked is not null group by 1,2,3
),
  totals as (
   SELECT
   days,
   sum(osmo_staked) as month_osmo_staked,
   sum(month_osmo_staked) over (order by days)as total_osmo_staked
   from monthly
   group by 1 order by 1
   ),
ranking as (
   SELECT 
   days,
   validator,
   count(distinct tx_id) as txs,
   sum(osmo_staked) as total_near_delegated,
sum(total_near_delegated) over (partition by validator order by days) as cumulative_near_delegated
FROM monthly 
group by 1,2
),
stats as (
  SELECT
  days,
66 as bizantine_fault_tolerance,
total_osmo_staked,
(total_osmo_staked*bizantine_fault_tolerance)/100 as threshold--,
--sum(total_sol_delegated) over (partition by days order by validator_ranks asc) as total_sol_delegated_by_ranks,
--count(distinct vote_accounts) as validators
from totals
), 
stats2 as (
   select *,
1 as numbering,
sum(numbering) over (partition by days order by cumulative_near_delegated desc) as rank 
from ranking
   ),
stats3 as (
SELECT
days,
validator,
cumulative_near_delegated,
rank,
sum(cumulative_near_delegated) over (partition by days order by rank asc) as total_staked
--count(case when total_staked)
--sum(1) over (partition by days order by stake_rank) as nakamoto_coeff
  from stats2
order by rank asc),
final_nak as (
SELECT
a.days,
validator,
sum(case when total_staked <= threshold then cumulative_near_delegated end) as voting_power
from stats3 a 
join stats b 
on a.days = b.days --where a.days >=CURRENT_DATE-INTERVAL '3 MONTHS'
group by 1,2
order by 1 asc
   )
SELECT
days,
sum(voting_power) as voting_power
from final_nak
group by 1 order by 1 asc 
"""

sql2 = f"""
 WITH 
stakes1 as (
  SELECT 
   block_timestamp,
   tx_id,
    REDELEGATE_SOURCE_VALIDATOR_ADDRESS as validator,
    (amount / power(10,6))*(-1) as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is not null
),
   stakes2 as (
  SELECT 
    block_timestamp,
   tx_id,
    validator_address as validator,
    CASE WHEN action = 'undelegate' then (amount / power(10,6))*(-1) 
    else amount/power(10,6) end as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is NULL
), 
  stakes12 as (
  SELECT 
   block_timestamp,
   tx_id,
    validator_address as validator,
    (amount / power(10,6)) as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is not null
),
   stakes3 as (
  SELECT * FROM stakes1 UNION SELECT * FROM stakes2 UNION SELECT * FROM stakes12
), 
monthly as (
   SELECT 
   trunc(block_timestamp,'day') as days,
   tx_id,
   validator,
   sum(staked) as osmo_staked
FROM stakes3 WHERE staked is not null group by 1,2,3
),
  totals as (
   SELECT
   days,
   sum(osmo_staked) as month_osmo_staked,
   sum(month_osmo_staked) over (order by days)as total_osmo_staked
   from monthly
   group by 1 order by 1
   ),
ranking as (
   SELECT 
   days,
   validator,
   count(distinct tx_id) as txs,
   sum(osmo_staked) as total_near_delegated,
sum(total_near_delegated) over (partition by validator order by days) as cumulative_near_delegated
FROM monthly 
group by 1,2
),
stats as (
  SELECT
  days,
33 as bizantine_fault_tolerance,
total_osmo_staked,
(total_osmo_staked*bizantine_fault_tolerance)/100 as threshold--,
--sum(total_sol_delegated) over (partition by days order by validator_ranks asc) as total_sol_delegated_by_ranks,
--count(distinct vote_accounts) as validators
from totals
), 
stats2 as (
   select *,
1 as numbering,
sum(numbering) over (partition by days order by cumulative_near_delegated desc) as rank 
from ranking
   ),
stats3 as (
SELECT
days,
validator,
cumulative_near_delegated,
rank,
sum(cumulative_near_delegated) over (partition by days order by rank asc) as total_staked
--count(case when total_staked)
--sum(1) over (partition by days order by stake_rank) as nakamoto_coeff
  from stats2
order by rank asc),
finals as (
SELECT
a.days,
rank,
validator,
cumulative_near_delegated/total_osmo_staked as power_share
from stats3 a 
join totals b 
on a.days = b.days
--group by 1,2
order by 1 asc
   )
SELECT
   days,
case when rank between 1 and 10 then '1. Top 10 validators'
when rank between 10 and 50 then '2. Top 10-50 validators'
else '3. Top +50 validators' end as ranks,
sum(power_share) as power_share
from finals --where days >= CURRENT_DATE-INTERVAL '3 MONTHS'
group by 1,2
order by 1 asc, 2

"""

sql3 = f"""
 WITH 
stakes1 as (
  SELECT 
   block_timestamp,
   tx_id,
    REDELEGATE_SOURCE_VALIDATOR_ADDRESS as validator,
    (amount / power(10,6))*(-1) as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is not null
),
   stakes2 as (
  SELECT 
    block_timestamp,
   tx_id,
    validator_address as validator,
    CASE WHEN action = 'undelegate' then (amount / power(10,6))*(-1) 
    else amount/power(10,6) end as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is NULL
), 
  stakes12 as (
  SELECT 
   block_timestamp,
   tx_id,
    validator_address as validator,
    (amount / power(10,6)) as staked
  FROM osmosis.core.fact_staking
  where currency LIKE 'uosmo'
  AND REDELEGATE_SOURCE_VALIDATOR_ADDRESS is not null
),
   stakes3 as (
  SELECT * FROM stakes1 UNION SELECT * FROM stakes2 UNION SELECT * FROM stakes12
), 
monthly as (
   SELECT 
   trunc(block_timestamp,'day') as days,
   tx_id,
   validator,
   sum(staked) as osmo_staked
FROM stakes3 WHERE staked is not null group by 1,2,3
),
  totals as (
   SELECT
   days,
   sum(osmo_staked) as month_osmo_staked,
   sum(month_osmo_staked) over (order by days)as total_osmo_staked
   from monthly
   group by 1 order by 1
   ),
ranking as (
   SELECT 
   days,
   validator,
   count(distinct tx_id) as txs,
   sum(osmo_staked) as total_near_delegated,
sum(total_near_delegated) over (partition by validator order by days) as cumulative_near_delegated
FROM monthly 
group by 1,2
),
stats as (
  SELECT
  days,
35 as bizantine_fault_tolerance,
total_osmo_staked,
(total_osmo_staked*bizantine_fault_tolerance)/100 as threshold--,
--sum(total_sol_delegated) over (partition by days order by validator_ranks asc) as total_sol_delegated_by_ranks,
--count(distinct vote_accounts) as validators
from totals
), 
stats2 as (
   select *,
1 as numbering,
sum(numbering) over (partition by days order by cumulative_near_delegated desc) as rank 
from ranking
   ),
stats3 as (
SELECT
days,
validator,
cumulative_near_delegated,
rank,
sum(cumulative_near_delegated) over (partition by days order by rank asc) as total_staked
--count(case when total_staked)
--sum(1) over (partition by days order by stake_rank) as nakamoto_coeff
  from stats2
order by rank asc),
final_nak as (
SELECT
a.days,
validator,
count(case when total_staked <= threshold then 1 end) as nakamoto_coeff
from stats3 a 
join stats b 
on a.days = b.days --where a.days >=CURRENT_DATE-INTERVAL '3 MONTHS'
group by 1,2
order by 1 asc
   )
SELECT
days,
   sum(nakamoto_coeff) as nakamoto_coeff
from final_nak
group by 1 order by 1 asc 

"""

# In[11]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.subheader('Terra general activity metrics regarding transactions')
#st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[22]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = px.area(df, x="days", y="voting_power")

fig.update_layout(
    title='Voting power of the top 66% of the active set validators change',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig.update_yaxes(title_text="Daily voting power", secondary_y=False)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)


# Create figure with secondary y-axis
st.altair_chart(alt.Chart(df2)
        .mark_area()
        .encode(x='days:N', y='power_share:Q',color='ranks')
        .properties(title='Power share distribution per validators rank',width=600))

st.altair_chart(alt.Chart(df3)
        .mark_bar()
        .encode(x='days:N', y='nakamoto_coeff:Q',color='nakamoto_coeff')
        .properties(title='Nakamoto coefficient evolution',width=600))


# In[8]:


st.subheader('Validators activity')

sql="""
WITH
  t1 as (
  select 
distinct proposal_id,
min(block_timestamp)as debut
from osmosis.core.fact_governance_proposal_deposits 
  group by 1
  )
select trunc(debut,'week') as weeks,
count(distinct proposal_id) as new_proposals,
sum(new_proposals) over (order by weeks) as cum_proposals
from t1 group by 1 order by 1 asc
"""

sql2 = f"""
 WITH 
 news as (
 SELECT 
  	  voter as validator_address,
      min(trunc(block_timestamp,'day')) as debut
    FROM osmosis.core.fact_governance_votes
    GROUP BY 1
),
   proposals_info as (
SELECT 
   proposal_id,
    voter,
    block_timestamp,
   tx_id
  FROM osmosis.core.fact_governance_votes
   )
SELECT
trunc(block_timestamp,'day') as date,
   case when datediff('day',debut,date)<30 then 'New validator'
   else 'Old validator' end as type,
   count(distinct voter) as voters,
   count(distinct tx_id) as votes
from proposals_info x
   join news y on voter=validator_address
group by 1,2 order by 1 asc 
  """

sql3="""
 WITH 
 news as (
 SELECT 
  	  voter as validator_address,
      min(trunc(block_timestamp,'day')) as debut
    FROM osmosis.core.fact_governance_votes
    GROUP BY 1
),
   proposals_info as (
SELECT 
   proposal_id,
    voter,
    block_timestamp,
   tx_id
  FROM osmosis.core.fact_governance_votes
   ),
   final as (
SELECT
trunc(block_timestamp,'day') as date,
   case when datediff('day',debut,date)<30 then 'New validator'
   else 'Old validator' end as type,
   voter,
   count(distinct tx_id) as votes
from proposals_info x
   join news y on voter=validator_address
group by 1,2,3 
   )
SELECT
trunc(date,'week') as weeks, type,avg(votes) as avg_votes_per_voter
from final group by 1,2 order by 1 asc 
"""

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()

#Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['weeks'],
                y=df['new_proposals'],
                name='# of proposals',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['weeks'],
                y=df['cum_proposals'],
                name='# of proposals',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Osmosis proposals evolution',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly new proposals", secondary_y=False)
fig3.update_yaxes(title_text="Total new proposals", secondary_y=True)



# Create figure with secondary y-axis
st.altair_chart(alt.Chart(df2)
        .mark_bar()
        .encode(x='date:N', y='voters:Q',color='type')
        .properties(title='Active voters by type of delegator over time',width=600))

st.altair_chart(alt.Chart(df2)
        .mark_line()
        .encode(x='date:N', y='votes:Q',color='type')
        .properties(title='Voting activity by type of delegator over time',width=600))

# Create figure with secondary y-axis
st.altair_chart(alt.Chart(df3)
        .mark_line()
        .encode(x='weeks:N', y='avg_votes_per_voter:Q',color='type')
        .properties(title='Average weekly votes per voter per type of delegator',width=600))


# In[ ]:




