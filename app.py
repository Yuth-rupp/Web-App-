import html as html_lib

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="EduRisk Analytics - Lab 02",
    page_icon="🎓",
    layout="wide"
)

# ------------------------------------------------------------------
# DESIGN TOKENS  (deep petrol background + sky-blue accent)
# ------------------------------------------------------------------
BG = "#0B1B26"
SURFACE = "#12293A"
SURFACE2 = "#1A3850"
BORDER = "#264A63"
TEXT = "#E8F1F7"
MUTED = "#8FA9BA"
ACCENT = "#38BDF8"

RISK_COLORS = {
    "Low Risk": "#34D399",
    "Medium Risk": "#FBBF24",
    "High Risk": "#F87171",
}
RISK_BG = {
    "Low Risk": "rgba(52, 211, 153, 0.15)",
    "Medium Risk": "rgba(251, 191, 36, 0.15)",
    "High Risk": "rgba(248, 113, 113, 0.15)",
}

ROOT_VARS = f"""
<style>
:root {{
    --bg: {BG};
    --surface: {SURFACE};
    --surface2: {SURFACE2};
    --border: {BORDER};
    --text: {TEXT};
    --muted: {MUTED};
    --accent: {ACCENT};
}}
</style>
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, .stApp, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: var(--bg); color-scheme: dark; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1150px; }

header[data-testid="stHeader"] { background: transparent; }
header[data-testid="stHeader"] * { color: var(--muted); }

/* Make sure all text is readable */
:where(.stApp) :is(h1, h2, h3, h4, p, li, label, span, div, small) { color: var(--text); }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}
.brand { display: flex; gap: 12px; align-items: center; padding: 6px 4px 20px 4px; }
.brand-logo {
    width: 40px; height: 40px; border-radius: 10px;
    background: var(--accent);
    color: #06202E !important;
    font-weight: 700; font-size: 1.15rem;
    display: flex; align-items: center; justify-content: center;
}
.brand-name { font-weight: 700; font-size: 1.15rem; color: var(--text); line-height: 1.1; }
.brand-sub { font-size: 0.8rem; color: var(--muted) !important; }

section[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
section[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 10px 14px;
    border-radius: 10px;
    width: 100%;
    cursor: pointer;
}
section[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }
section[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: var(--surface2); }
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: var(--surface2);
    box-shadow: inset 3px 0 0 var(--accent);
}
section[data-testid="stSidebar"] [role="radiogroup"] label p { font-size: 1rem; font-weight: 500; }

.side-note {
    font-size: 0.85rem;
    color: var(--muted) !important;
    line-height: 1.5;
    margin-top: 24px;
    padding-top: 14px;
    border-top: 1px solid var(--border);
}

/* ---------- Page header ---------- */
.ph {
    display: flex; justify-content: space-between; align-items: flex-end;
    gap: 16px; flex-wrap: wrap; margin-bottom: 1.4rem;
}
.ph-title { font-size: 2rem; font-weight: 700; margin: 0; color: var(--text); line-height: 1.15; }
.ph-desc { color: var(--muted) !important; margin: 6px 0 0 0; font-size: 1.02rem; }
.chip {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 14px; border-radius: 999px;
    background: var(--surface); border: 1px solid var(--border);
    font-size: 0.88rem; color: var(--muted) !important;
}
.chip i { width: 8px; height: 8px; border-radius: 50%; background: #34D399; display: inline-block; }

.sec-title { font-size: 1.15rem; font-weight: 700; margin: 1.8rem 0 0.7rem 0; color: var(--text); }
.card-title { font-size: 1.05rem; font-weight: 700; color: var(--text); margin: 0; }
.card-sub { color: var(--muted) !important; font-size: 0.88rem; margin: 2px 0 10px 0; }

/* ---------- Metric cards ---------- */
.m-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 18px;
}
.m-label {
    display: flex; align-items: center; gap: 8px;
    color: var(--muted) !important; font-size: 0.92rem; font-weight: 500;
}
.dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.m-value { font-size: 2.1rem; font-weight: 700; margin: 6px 0 2px 0; color: var(--text); line-height: 1.1; }
.m-note { color: var(--muted) !important; font-size: 0.85rem; }
.m-track { height: 6px; background: var(--surface2); border-radius: 999px; margin-top: 12px; overflow: hidden; }
.m-track.small { margin-top: 0; width: 90px; height: 5px; }
.m-fill { height: 100%; border-radius: 999px; }

/* ---------- Table ---------- */
.tbl-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: 12px; }
table.tbl { width: 100%; border-collapse: collapse; min-width: 680px; }
.tbl th {
    text-align: left; padding: 12px 16px;
    color: var(--muted); font-weight: 600; font-size: 0.88rem;
    background: var(--surface); border-bottom: 1px solid var(--border);
}
.tbl td { padding: 12px 16px; border-bottom: 1px solid var(--border); color: var(--text); }
.tbl tr:last-child td { border-bottom: none; }
.tbl tbody tr:hover td { background: var(--surface); }
.cell-bar { display: flex; align-items: center; gap: 10px; }
.cell-bar b { width: 30px; font-weight: 600; color: var(--text); }
.pill { display: inline-block; padding: 3px 12px; border-radius: 999px; font-size: 0.85rem; font-weight: 600; }

/* ---------- Risk guide ---------- */
.guide { display: flex; gap: 12px; flex-wrap: wrap; }
.guide.vertical { flex-direction: column; }
.guide-item {
    flex: 1; min-width: 200px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 12px 16px;
}
.g-title { display: flex; align-items: center; gap: 8px; font-weight: 700; color: var(--text); }
.g-text { color: var(--muted) !important; font-size: 0.9rem; margin-top: 2px; }

/* ---------- Welcome / nav cards ---------- */
.welcome {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 18px;
}
.w-title { font-size: 2.2rem; font-weight: 700; color: var(--text); margin: 0 0 6px 0; }
.w-sub { font-size: 1.1rem; color: var(--accent) !important; font-weight: 600; margin: 0 0 12px 0; }
.w-text { color: var(--muted) !important; margin: 0 0 4px 0; font-size: 1.02rem; }
.nav-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;
    color: var(--text);
}
.nav-card span { color: var(--muted) !important; }

/* ---------- Result ---------- */
.result { border-radius: 14px; padding: 22px 26px; margin-top: 16px; border: 1px solid; }
.r-level { font-size: 1.5rem; font-weight: 700; margin: 0 0 10px 0; }
.r-row { display: flex; justify-content: space-between; gap: 16px; padding: 6px 0; color: var(--text); }
.r-row span { color: var(--muted) !important; }

.empty {
    background: var(--surface); border: 1px dashed var(--border);
    border-radius: 12px; padding: 28px; text-align: center;
    color: var(--muted) !important;
}

/* ---------- Inputs & buttons ---------- */
div[data-testid="stForm"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
}
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    background: var(--accent);
    border: none; border-radius: 8px;
    font-weight: 700; padding: 0.5rem 1.3rem;
}
.stButton > button p, .stDownloadButton > button p, .stFormSubmitButton > button p {
    color: #06202E; font-weight: 700;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
    background: #7DD3FC;
}
</style>
"""

