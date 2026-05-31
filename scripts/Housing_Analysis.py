#!/usr/bin/env python
# coding: utf-8

# **Part 3 - Data Analysis**
# 
# The following SQL query was used to join the four source tables on the composite key (city, month_booking, landlord_type, listing_type) and filter for Madrid:
# 
# ```sql
# SELECT 
#     d.city,
#     d.month_booking,
#     d.landlord_type,
#     d.listing_type,
#     d.visitors,
#     d.searchers,
#     d.applicants,
#     o.bookings,
#     o.revenue_eur,
#     m.commission_rate_pct,
#     m.booking_fee_eur,
#     m.avg_revenue_per_booking_eur,
#     m.avg_rent_eur,
#     s.available_listings,
#     s.created_listings
# FROM data_demand d
# LEFT JOIN data_key_outcomes o 
#     ON d.city = o.city 
#     AND d.month_booking = o.month_booking
#     AND d.landlord_type = o.landlord_type
#     AND d.listing_type = o.listing_type
# LEFT JOIN data_monetisation m 
#     ON d.city = m.city 
#     AND d.month_booking = m.month_booking
#     AND d.landlord_type = m.landlord_type
#     AND d.listing_type = m.listing_type
# LEFT JOIN data_supply s 
#     ON d.city = s.city 
#     AND d.month_booking = s.month_booking
#     AND d.landlord_type = s.landlord_type
#     AND d.listing_type = s.listing_type
# WHERE d.city = 'Madrid'
# ```
# 
# The output was exported to Excel and loaded into this notebook for analysis.

# In[1]:


import pandas as pd
df = pd.read_excel(r"C:\Users\pandi\Documents\Python Scripts\HousingAnywhere\HousingAnywhere_Madrid_Data.xlsx")

df.head()


# In[2]:


# Check the data loaded correctly
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nDate range:", df['month_booking'].min(), "to", df['month_booking'].max())
print("\nLandlord types:", df['landlord_type'].unique())
print("\nListing types:", df['listing_type'].unique())
print("\nNull values:\n", df.isnull().sum())


# In[23]:


df['year'] = df['month_booking'].dt.year

annual = df.groupby('year').agg(
    total_visitors = ('visitors', 'sum'),
    total_searchers = ('searchers', 'sum'),
    total_applicants = ('applicants', 'sum'),
     total_bookings = ('bookings', 'sum'),
    total_revenue = ('revenue_eur', 'sum')
).reset_index()

print(annual)


# In[36]:


import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(12, 7))
fig.suptitle('Madrid: Visitor to Booking Funnel 2023–2025', fontsize=16, fontweight='bold')

years = annual['year'].astype(str)
x = np.arange(len(years))
width = 0.2

metrics = [
    ('total_visitors', 'Visitors (K)', '#4C9BE8'),
    ('total_searchers', 'Searchers (K)', '#2ECC71'),
    ('total_applicants', 'Applicants (K)', '#F39C12'),
    ('total_bookings', 'Bookings (K)', '#E74C3C')
]

bar_positions = {}

for i, (col, label, color) in enumerate(metrics):
    values = annual[col] / 1000
    positions = x + (i - 1.5) * width
    bars = ax.bar(positions, values, width, label=label, color=color, alpha=0.8)
    bar_positions[col] = (positions, values)
    
    
    for j, (pos, val) in enumerate(zip(positions, values)):
        ax.text(pos, val + 5,
                f'{val:.0f}K', ha='center', fontsize=8, color='gray')

