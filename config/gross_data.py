import pandas as pd
import plotly.graph_objects as go

class Data:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df, self.cost = self.load_data()
        self.acre_to_hectare = 2.47105
        self.fluctuation_mapping = {"Low": 0.01, "Moderate": 0.02, "High": 0.03}

    def load_data(self):
        """Load primary data and cost data."""
        df = pd.read_excel(self.file_path)
        cost_data = [
            ["Large-scale", "With Subsidy", 23, 2400, 9600, 1800, 1000, 9750, 6125, 15000, 2557, 48232, 2144, 1],
            ["Large-scale", "Without Subsidy", 23, 2400, 14250, 1800, 1000, 9750, 6125, 15000, 2962, 53287, 2368, 1],
            ["Small-scale", "With Subsidy", 18, 2400, 7100, 1500, 0, 7050, 12000, 10000, 2379, 42429, 2357, 1],
            ["Small-scale", "Without Subsidy", 18, 2400, 11500, 1500, 0, 7050, 12000, 10000, 2628, 47078, 2615, 1],
        ]
        columns = [
            "Scale of Production", "Fertilizer Subsidy", "Average Yield (90kg bags/acre)",
            "Seed Cost (KES)", "Fertilizer Cost (KES)", "Pesticides Cost",
            "Herbicides Cost (KES)", "Machinery Cost (KES)", "Labour Cost (KES)",
            "Landrent Cost (KES)", "Other Costs (KES)", "Total Cost/Acre (KES)",
            "Total Cost/Bag (KES)", "Quantity"
        ]
        cost = pd.DataFrame(cost_data, columns=columns)
        return df, cost

    def filter_data(self, selected_county, selected_value_chain):
        """Filter the main dataset based on county and value chain."""
        filtered_df = self.df.copy()
        if selected_county != "All":
            filtered_df = filtered_df[filtered_df["County"] == selected_county]
        if selected_value_chain != "All":
            filtered_df = filtered_df[filtered_df["Crop Type"] == selected_value_chain]
        return filtered_df
    
    def calculate_gross_margin(self, cost_df, farmgate_price, loss_percentage, own_consumption_percentage):
        gross_output = farmgate_price * (1 - loss_percentage / 100)
        net_output = gross_output * (1 - own_consumption_percentage / 100)
        gross_margin = net_output - cost_df["Cost Per Unit"].sum()
        return gross_output, net_output, gross_margin

    def calculate_aggregate_metrics(self, filtered_df, area_unit="Hectares"):
        """Calculate total production, area, and yield per hectare or acre."""
        total_production = filtered_df["Production (Tonnes)"].sum()
        total_area = filtered_df["Area (Ha)"].sum()
        
        if area_unit == "Acres":
            total_area *= self.acre_to_hectare
        yield_kg = (total_production * 1000) / total_area if total_area else 0

        return {
            "total_production": total_production,
            "total_area": total_area,
            "yield_kg": yield_kg
        }

    def adjust_costs(self, area_unit, exchange_rate, fluctuation_level):
        """
        Adjust costs based on area unit, exchange rate, and fluctuation level.
        """
        multiplier = self.acre_to_hectare if area_unit == "Acres" else 1
        fluctuation = self.fluctuation_mapping[fluctuation_level]

        adjusted_costs = []
        for _, row in self.cost.iterrows():
            adjusted_row = row.copy()
            for col in ["Seed Cost (KES)", "Fertilizer Cost (KES)", "Pesticides Cost",
                        "Herbicides Cost (KES)", "Machinery Cost (KES)", "Labour Cost (KES)",
                        "Landrent Cost (KES)", "Other Costs (KES)"]:
                value = row[col] * multiplier * exchange_rate
                std_dev = value * fluctuation
                adjusted_row[col] = value
                adjusted_row[f"{col}_CI"] = (value - 1.96 * std_dev, value + 1.96 * std_dev)
            adjusted_costs.append(adjusted_row)
        return pd.DataFrame(adjusted_costs)

    def calculate_break_even(self, fixed_costs, variable_cost_per_unit, selling_price_per_unit):
        """
        Calculate break-even quantity and revenue.
        """
        if selling_price_per_unit <= variable_cost_per_unit:
            return {"break_even_quantity": None, "break_even_revenue": None}

        break_even_quantity = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
        break_even_revenue = break_even_quantity * selling_price_per_unit
        return {
            "break_even_quantity": break_even_quantity,
            "break_even_revenue": break_even_revenue
        }

    def plot_break_even(self, fixed_costs, variable_cost_per_unit, selling_price_per_unit):
        """Generate a break-even analysis plot."""
        units = list(range(0, 2000, 10))
        total_costs = [fixed_costs + variable_cost_per_unit * unit for unit in units]
        total_revenue = [selling_price_per_unit * unit for unit in units]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=units, y=total_costs, mode="lines", name="Total Costs"))
        fig.add_trace(go.Scatter(x=units, y=total_revenue, mode="lines", name="Total Revenue"))
        fig.update_layout(
            title="Break-Even Analysis",
            xaxis_title="Units Produced",
            yaxis_title="Costs/Revenue",
            template="plotly_white"
        )
        return fig

    def plot_cost_and_revenue_distribution(self, categories, values):
        """Generate a bar chart for cost and revenue distribution."""
        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=categories, y=values, text=[f"{value:,.2f}" for value in values], textposition="auto")
        )
        fig.update_layout(
            title="Cost and Revenue Distribution",
            xaxis_title="Category",
            yaxis_title="Value",
            template="plotly_white"
        )
        return fig