st.markdown(ROOT_VARS + CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------
# DATA
# ------------------------------------------------------------------
student_df = pd.DataFrame({
    "Student Name": [
        "Dara",
        "Sophea",
        "Vuthy",
        "Malis",
        "Rithy",
        "Sreyneang",
        "Chan",
        "Bopha"
    ],
    "Course": [
        "Python",
        "Statistics",
        "Python",
        "Database",
        "Web App",
        "Database",
        "Python",
        "Statistics"
    ],
    "Score": [85, 68, 45, 92, 58, 91, 72, 62],
    "Attendance": [90, 75, 50, 95, 60, 94, 80, 88],
    "Study Hours": [12, 8, 3, 15, 5, 14, 9, 7]
})


def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"


student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)


# ------------------------------------------------------------------
# DESIGN HELPERS (display only)
# ------------------------------------------------------------------
def render(markup):
    st.markdown(markup, unsafe_allow_html=True)


def page_header(title, description, chip=None):
    chip_html = f'<span class="chip"><i></i>{chip}</span>' if chip else ""
    render(
        f'<div class="ph"><div>'
        f'<p class="ph-title">{title}</p>'
        f'<p class="ph-desc">{description}</p>'
        f'</div>{chip_html}</div>'
    )


def section_title(text):
    render(f'<div class="sec-title">{text}</div>')


def card_title(title, subtitle=""):
    render(
        f'<p class="card-title">{title}</p>'
        f'<p class="card-sub">{subtitle}</p>'
    )


def metric_card(label, value, note, color, pct=None):
    bar = ""
    if pct is not None:
        pct = max(0, min(100, pct))
        bar = (
            f'<div class="m-track"><div class="m-fill" '
            f'style="width:{pct}%; background:{color};"></div></div>'
        )
    return (
        f'<div class="m-card">'
        f'<div class="m-label"><span class="dot" style="background:{color};"></span>{label}</div>'
        f'<div class="m-value">{value}</div>'
        f'<div class="m-note">{note}</div>'
        f'{bar}</div>'
    )


def value_color(value):
    if value < 60:
        return RISK_COLORS["High Risk"]
    elif value < 75:
        return RISK_COLORS["Medium Risk"]
    return RISK_COLORS["Low Risk"]


def risk_pill(level):
    return (
        f'<span class="pill" style="background:{RISK_BG[level]}; '
        f'color:{RISK_COLORS[level]};">{level}</span>'
    )


def bar_cell(value, suffix=""):
    return (
        f'<div class="cell-bar"><b>{value}{suffix}</b>'
        f'<div class="m-track small"><div class="m-fill" '
        f'style="width:{value}%; background:{value_color(value)};"></div></div></div>'
    )


def html_table(df):
    if len(df) == 0:
        return '<div class="empty">No students match the current filters.</div>'

    columns = [
        "Student Name", "Course", "Score",
        "Attendance", "Study Hours", "Risk Level"
    ]
    head = "".join(f"<th>{c}</th>" for c in columns)

    rows = ""
    for _, r in df.iterrows():
        rows += (
            "<tr>"
            f"<td><b>{html_lib.escape(str(r['Student Name']))}</b></td>"
            f"<td>{html_lib.escape(str(r['Course']))}</td>"
            f"<td>{bar_cell(r['Score'])}</td>"
            f"<td>{bar_cell(r['Attendance'], '%')}</td>"
            f"<td>{r['Study Hours']} h</td>"
            f"<td>{risk_pill(r['Risk Level'])}</td>"
            "</tr>"
        )

    return (
        '<div class="tbl-wrap"><table class="tbl">'
        f"<thead><tr>{head}</tr></thead><tbody>{rows}</tbody>"
        "</table></div>"
    )


def risk_guide(vertical=False):
    css_class = "guide vertical" if vertical else "guide"
    render(
        f"""
        <div class="{css_class}">
        <div class="guide-item">
        <div class="g-title"><span class="dot" style="background:{RISK_COLORS['Low Risk']};"></span>Low Risk</div>
        <div class="g-text">Score and attendance are both 75 or higher</div>
        </div>
        <div class="guide-item">
        <div class="g-title"><span class="dot" style="background:{RISK_COLORS['Medium Risk']};"></span>Medium Risk</div>
        <div class="g-text">Score or attendance is below 75</div>
        </div>
        <div class="guide-item">
        <div class="g-title"><span class="dot" style="background:{RISK_COLORS['High Risk']};"></span>High Risk</div>
        <div class="g-text">Score or attendance is below 60</div>
        </div>
        </div>
        """
    )


def risk_scale():
    return alt.Scale(
        domain=list(RISK_COLORS.keys()),
        range=list(RISK_COLORS.values())
    )


def style_chart(chart):
    return (
        chart
        .configure(background="transparent")
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor=MUTED,
            labelFontSize=12,
            gridColor=BORDER,
            domainColor=BORDER,
            tickColor=BORDER
        )
    )


# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    render(
        '<div class="brand"><div class="brand-logo">E</div>'
        '<div><div class="brand-name">EduRisk</div>'
        '<div class="brand-sub">Student risk monitor</div></div></div>'
    )

    st.title("EduRisk Menu")

    selected_page = st.radio(
        "Select Page",
        [
            "Home",
            "Dashboard",
            "Student Data",
            "Risk Checker",
            "About"
        ],
        label_visibility="collapsed"
    )

    render(
        '<div class="side-note">Risk prediction should support '
        'students, not punish them.</div>'
    )


# ------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------
if selected_page == "Home":

    render(
        """
        <div class="welcome">
        <p class="w-title">🎓 EduRisk Analytics</p>
        <p class="w-sub">Interactive Student Risk Monitoring Dashboard</p>
        <p class="w-text">Welcome to Lab 02.</p>
        <p class="w-text">In this lab, you will use Streamlit widgets to explore student performance data.</p>
        <br>
        <span class="chip"><i></i>Lab 02 app is running successfully!</span>
        </div>
        """
    )

    h1, h2, h3 = st.columns(3)

    with h1:
        render(metric_card(
            "Students", len(student_df), "in the dataset", ACCENT
        ))

    with h2:
        render(metric_card(
            "Courses", student_df["Course"].nunique(), "being tracked", ACCENT
        ))

    with h3:
        render(metric_card(
            "High Risk",
            student_df[student_df["Risk Level"] == "High Risk"].shape[0],
            "students need support",
            RISK_COLORS["High Risk"]
        ))

    section_title("What you can do")

    render(
        """
        <div class="nav-card"><b>Dashboard</b> <span>– filter students and see charts</span></div>
        <div class="nav-card"><b>Student Data</b> <span>– see the full list of students</span></div>
        <div class="nav-card"><b>Risk Checker</b> <span>– check the risk of one student</span></div>
        """
    )


