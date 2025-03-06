# risk_assessment_tool.py

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RiskAssessmentTool:
    def __init__(self):
        self.risk_score = 0

    def assess_risk(self, inflation_rate, unemployment_rate, gdp_growth):
        """Assess risk based on economic indicators."""
        # Simple risk assessment formula
        self.risk_score = (inflation_rate * 0.4) + (unemployment_rate * 0.4) - (gdp_growth * 0.2)

        # Normalize risk score to a scale of 0 to 100
        self.risk_score = max(0, min(100, self.risk_score))
        logging.info(f"Risk assessed: {self.risk_score:.2f} (Inflation: {inflation_rate}, Unemployment: {unemployment_rate}, GDP Growth: {gdp_growth})")
        return self.risk_score

    def provide_recommendations(self):
        """Provide recommendations based on the assessed risk score."""
        if self.risk_score < 30:
            return "Risk is low. Continue current economic policies."
        elif 30 <= self.risk_score < 70:
            return "Moderate risk detected. Consider implementing measures to stimulate growth."
        else:
            return "High risk detected. Urgent measures needed to stabilize the economy."

if __name__ == "__main__":
    # Example usage
    risk_tool = RiskAssessmentTool()

    # Simulated economic indicators
    inflation_rate = 5.0  # Example inflation rate in percentage
    unemployment_rate = 7.0  # Example unemployment rate in percentage
    gdp_growth = 2.0  # Example GDP growth rate in percentage

    # Assess risk
    risk_score = risk_tool.assess_risk(inflation_rate, unemployment_rate, gdp_growth)

    # Provide recommendations
    recommendations = risk_tool.provide_recommendations()
    print(f"Risk Score: {risk_score:.2f}")
    print(f"Recommendations: {recommendations}")
