# Complaint Intelligence

A customer complaint analytics and operational prioritization portfolio project using synthetic data.

This project explores how complaint records can be transformed into actionable operational insights — from measuring response and resolution performance to identifying recurring issues, outlet hotspots, and cases that may require greater attention.

## Business Question

**Which complaints and operational areas need attention first?**

Instead of only counting complaints, this project examines:

- Complaint volume and distribution
- First response time
- Resolution time
- Recurring complaint types
- Outlet-level complaint patterns
- Responsible operational areas
- Ticket outcomes
- Operational priority signals

## Analytical Workflow

Raw Complaint Records  
→ Data Preparation  
→ Response & Resolution Metrics  
→ Complaint Pattern Analysis  
→ Outlet & Issue Hotspot Detection  
→ Priority Scoring  
→ Interactive Streamlit Application

## Planned Metrics

### First Response Time

Measures how long it takes from receiving a complaint until the first response.

`Response Time = Response Timestamp - Complaint Timestamp`

### Resolution Time

Measures how long it takes from receiving a complaint until the case is resolved.

`Resolution Time = Resolve Timestamp - Complaint Timestamp`

### Complaint Hotspots

Identifies recurring patterns across:

- Outlet
- Brand
- Complaint type
- Issue detail
- Responsible area

### Operational Priority

A transparent rule-based framework will be used to highlight cases or operational areas that may deserve further review.

The priority score is intended as an analytical aid — not an automated operational decision.

## Tools

- Python
- Pandas
- Streamlit
- GitHub

## Data Privacy

This repository uses fully synthetic complaint data created specifically for this portfolio project.

The project structure is inspired by a previous customer-experience analytics exercise, but no original customer records, personally identifiable information, confidential company data, or proprietary assessment dataset is distributed.

## Disclaimer

The analytical rules, thresholds, and priority framework used in this project are independently designed for educational and portfolio purposes. They should not be interpreted as an official methodology of any company.