# Add connecting arrows between bars of same category
for col, color in [(m[0], m[2]) for m in metrics]:
    positions, values = bar_positions[col]
    for j in range(1, len(years)):
        growth = ((values.iloc[j] - values.iloc[j-1]) / values.iloc[j-1]) * 100
        x_start = positions[j-1] + width/2
        x_end = positions[j] - width/2
        y_mid = max(values.iloc[j], values.iloc[j-1]) + 20

        ax.annotate('',
                    xy=(x_end, values.iloc[j] + 5),
                    xytext=(x_start, values.iloc[j-1] + 5),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

        ax.text((x_start + x_end) / 2, y_mid,
                f'+{growth:.0f}%',
                ha='center', fontsize=8, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel('Volume (thousands)')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('slide1_funnel.png', dpi=150, bbox_inches='tight')
plt.show()


# Madrid shows strong top-of-funnel growth between 2023 and 2025:
# - Visitors grew **+58%** (593K → 936K)
# - Searchers grew **+49%** (214K → 318K)
# 
# However, growth slows significantly at the bottom of the funnel:
# - Applicants grew only **+29%** (47K → 61K)
# - Bookings grew only **+17%** (11K → 13K)
# 
# **Key insight:** 
# Madrid is successfully attracting more visitors YoY, but the platform is losing a big proportion of them before they complete a booking. The gap between visitor growth (+58%) and booking growth (+17%) suggests either:
# - Supply is not keeping up with demand
# - There is friction in the matching or application process
# - Listings are not meeting tenant expectations

# In[43]:


# Check revenue vs bookings growth
print("Revenue growth 2023-2025:", 
      round((annual['total_revenue'].iloc[-1] - annual['total_revenue'].iloc[0]) / annual['total_revenue'].iloc[0] * 100, 1), "%")

print("Booking growth 2023-2025:", 
      round((annual['total_bookings'].iloc[-1] - annual['total_bookings'].iloc[0]) / annual['total_bookings'].iloc[0] * 100, 1), "%")

print("Revenue per booking 2023:", round(annual['total_revenue'].iloc[0] / annual['total_bookings'].iloc[0], 2))
print("Revenue per booking 2025:", round(annual['total_revenue'].iloc[-1] / annual['total_bookings'].iloc[-1], 2))


# In[47]:


# Revenue by landlord type per year
landlord_revenue = df.groupby(['year', 'landlord_type']).agg(
    total_revenue=('revenue_eur', 'sum'),
    total_bookings=('bookings', 'sum')
).reset_index()

print(landlord_revenue)

# Revenue by listing type per year
listing_revenue = df.groupby(['year', 'listing_type']).agg(
    total_revenue=('revenue_eur', 'sum'),
    total_bookings=('bookings', 'sum')
).reset_index()

print(listing_revenue)


# In[49]:


print("=== LANDLORD TYPE GROWTH ===")
for landlord in ['PBSA', 'Private Landlord', 'Property Manager']:
    data = landlord_revenue[landlord_revenue['landlord_type'] == landlord]
    rev_2023 = data[data['year']==2023]['total_revenue'].values[0]
    rev_2025 = data[data['year']==2025]['total_revenue'].values[0]
    growth = (rev_2025 - rev_2023) / rev_2023 * 100
    print(f"{landlord}: +{growth:.1f}%")

print("\n=== LISTING TYPE GROWTH ===")
for listing in ['Apartment', 'Room', 'Studio']:
    data = listing_revenue[listing_revenue['listing_type'] == listing]
    rev_2023 = data[data['year']==2023]['total_revenue'].values[0]
    rev_2025 = data[data['year']==2025]['total_revenue'].values[0]
    growth = (rev_2025 - rev_2023) / rev_2023 * 100
    print(f"{listing}: +{growth:.1f}%")


# In[51]:


fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Madrid: What is Driving Revenue Growth?', fontsize=16, fontweight='bold')

years_list = [2023, 2024, 2025]
colors_landlord = {'PBSA': '#4C9BE8', 'Private Landlord': '#2ECC71', 'Property Manager': '#E74C3C'}
colors_listing = {'Apartment': '#F39C12', 'Room': '#9B59B6', 'Studio': '#1ABC9C'}

# Chart 1: Revenue by landlord type
bottom = np.zeros(3)
for landlord, color in colors_landlord.items():
    values = [landlord_revenue[(landlord_revenue['year']==y) & 
              (landlord_revenue['landlord_type']==landlord)]['total_revenue'].values[0]/1000000 
              for y in years_list]
    axes[0].bar(range(3), values, bottom=bottom, label=landlord, color=color, alpha=0.8)
    for i, (val, bot) in enumerate(zip(values, bottom)):
        if val > 0.05:
            axes[0].text(i, bot + val/2, f'€{val:.2f}M', 
                        ha='center', fontsize=8, fontweight='bold', color='white')
    bottom += np.array(values)

axes[0].set_xticks(range(3))
axes[0].set_xticklabels(['2023', '2024', '2025'])
axes[0].set_title('By Landlord Type')
axes[0].set_ylabel('Revenue (€M)')
axes[0].legend(loc='upper left', fontsize=8)

# Chart 2: Revenue by listing type
bottom = np.zeros(3)
for listing, color in colors_listing.items():
    values = [listing_revenue[(listing_revenue['year']==y) & 
              (listing_revenue['listing_type']==listing)]['total_revenue'].values[0]/1000000 
              for y in years_list]
    axes[1].bar(range(3), values, bottom=bottom, label=listing, color=color, alpha=0.8)
    for i, (val, bot) in enumerate(zip(values, bottom)):
        if val > 0.05:
            axes[1].text(i, bot + val/2, f'€{val:.2f}M',
                        ha='center', fontsize=8, fontweight='bold', color='white')
    bottom += np.array(values)

axes[1].set_xticks(range(3))
axes[1].set_xticklabels(['2023', '2024', '2025'])
axes[1].set_title('By Listing Type')
axes[1].set_ylabel('Revenue (€M)')
axes[1].legend(loc='upper left', fontsize=8)

plt.tight_layout()
plt.savefig('slide2_segments.png', dpi=150, bbox_inches='tight')
plt.show()


# Despite booking growth of only **+17%**, revenue grew significantly faster at **+37%** between 2023 and 2025. This means HousingAnywhere Madrid is earning more per booking (revenue per booking increased from €203 in 2023 to €238 in 2025).
# 
# **What is driving this?**
# 
# By landlord type: All three segments are growing at similar rates, with Property Managers showing the strongest growth at +37.8%, slightly ahead of Private Landlords (+36.5%) and PBSA (+30.4%). Private Landlords remain the dominant revenue source, contributing approximately 63% of total revenue.
# 
# By listing type: Apartments are the fastest growing segment at +39.3%, outpacing Rooms (+34.5%) and Studios (+33.6%). Apartments also command the highest average rent, which explains the increase in revenue per booking over time.
# 
# **Key insight:** 
# Madrid's revenue growth is being driven by a shift toward higher-value listings particularly apartments, and growing Property Manager supply. Even as booking volume growth slows, the platform is capturing more value per transaction.

# In[52]:


# Monthly revenue across all years
df['month'] = df['month_booking'].dt.month
df['month_name'] = df['month_booking'].dt.strftime('%b')

seasonality = df.groupby(['year', 'month', 'month_name']).agg(
    total_revenue=('revenue_eur', 'sum'),
    total_bookings=('bookings', 'sum'),
    total_visitors=('visitors', 'sum')
).reset_index().sort_values(['year', 'month'])

# Average by month across all years
avg_seasonality = df.groupby(['month', 'month_name']).agg(
    avg_revenue=('revenue_eur', 'mean'),
    avg_bookings=('bookings', 'mean'),
    avg_visitors=('visitors', 'mean')
).reset_index().sort_values('month')

print(avg_seasonality)


# In[58]:


fig, ax1 = plt.subplots(figsize=(14, 7))
fig.suptitle('Madrid Seasonality: Academic Calendar Drives Demand', 
             fontsize=16, fontweight='bold')

months = avg_seasonality['month_name']
x = np.arange(len(months))

bars = ax1.bar(x, avg_seasonality['avg_bookings'], color='#4C9BE8', 
               alpha=0.7, label='Avg Bookings')
ax1.set_ylabel('Average Bookings', color='#4C9BE8')
ax1.set_xticks(x)
ax1.set_xticklabels(months)
ax1.tick_params(axis='y', labelcolor='#4C9BE8')

for bar, val in zip(bars, avg_seasonality['avg_bookings']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.0f}', ha='center', fontsize=8, color='#4C9BE8')

ax2 = ax1.twinx()
ax2.plot(x, avg_seasonality['avg_visitors'], marker='o', linewidth=2.5, 
         markersize=8, color='#E74C3C', label='Avg Visitors')
ax2.set_ylabel('Average Visitors', color='#E74C3C')
ax2.tick_params(axis='y', labelcolor='#E74C3C')

for i, val in enumerate(avg_seasonality['avg_visitors']):
    ax2.text(i, val + 100, f'{val:.0f}', ha='center', 
             fontsize=8, color='#E74C3C')

ax1.axvspan(0, 1.5, alpha=0.1, color='green', label='Jan/Feb intake')
ax1.axvspan(7.5, 9.5, alpha=0.1, color='orange', label='Sep/Oct intake')
ax1.axvspan(5, 7.5, alpha=0.1, color='red', label='Summer paradox')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)

ax1.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('slide3_seasonality.png', dpi=150, bbox_inches='tight')
plt.show()


# Madrid's booking patterns are strongly driven by the academic calendar, not general travel trends. 2 clear demand peaks emerge every year:
# 
# **January/February intake**
# The start of the spring semester drives a strong booking spike. Average bookings reach 138-146 per month during this period.
# 
# **September/October intake**
# The most important period of the year, the start of the autumn semester. September is the single strongest month with 134 average bookings, coinciding with the highest visitor traffic of the year (8,680 avg visitors).
# 
# **The Summer Paradox**
# June, July and August present an interesting contradiction:
# - Visitors are at their HIGHEST (7,600 - 8,650 per month)
# - But bookings are at their LOWEST (62 - 75 per month)
# 
# This suggests summer traffic is driven by early browsers and tourists rather than tenants with immediate booking intent. Conversion during this period is significantly below the annual average.
# 
# **Key insight:** 
# HousingAnywhere Madrid should align landlord acquisition campaigns and marketing investment with academic calendar peaks particularly July/August when future students begin researching, and September when they commit to booking.

# In[55]:


# Supply vs Demand exploration
supply_demand = df.groupby(['year', 'month']).agg(
    total_available_listings=('available_listings', 'sum'),
    total_created_listings=('created_listings', 'sum'),
    total_applicants=('applicants', 'sum'),
    total_bookings=('bookings', 'sum')
).reset_index().sort_values(['year', 'month'])

# Annual summary
annual_supply = df.groupby('year').agg(
    total_available_listings=('available_listings', 'sum'),
    total_created_listings=('created_listings', 'sum'),
    total_applicants=('applicants', 'sum'),
    total_bookings=('bookings', 'sum')
).reset_index()

# Supply utilisation = bookings / available listings
annual_supply['utilisation_rate'] = annual_supply['total_bookings'] / annual_supply['total_available_listings'] * 100

# Demand pressure = applicants / available listings
annual_supply['demand_pressure'] = annual_supply['total_applicants'] / annual_supply['total_available_listings']

print(annual_supply)


# In[57]:


fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('Madrid: Supply vs Demand 2023–2025', fontsize=16, fontweight='bold')

years_list = ['2023', '2024', '2025']
x = np.arange(len(years_list))
width = 0.35

# Available listings vs Applicants
bars1 = ax.bar(x - width/2, annual_supply['total_available_listings']/1000, 
               width, label='Available Listings (K)', color='#4C9BE8', alpha=0.8)
bars2 = ax.bar(x + width/2, annual_supply['total_applicants']/1000, 
               width, label='Applicants (K)', color='#E74C3C', alpha=0.8)

# Add labels and YoY growth
for i, (bar, val) in enumerate(zip(bars1, annual_supply['total_available_listings']/1000)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.0f}K', ha='center', fontsize=8, fontweight='bold', color='#4C9BE8')
    if i > 0:
        growth = ((annual_supply['total_available_listings'].iloc[i] - 
                   annual_supply['total_available_listings'].iloc[i-1]) / 
                   annual_supply['total_available_listings'].iloc[i-1]) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                f'+{growth:.0f}%', ha='center', fontsize=9, 
                fontweight='bold', color='white')

