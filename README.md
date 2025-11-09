Mai Shan Yun Inventory Intelligence Dashboard
Project Overview
The Mai Shan Yun Inventory Intelligence Dashboard is a comprehensive data analytics solution designed to transform raw restaurant operational data into actionable business intelligence. This interactive dashboard empowers restaurant managers to optimize inventory management, minimize waste, prevent stockouts, and make data-driven decisions about purchasing and menu planning.
Purpose
This dashboard addresses critical operational challenges faced by Mai Shan Yun restaurant:

Inventory Optimization: Real-time tracking of ingredient levels to prevent overstocking and shortages
Predictive Analytics: Forecast future ingredient needs based on historical consumption patterns
Cost Management: Identify spending patterns and opportunities for cost reduction
Operational Efficiency: Streamline shipment scheduling and reduce manual tracking overhead
Waste Reduction: Optimize ordering quantities for perishable ingredients like fresh vegetables

Key Insights Discovered
Through analysis of the restaurant's operational data, several critical insights emerged:
Demand Trends

Ramen-based dishes show a 15% upward trend over the past month, indicating growing customer preference
Weekend fried rice orders spike significantly, requiring adjusted inventory levels for Friday through Sunday
Rice noodle dishes are gaining popularity with consistent week-over-week growth of approximately 8%

Inventory Challenges

Eggs represent a critical inventory bottleneck with usage of 42+ units weekly across 17 menu items
Fresh ingredients (green onions, cilantro) have short shelf lives requiring more frequent, smaller shipments
Protein ingredients (beef, chicken, pork) account for approximately 65% of total weekly food costs

Cost Optimization Opportunities

Bulk purchasing contracts for beef and chicken could reduce costs by 10-15%
Current weekly operational food costs estimated at $1,610
Menu items with overlapping ingredients offer better ingredient utilization rates

Shipment Efficiency

Current weekly shipment schedule: 40+ deliveries across 14 ingredient categories
Biweekly shipments for staples (rice, ramen) align well with consumption rates
Fresh produce requires 2-5 weekly shipments due to perishability constraints

Datasets Used
The dashboard integrates multiple data sources from Mai Shan Yun operations:
1. Ingredient Requirements Dataset (MSY Data - Ingredient.csv)

Contains 17 menu items with detailed ingredient breakdowns
Specifies quantities needed per dish for 18 different ingredients
Includes proteins (beef, chicken, pork), carbohydrates (rice, noodles, ramen), vegetables, and garnishes
Critical for calculating consumption rates and predicting ingredient depletion

2. Shipment Schedule Dataset (MSY Data - Shipment.csv)

Documents 14 ingredient categories with delivery frequencies
Includes quantity per shipment, units of measurement, and frequency (weekly, biweekly, monthly)
Essential for tracking supply chain timing and preventing stockouts

Data Integration Methodology
The dashboard combines these datasets through:

Cross-referencing ingredient names between datasets to calculate total weekly consumption
Multiplying per-dish requirements by estimated sales volume to determine aggregate demand
Comparing consumption rates against shipment schedules to identify potential shortages
Analyzing ingredient usage patterns across menu categories to identify optimization opportunities

Technical Implementation
Technology Stack

Frontend: HTML5, CSS3, JavaScript (ES6+)
Visualization: Chart.js 3.9.1 for interactive charts and graphs
Design: Responsive CSS Grid layout with mobile-first approach
Styling: Custom CSS with gradient backgrounds and modern UI components

Architecture
The dashboard is built as a single-page application (SPA) with:

Modular component structure for maintainability
Client-side data processing for instant responsiveness
No backend dependencies for easy deployment
Responsive design supporting desktop, tablet, and mobile viewports

Features Implemented
1. Real-Time Inventory Monitoring

Visual indicators for stock levels across all ingredients
Color-coded alerts (critical, warning, success) for different urgency levels
Percentage-based inventory bars for quick visual assessment

2. Predictive Demand Forecasting

Time-series analysis of historical order data
Linear regression model for 2-week forward predictions
Confidence intervals for forecast accuracy
Separate forecasts for major menu categories (ramen, fried rice, wings, rice noodles)

3. Interactive Multi-Chart Visualizations

Bar charts for ingredient usage comparison
Line charts for sales trends over time
Forecast visualization with actual vs. predicted demand
All charts support hover interactions for detailed data points

4. Shipment Schedule Management

Tabular view of all scheduled deliveries
Next delivery date calculations based on frequency patterns
Overdue shipment highlighting for immediate action

5. Cost Analysis Dashboard

Weekly expenditure breakdown by ingredient category
Visual cost comparison using horizontal bar indicators
Total operational cost summaries
Cost-per-pound and cost-per-unit calculations

6. Multi-Tab Interface

Sales Analysis: Historical performance tracking
Ingredient Matrix: Cross-reference of menu items and ingredients
Demand Forecast: Predictive analytics and trend projections

Setup and Installation
Requirements

Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
JavaScript enabled
No server or backend required

Installation Steps

Download the project files
Extract to a local directory
Open index.html in any modern web browser
No compilation, build process, or dependency installation required
