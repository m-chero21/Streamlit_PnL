import pandas as pd

class Data:
    def __init__(self):
        self.df = self.get_dataframe()

    @staticmethod
    def adjust_percentages(biotech, opv):
        """Calculate adjusted OPV and Hybrid percentages."""
        remaining = 100 - biotech
        adjusted_opv = min(opv, remaining)
        adjusted_hybrid = remaining - adjusted_opv
        return adjusted_opv, adjusted_hybrid

    def update_percentages(self, biotech_2023, opv_2023, biotech_2028, opv_2028):
        """Update OPV, Hybrid, and Biotech percentages for 2023 and 2028."""
        for year, biotech, opv in [("2023", biotech_2023, opv_2023), ("2028", biotech_2028, opv_2028)]:
            self.df[f"{year} % of OPV"], self.df[f"{year} % of Hybrid"] = self.adjust_percentages(biotech, opv)
            self.df[f"{year} % of Biotech"] = biotech

    def calculate_seed_requirements(self, year, seed_rate):
        """Calculate seed requirements (kg) for OPV, Hybrid, and Biotech."""
        for category in ["OPV", "Hybrid", "Biotech"]:
            self.df[f"{year} kg seed {category}"] = (
                self.df[f"Hectares {year}"] *
                self.df[f"{year} % of {category}"] / 100 *
                seed_rate
            ).round(1)

    def calculate_production_volume(self, year):
        """Calculate production volume for the specified year."""
        self.df[f"Production Volume {year}"] = (
            self.df["Avg Yield OPV"] * self.df[f"Hectares {year}"] * self.df[f"{year} % of OPV"] / 100 +
            self.df["Avg Yield Hybrid"] * self.df[f"Hectares {year}"] * self.df[f"{year} % of Hybrid"] / 100 +
            self.df["Avg Yield Biotech"] * self.df[f"Hectares {year}"] * self.df[f"{year} % of Biotech"] / 100
        ).round(1)

    def calculate_projections(self, seed_rate):
        """Calculate hectares, seed requirements, and production volumes for 2023 and 2028."""
        # Calculate Hectares 2028
        self.df["Hectares 2028"] = (
            self.df["Hectares 2023"] * (1 + self.df["G% Hectares (2023-2028)"] / 100)
        ).round(1)

        # Calculate seed requirements and production volumes for 2023 and 2028
        for year in ["2023", "2028"]:
            self.calculate_seed_requirements(year, seed_rate)
            self.calculate_production_volume(year)

    def calculate_summary_metrics(self, selected_counties=None):
        """Calculate combined summary metrics for national and sub-national levels."""
        def calculate_metrics(df):
            """Helper to calculate summary metrics for a given DataFrame."""
            total_hectares = df["Hectares 2023"].sum()
            biotech_hectares_2028 = (df["Hectares 2028"] * df["2028 % of Biotech"] / 100).sum()
            percent_biotech = (biotech_hectares_2028 / total_hectares * 100) if total_hectares != 0 else 0
            return {
                "Area under maize (Ha)": total_hectares,
                "Area under biotech seed (Ha)": biotech_hectares_2028,
                "Area under biotech seed (%)": percent_biotech,
                "Biotech seed requirement 2028 (Kg)": df["2028 kg seed Biotech"].sum(),
                "OPV seed requirement 2028 (Kg)": df["2028 kg seed OPV"].sum(),
                "Hybrid seed requirement 2028 (Kg)": df["2028 kg seed Hybrid"].sum(),
            }

        # Calculate national metrics
        national_metrics = calculate_metrics(self.df)

        # Calculate sub-national metrics if counties are selected
        if selected_counties:
            filtered_df = self.df[self.df["County"].isin(selected_counties)]
            sub_national_metrics = calculate_metrics(filtered_df)
        else:
            sub_national_metrics = {key: "N/A" for key in national_metrics.keys()}

        # Combine results into a DataFrame
        summary_data = {
            "Indicator": list(national_metrics.keys()),
            "National": [f"{value:,.1f}" if isinstance(value, (int, float)) else value for value in national_metrics.values()],
            "Sub-National": [
                f"{value:,.1f}" if isinstance(value, (int, float)) else value
                for value in sub_national_metrics.values()
            ],
        }

        return pd.DataFrame(summary_data)

    @staticmethod
    def get_dataframe():
        """Return the processed DataFrame."""
        kenyan_counties = [
            "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet", "Embu",
            "Garissa", "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho",
            "Kiambu", "Kilifi", "Kirinyaga", "Kisii", "Kisumu", "Kitui",
            "Kwale", "Laikipia", "Lamu", "Machakos", "Makueni", "Mandera",
            "Meru", "Migori", "Marsabit", "Mombasa", "Murang'a", "Nairobi",
            "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri",
            "Samburu", "Siaya", "Taita-Taveta", "Tana River", "Tharaka Nithi",
            "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot"
        ]
        data = {
            "County": kenyan_counties,
            "Hectares 2023": [
                42501, 27250, 92847, 44097, 43133, 34500, 142, 78795, 256, 33241, 87532, 40643,
                30537, 95674, 38467, 66221, 62195, 83618, 60518, 29596, 45800, 138830, 136912,
                3209, 142379, 78567, 2184, 876, 68399, 758, 71470, 67429, 132396, 48175, 20716,
                31317, 6448, 77550, 13596, 5734, 26617, 125065, 1750, 117923, 24921, 132, 49097
            ],
            "G% Hectares (2023-2028)": [0] * len(kenyan_counties),
            "2023 % of OPV": [30] * len(kenyan_counties),
            "2023 % of Hybrid": [70] * len(kenyan_counties),
            "2023 % of Biotech": [0] * len(kenyan_counties),
            "2028 % of OPV": [30] * len(kenyan_counties),
            "2028 % of Hybrid": [70] * len(kenyan_counties),
            "2028 % of Biotech": [0] * len(kenyan_counties),
            "Avg Yield OPV": [
                0.67, 0.70, 0.72, 0.48, 1.04, 0.36, 0.28, 0.44, 0.21, 0.37, 0.45, 0.82,
                0.29, 0.26, 0.39, 0.54, 0.51, 0.13, 0.30, 0.45, 0.49, 0.38, 0.18, 0.26,
                0.05, 0.32, 0.39, 0.30, 0.25, 0.27, 0.90, 0.71, 0.71, 0.39, 0.68, 0.34,
                0.71, 0.45, 0.27, 0.31, 0.38, 1.07, 0.23, 1.21, 0.36, 0.08, 0.59
            ],
            "Avg Yield Hybrid": [
                1.56, 1.62, 1.68, 1.13, 2.44, 0.84, 0.65, 1.03, 0.48, 0.86, 1.06, 1.91,
                0.68, 0.60, 0.90, 1.26, 1.18, 0.30, 0.71, 1.05, 1.14, 0.88, 0.42, 0.60,
                0.11, 0.74, 0.90, 0.70, 0.58, 0.62, 2.11, 1.66, 1.66, 0.92, 1.58, 0.79,
                1.66, 1.04, 0.64, 0.72, 0.89, 2.51, 0.53, 2.83, 0.83, 0.18, 1.37
            ],
            "Avg Yield Biotech": [0] * len(kenyan_counties),
        }
        return pd.DataFrame(data)