for i, (bar, val) in enumerate(zip(bars2, annual_supply['total_applicants']/1000)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.0f}K', ha='center', fontsize=8, fontweight='bold', color='#E74C3C')
    if i > 0:
        growth = ((annual_supply['total_applicants'].iloc[i] - 
                   annual_supply['total_applicants'].iloc[i-1]) / 
                   annual_supply['total_applicants'].iloc[i-1]) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                f'+{growth:.0f}%', ha='center', fontsize=9, 
                fontweight='bold', color='white')

ax.set_xticks(x)
ax.set_xticklabels(years_list)
ax.set_title('Available Listings vs Applicants')
ax.set_ylabel('Volume (thousands)')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('slide4_supply.png', dpi=150, bbox_inches='tight')
plt.show()


# Madrid's supply has grown significantly between 2023 and 2025:
# - Available listings increased by **+75%** (25,934 → 45,518)
# - New listings created grew from 2,763 in 2023 to 5,116 in 2025
# 
# However, demand growth is not keeping pace with supply expansion:
# - Applicants grew only **+29%** (47,375 → 60,953)
# - Listing utilisation rate declined from **42.7%** in 2023 to **28.5%** in 2025
# 
# **What this means:**
# In 2023, roughly 43 out of every 100 listings received a booking. By 2025, that number dropped to only 28 out of every 100.
# 
# A growing number of listings are sitting empty and not converting into bookings. This suggests that while HousingAnywhere is successfully attracting more landlords to the platform, the quality or positioning of new listings may not be meeting tenant expectations.
# 
# **Key insight:** 
# The challenge in Madrid is no longer supply shortage, it is supply quality and matching efficiency. New listings need better onboarding, pricing guidance, and optimisation to convert applicants into bookings at the same rate as established listings.

