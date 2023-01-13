#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import altair as alt
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[9]:


st.title('Governing the Cosmos')


# In[10]:

st.markdown("Cosmos is an ever-expanding ecosystem of interconnected apps and services, built for a decentralized future. Cosmos apps and services connect using IBC, the Inter-Blockchain Communication protocol. This innovation enables you to freely exchange assets and data across sovereign, decentralized blokchains [1](https://cosmos.network/).")

st.markdown("Throughout the cosmos, ecosystem builders are molding the future of their app chain by actively participating in governance and debating actionable measures. Every chain is different so let's take a peak under the hood and compare governance performance on Osmosis, Cosmos, Terra and Axelar chains.")

st.markdown("So, the question is... How active and engaged are users? How many unique voters are there on each chain? How is voting power distributed? What chain has been the most active in proposals?")

# In[11]:
st.markdown("The main idea of this app is to show an overview of how the staking and governance is being used and developed on each Cosmos chain to see each performance and activity. You can find information about each different chain by navigating on the sidebar pages.")


# In[12]:


st.markdown("These includes:") 
st.markdown("1. **_Osmosis Governance activity_**") 
st.markdown("2. **_Cosmos Governance activity_**")
st.markdown("3. **_Terra Governance activity_**")
st.markdown("4. **_Axelar Governance activity_**")


# In[ ]:




