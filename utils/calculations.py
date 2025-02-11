import numpy as np
import plotly.graph_objects as go

def adjust_percentages(biotech, opv, country):
    remaining = 100 - biotech  # Remaining percentage after Biotech
    
    if country == "Nigeria":
        opv_start = 90
        hybrid_start = 10
        opv_ratio = 0.9  # 90% of remaining
        hybrid_ratio = 0.1  # 10% of remaining
    else:
        opv_start = 30
        hybrid_start = 70
        opv_ratio = 0.3  # 30% of remaining
        hybrid_ratio = 0.7  # 70% of remaining

    # Start with the predefined OPV and Hybrid values when Biotech is 0
    if biotech == 0:
        adjusted_opv = opv_start
        adjusted_hybrid = hybrid_start
    else:
        adjusted_opv = min(opv, remaining)  # OPV takes as much as possible
        extra_remaining = remaining - adjusted_opv
        
        # Split the extra remaining percentage
        adjusted_opv += opv_ratio * extra_remaining
        adjusted_hybrid = hybrid_ratio * extra_remaining

    return round(adjusted_opv), round(adjusted_hybrid)

def update_combined_summary_metrics(filtered_c_df, selected_counties, new_biotech_percentage, pd, st):
    total_hectares_national = filtered_c_df["Hectares 2023"].sum()
    opv_seed_2028_national = filtered_c_df["2028 kg seed OPV"].sum()
    hybrid_seed_2028_national = filtered_c_df["2028 kg seed Hybrid"].sum()
    total_biotech_hectares_2028_national = (
        (filtered_c_df["Hectares 2028"] * filtered_c_df["2028 % of Biotech"] / 100).sum()
    )
    percent_national_hectares_national = (
        (total_biotech_hectares_2028_national / total_hectares_national * 100)
        if total_hectares_national != 0
        else 0
    )
    commercial_seed_2028_national = filtered_c_df["2028 kg seed Biotech"].sum()

    if selected_counties:
        filtered_df = filtered_c_df[filtered_c_df["County/State"].isin(selected_counties)]
        total_hectares_sub = filtered_df["Hectares 2023"].sum()
        opv_seed_2028_sub = filtered_df["2028 kg seed OPV"].sum()
        hybrid_seed_2028_sub = filtered_df["2028 kg seed Hybrid"].sum()
        total_biotech_hectares_2028_sub = (
            (filtered_df["Hectares 2028"] * filtered_df["2028 % of Biotech"] / 100).sum()
        )
        percent_national_hectares_sub = (
            (total_biotech_hectares_2028_sub / total_hectares_sub * 100)
            if total_hectares_sub != 0
            else 0
        )
        commercial_seed_2028_sub = filtered_df["2028 kg seed Biotech"].sum()
    else:
        total_hectares_sub = 0
        opv_seed_2028_sub = 0
        hybrid_seed_2028_sub = 0
        total_biotech_hectares_2028_sub = 0
        percent_national_hectares_sub = 0
        commercial_seed_2028_sub = 0

    summary_data = {
        "Indicator": [
            "Area under maize (Ha)",
            "Area under biotech seed (Ha)",
            "Area under biotech seed (%)",
            "Biotech seed requirement 2028 (Kg)",
            "OPV seed requirement 2028 (Kg)",
            "Hybrid seed requirement 2028 (Kg)",
        ],
        "National": [
            f"{total_hectares_national:,.0f}",
            f"{total_biotech_hectares_2028_national:,.0f}",
            f"{percent_national_hectares_national:.1f}%",
            f"{commercial_seed_2028_national:,.0f}",
            f"{opv_seed_2028_national:,.0f}",
            f"{hybrid_seed_2028_national:,.0f}",
        ],
        "Sub-National":[
            f"{total_hectares_sub:,.0f}" if total_hectares_sub > 0 else "N/A",
            f"{total_biotech_hectares_2028_sub:,.0f}" if total_biotech_hectares_2028_sub > 0 else "N/A",
            f"{percent_national_hectares_sub:.1f}%" if total_hectares_sub > 0 else "N/A",
            f"{commercial_seed_2028_sub:,.0f}" if commercial_seed_2028_sub > 0 else "N/A",
            f"{opv_seed_2028_sub:,.0f}" if opv_seed_2028_sub > 0 else "N/A",
            f"{hybrid_seed_2028_sub:,.0f}" if hybrid_seed_2028_sub > 0 else "N/A",
        ],
    }

    st.markdown(
        """<div class="cost-breakdown-title">Summary</div>""",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(f""" <div class="update-county">
        <b>Updated {', '.join(selected_counties)} , the 2028 Biotech  for the selected county/ies is now: {new_biotech_percentage} %</b>
    </div> """, unsafe_allow_html=True)

    summary_df = pd.DataFrame(summary_data)

    
    html_table = summary_df.to_html(index=False)

   
    html_table = html_table.replace(
        "<thead>", '<thead class="text-align-center;">'
    )
    st.write(summary_df.to_html(index=False), unsafe_allow_html=True)



#______________________________Gross Margin Calculator Functions___________________________________



# Gross Margin Calculation
def calculate_gross_margin(cost_df, yield_kg, farmgate_price, loss_percentage, own_consumption_percentage):
    gross_output = yield_kg * farmgate_price 
    post_harvest_loss = gross_output * (loss_percentage / 100)
    own_consumption = gross_output * (own_consumption_percentage / 100)
    net_output = gross_output - (post_harvest_loss + own_consumption)
    
    total_costs = cost_df["Cost Per Unit"].sum() 
    gross_margin = net_output - total_costs + own_consumption
    real_g_margin= total_costs-gross_output
    return gross_output, net_output, gross_margin, real_g_margin

# Function to calculate Confidence Interval
def calculate_confidence_interval(cost_per_unit, std_dev, quantity):
    # Calculate standard deviation with quantity and fluctuation level
    lower_bound = round(cost_per_unit * quantity - 1.96 * std_dev)  # 95% CI lower bound
    upper_bound = round(cost_per_unit* quantity + 1.96 * std_dev)  # 95% CI upper bound
    return lower_bound, upper_bound 



# Break-Even Analysis
def calculate_break_even(selling_price_per_unit, total_costs, fluctuation_levels,selected_fluctuation):       
    break_even_quantity = total_costs / selling_price_per_unit        
    break_even_revenue = break_even_quantity * selling_price_per_unit
                
    break_even_quantity_std_dev = break_even_quantity * (0.01 * fluctuation_levels[selected_fluctuation])
    worst_case_quantity = break_even_quantity - 1.96 * break_even_quantity_std_dev
    best_case_quantity = break_even_quantity + 1.96 * break_even_quantity_std_dev

    return break_even_quantity, break_even_revenue, worst_case_quantity, best_case_quantity

# Break-Even Plot Function
def plot_break_even(fixed_costs, variable_cost_per_unit, selling_price_per_unit):
    units = np.arange(0, 8000, 10)
    # Compute total costs and revenue
    total_costs = fixed_costs + variable_cost_per_unit * units 
    total_revenue = selling_price_per_unit * units 

    # Find break-even point
    break_even_indices = np.where(total_costs <= total_revenue)[0]

    if break_even_indices.size > 0:
        break_even_index = break_even_indices[0]
        break_even_units = units[break_even_index]
        break_even_revenue = total_revenue[break_even_index]
    else:
        break_even_units = None
        break_even_revenue = None

    break_even_point = (break_even_units, break_even_revenue)
    
    # Create Plotly figure
    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=units,
        y=total_costs,
        mode='lines',
        name='Total Costs',
        line=dict(color='#a4343a', width=2)
    ))

    fig1.add_trace(go.Scatter(
        x=units,
        y=total_revenue,
        mode='lines',
        name='Total Revenue',
        line=dict(color='#37B7C3', width=2)
    ))

    # Plot break-even point if it exists
    if break_even_units is not None and break_even_revenue is not None:
        fig1.add_trace(go.Scatter(
            x=[break_even_units],
            y=[break_even_revenue],
            mode='markers',
            name='Break-Even Point',
            marker=dict(color='#000000', size=10, symbol='x')
        ))

    # Update figure layout
    fig1.update_layout(
        xaxis_title='Units Produced/Sold',
        yaxis_title='Cost/Revenue',
        xaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
        yaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="seaborn",
        width=700,  
        height=600
    )
    return fig1, total_costs, total_revenue, break_even_point 


def plot_cost_and_revenue_distribution(categories, values, currency):
    # Define colors based on whether the value is negative or not
    colors = ['#a4343a' if value < 0 else '#2D9596' for value in values]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values,
                text=[f"{value:,.2f}" for value in values],  
                textposition='auto',
                marker=dict(color=colors)  # Use the colors defined based on value
            )
        ]
    )

    fig.update_layout(
        xaxis_title='Category',
        yaxis_title=f'Value ({currency})',
        xaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
        yaxis=dict(
            title_font=dict(color='black', size=14, family='Arial', weight='bold'),
            tickfont=dict(color='black', size=12)
        ),
        template="seaborn",
        bargap=0.2,
        width=700,   
        height=600   
    )

    return fig