# In[59]:


# Average rent trends over time
rent_trends = df.groupby(['year', 'month']).agg(
    avg_rent=('avg_rent_eur', 'mean')
).reset_index()

# Annual average rent
annual_rent = df.groupby('year').agg(
    avg_rent=('avg_rent_eur', 'mean')
).reset_index()

# Rent by listing type
rent_by_listing = df.groupby(['year', 'listing_type']).agg(
    avg_rent=('avg_rent_eur', 'mean')
).reset_index()

# Rent by landlord type
rent_by_landlord = df.groupby(['year', 'landlord_type']).agg(
    avg_rent=('avg_rent_eur', 'mean')
).reset_index()

print("=== ANNUAL AVERAGE RENT ===")
print(annual_rent)
print("\n=== RENT BY LISTING TYPE ===")
print(rent_by_listing)
print("\n=== RENT BY LANDLORD TYPE ===")
print(rent_by_landlord)


# In[60]:


fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Madrid: Rising Rents 2023–2025', fontsize=16, fontweight='bold')

years_list = ['2023', '2024', '2025']
x = np.arange(len(years_list))
width = 0.25

# Chart 1: Overall average rent trend
axes[0].plot(years_list, annual_rent['avg_rent'], marker='o', 
             linewidth=2.5, markersize=10, color='#E74C3C')
axes[0].set_title('Average Rent (€/month)')
axes[0].set_ylabel('Average Rent (€)')
axes[0].set_ylim(900, 1500)
axes[0].grid(axis='y', alpha=0.3)

for i, val in enumerate(annual_rent['avg_rent']):
    axes[0].text(i, val + 10, f'€{val:.0f}', ha='center',
                fontsize=10, fontweight='bold', color='#E74C3C')
    if i > 0:
        growth = ((annual_rent['avg_rent'].iloc[i] - annual_rent['avg_rent'].iloc[i-1]) / 
                   annual_rent['avg_rent'].iloc[i-1]) * 100
        axes[0].text(i - 0.5, (annual_rent['avg_rent'].iloc[i] + 
                    annual_rent['avg_rent'].iloc[i-1])/2 + 20,
                    f'+{growth:.1f}%', ha='center', fontsize=9,
                    fontweight='bold', color='green',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

# Chart 2: Rent by listing type
colors_listing = {'Apartment': '#F39C12', 'Room': '#9B59B6', 'Studio': '#1ABC9C'}

for i, (listing, color) in enumerate(colors_listing.items()):
    values = rent_by_listing[rent_by_listing['listing_type']==listing]['avg_rent']
    axes[1].plot(years_list, values, marker='o', linewidth=2.5, 
                markersize=8, color=color, label=listing)
    for j, val in enumerate(values):
        axes[1].text(j, val + 15, f'€{val:.0f}', ha='center',
                    fontsize=8, fontweight='bold', color=color)

axes[1].set_title('Average Rent by Listing Type (€/month)')
axes[1].set_ylabel('Average Rent (€)')
axes[1].grid(axis='y', alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.savefig('slide5_rent.png', dpi=150, bbox_inches='tight')
plt.show()


# Average rents in Madrid have increased significantly between 2023 and 2025:
# - Overall average rent grew from **€1,099** to **€1,327**, an increase of **+20.8%** in just 2 years
# - The increase is consistent across all listing types and landlord types
# 
# **Rent growth by listing type:**
# - Apartments: €1,687 → €2,043 (**+21%**)
# - Studios: €950 → €1,146 (**+21%**)
# - Rooms: €660 → €794 (**+20%**)
# 
# **The connection to supply and utilisation:**
# When read alongside previous chart, a clear picture emerges. Supply grew **+75%** and rents grew **+21%** but applicants only grew **+29%** and utilisation dropped from **42.7%** to **28.5%**.
# 
# Rising rents are likely contributing to the declining utilisation rate. Tenants are browsing and applying but not completing bookings because listings are becoming increasingly unaffordable.
# 
# This is consistent with HousingAnywhere's own research, which identifies high rental prices and lack of affordable properties as the most common barriers for young tenants in Europe.
# 
# **Key insight:** 
# Madrid faces a growing affordability gap. More listings are available than ever before, but rising rents are pricing out the core tenant audience, the international students and young professionals with limited budgets.

# Based on the analysis of Madrid's performance between 2023 and 2025, 
# three priority recommendations emerge:
# 
# **Recommendation 1 - Improve Funnel Conversion Through Listing Quality**
# 
# **What:**
# Introduce a listing quality score combining completeness, photos, response time, and pricing competitiveness. Prioritise high-scoring listings in search results and provide landlords with actionable optimisation tips.
# 
# **Why:**
# Visitors grew +58% but bookings only grew +17%. A growing proportion of applicants are not converting into bookings. With utilisation dropping from 42.7% to 28.5%, many listings are clearly not meeting tenant expectations.
# 
# **Expected impact:**
# Even a 5% improvement in applicant-to-booking conversion would generate approximately 3,000 additional bookings annually.
# 
# 
# 
# **Recommendation 2 - Align Acquisition and Marketing with Academic Calendar**
# 
# **What:**
# Concentrate landlord acquisition campaigns in May-July, ahead of the September peak. Launch tenant re-engagement campaigns in June-August to convert summer browsers into autumn bookings.
# 
# **Why:**
# September and January/February are the strongest booking months, driven by university intake. Summer months show high visitor traffic (8,600+ avg visitors) but critically low bookings (62-75 avg per month) representing a significant missed conversion opportunity.
# 
# **Expected impact:** 
# Capturing even 10% of summer browsers as autumn bookings could add 800+ bookings during the peak September period.
# 
# 
# **Recommendation 3 - Address the Affordability Gap**
# 
# **What:**
# Introduce a budget-friendly listing category or affordability filter for tenants. Incentivise landlords to offer competitive pricing through featured placement or reduced commission rates for listings priced below market average.
# 
# **Why:** 
# Average rents rose +20.8% in two years (€1,099 → €1,327) while the core tenant audience (international students and young professionals) has limited budgets. This affordability gap is directly contributing to declining utilisation and conversion rates.
# 
# **Expected impact:**
# Reducing price-driven drop-off in the application funnel could improve conversion rates and reactivate the growing pool of unlisted supply.