# ------------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------------
elif selected_page == "Dashboard":

    page_header(
        "Interactive Dashboard",
        "Use the filters below to explore student performance.",
        chip="Live dataset"
    )

    filter_box = st.container(border=True)

    with filter_box:

        card_title("Filters", "Narrow down the students you want to see.")

        f1, f2, f3, f4 = st.columns(4)

        with f1:
            selected_course = st.selectbox(
                "Select Course",
                ["All"] + list(student_df["Course"].unique())
            )

        with f2:
            selected_risk = st.selectbox(
                "Select Risk Level",
                [
                    "All",
                    "Low Risk",
                    "Medium Risk",
                    "High Risk"
                ]
            )

        with f3:
            min_attendance = st.slider(
                "Minimum Attendance",
                0,
                100,
                0
            )

        with f4:
            min_score = st.slider(
                "Minimum Score",
                0,
                100,
                0
            )

    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    with filter_box:
        st.caption(
            f"Showing {total_students} of {len(student_df)} students"
        )

    section_title("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    share_students = (
        total_students / len(student_df) * 100 if len(student_df) else 0
    )
    share_high = (
        high_risk_students / total_students * 100 if total_students else 0
    )

    with col1:
        render(metric_card(
            "Students",
            total_students,
            f"of {len(student_df)} in total",
            ACCENT,
            share_students
        ))

    with col2:
        render(metric_card(
            "Average Score",
            round(average_score, 2),
            "out of 100",
            value_color(average_score),
            average_score
        ))

    with col3:
        render(metric_card(
            "Average Attendance",
            f"{round(average_attendance, 2)}%",
            "average attendance rate",
            value_color(average_attendance),
            average_attendance
        ))

    with col4:
        render(metric_card(
            "High Risk",
            high_risk_students,
            f"{round(share_high)}% of filtered students",
            RISK_COLORS["High Risk"],
            share_high
        ))

    section_title("Charts")

    chart_col1, chart_col2 = st.columns([3, 2])

    with chart_col1:

        with st.container(border=True):

            card_title(
                "Student Scores",
                "Dashed lines mark the 60 and 75 cut-offs."
            )

            if len(filtered_df) > 0:

                bars = (
                    alt.Chart(filtered_df)
                    .mark_bar(
                        cornerRadiusTopLeft=4,
                        cornerRadiusTopRight=4
                    )
                    .encode(
                        x=alt.X(
                            "Student Name:N",
                            sort="-y",
                            title=None,
                            axis=alt.Axis(labelAngle=0)
                        ),
                        y=alt.Y(
                            "Score:Q",
                            scale=alt.Scale(domain=[0, 100]),
                            title=None
                        ),
                        color=alt.Color(
                            "Risk Level:N",
                            scale=risk_scale(),
                            legend=None
                        ),
                        tooltip=[
                            "Student Name",
                            "Course",
                            "Score",
                            "Attendance",
                            "Risk Level"
                        ]
                    )
                )

                lines = (
                    alt.Chart(pd.DataFrame({"cutoff": [60, 75]}))
                    .mark_rule(strokeDash=[4, 4], color=MUTED)
                    .encode(
                        y=alt.Y(
                            "cutoff:Q",
                            scale=alt.Scale(domain=[0, 100])
                        )
                    )
                )

                st.altair_chart(
                    style_chart((bars + lines).properties(height=290)),
                    use_container_width=True
                )

            else:

                render(
                    '<div class="empty">No data available for score chart.</div>'
                )

    with chart_col2:

        with st.container(border=True):

            card_title(
                "Risk Level Count",
                "Number of students in each risk level."
            )

            if len(filtered_df) > 0:

                risk_count = (
                    filtered_df["Risk Level"]
                    .value_counts()
                    .rename_axis("Risk Level")
                    .reset_index(name="Students")
                )

                order = ["High Risk", "Medium Risk", "Low Risk"]

                risk_bars = (
                    alt.Chart(risk_count)
                    .mark_bar(cornerRadiusEnd=4, size=28)
                    .encode(
                        y=alt.Y(
                            "Risk Level:N",
                            sort=order,
                            title=None
                        ),
                        x=alt.X(
                            "Students:Q",
                            title=None,
                            axis=alt.Axis(tickMinStep=1)
                        ),
                        color=alt.Color(
                            "Risk Level:N",
                            scale=risk_scale(),
                            legend=None
                        ),
                        tooltip=["Risk Level", "Students"]
                    )
                )

                risk_text = (
                    alt.Chart(risk_count)
                    .mark_text(
                        align="left",
                        dx=6,
                        color=TEXT,
                        fontSize=14,
                        fontWeight="bold"
                    )
                    .encode(
                        y=alt.Y("Risk Level:N", sort=order),
                        x=alt.X("Students:Q"),
                        text="Students:Q"
                    )
                )

                st.altair_chart(
                    style_chart((risk_bars + risk_text).properties(height=290)),
                    use_container_width=True
                )

            else:

                render(
                    '<div class="empty">No data available for risk chart.</div>'
                )

    section_title("Filtered Student Dataset")

    risk_guide()

    st.write("")

    show_data = st.checkbox(
        "Show Filtered Dataset",
        True
    )

    if show_data:

        render(html_table(filtered_df))

        csv = filtered_df.to_csv(
            index=False
        )

        st.write("")

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "Filtered dataset is hidden."
        )


