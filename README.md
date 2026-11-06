# EduRisk Analytics

A simple Streamlit student data application.

Run it with:

```powershell
streamlit run app.py
```

# EduRisk Analytics

A student performance analysis web application developed using Python and Streamlit.

## Features

- **Home:** Introduction to the application.
- **Dashboard:** Displays student statistics, filters, and interactive charts.
- **Student Data:** Displays student records.
- **Risk Checker:** Identifies students' academic risk levels.
- **About:** Provides project information.

## Risk Classification

| Condition                                       | Risk Level  |
| ----------------------------------------------- | ----------- |
| Score below 60 OR attendance below 60%          | High Risk   |
| Score below 75 OR attendance below 75%          | Medium Risk |
| Score 75 or higher AND attendance 75% or higher | Low Risk    |

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

```text
EduRiskAnalysis/
├── app.py
├── students.csv
├── requirements.txt
└── README.md
```

## Installation and Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Open the application at `http://localhost:8501`.

## Dataset

The `students.csv` file contains:

- Student Name
- Course
- Score
- Attendance
- Study Hours

## Conclusion

EduRisk Analytics helps users analyze student performance, visualize data, and identify students who may need additional academic support.

## Student Information

- **Name:** [Your Name]
- **Student ID:** [Your Student ID]
- **Course:** Web App Development for Data Science
- **Lab:** Lab 05 – Visualization and Interactivity