# ------------------------------------------------------------------
# STUDENT DATA
# ------------------------------------------------------------------
elif selected_page == "Student Data":

    page_header(
        "Student Data",
        "All students in one place.",
        chip=f"{len(student_df)} student records"
    )

    total_students = len(student_df)

    average_score = student_df[
        "Score"
    ].mean()

    average_attendance = student_df[
        "Attendance"
    ].mean()

    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render(metric_card(
            "Total Students",
            total_students,
            "enrolled in total",
            ACCENT
        ))

    with col2:
        render(metric_card(
            "Average Score",
            round(average_score, 2),
            "out of 100",
            value_color(average_score),
            average_score
        ))

    with col3:
        render(metric_card(
            "Average Attendance",
            f"{round(average_attendance, 2)}%",
            "average attendance rate",
            value_color(average_attendance),
            average_attendance
        ))

    with col4:
        render(metric_card(
            "High Risk Students",
            high_risk_students,
            f"{round(high_risk_students / total_students * 100)}% of all students",
            RISK_COLORS["High Risk"],
            high_risk_students / total_students * 100
        ))

    section_title("Full Student Dataset")

    risk_guide()

    st.write("")

    render(html_table(student_df))


# ------------------------------------------------------------------
# RISK CHECKER
# ------------------------------------------------------------------
elif selected_page == "Risk Checker":

    page_header(
        "Single Student Risk Checker",
        "Type a name, score and attendance, then press Check Risk."
    )

    left, right = st.columns([3, 2])

    with left:

        with st.form("risk_checker_form"):

            input_name = st.text_input(
                "Student Name"
            )

            n1, n2 = st.columns(2)

            with n1:
                input_score = st.number_input(
                    "Score",
                    0,
                    100,
                    50
                )

            with n2:
                input_attendance = st.number_input(
                    "Attendance",
                    0,
                    100,
                    50
                )

            submitted = st.form_submit_button(
                "Check Risk"
            )

        if submitted:

            risk_result = get_risk_level(
                input_score,
                input_attendance
            )

            color = RISK_COLORS[risk_result]

            render(
                f"""
                <div class="result" style="background:{RISK_BG[risk_result]}; border-color:{color};">
                <p class="r-level" style="color:{color};">Risk Level: {risk_result}</p>
                <div class="r-row"><span>Student Name</span><b>{html_lib.escape(input_name)}</b></div>
                <div class="r-row"><span>Score</span><b>{input_score}</b></div>
                <div class="r-row"><span>Attendance</span><b>{input_attendance}</b></div>
                </div>
                """
            )

    with right:

        card_title("How risk is decided")

        risk_guide(vertical=True)


# ------------------------------------------------------------------
# ABOUT
# ------------------------------------------------------------------
else:

    page_header(
        "About",
        "This app is part of Lab 02."
    )

    render(
        """
        <div class="nav-card"><span>Course</span><br><b>Web App Development for Data Science</b></div>
        <div class="nav-card"><span>Project Theme</span><br><b>EduRisk Analytics</b></div>
        <div class="nav-card"><span>Topic</span><br><b>Streamlit Interactive Dashboard</b></div>
        """
    )

    st.info(
        "Ethics Reminder: Risk prediction should support "
        "students, not punish them."
    )