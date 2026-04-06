from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import base64
import os
import json
import xml.etree.ElementTree as ET
import requests
import boto3
import glob

class TestReportGenerator:
    def __init__(self, trigger_id, agent_id, report_title="Test Report"):
        self.xml_file = r"/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI/Report"
        self.VisuleReportpath = r"/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Visual_Reports"
        self.company_logo = r"/home/ltts/Documents/EvQUAL_Logo.png"
        self.trigger_id = trigger_id
        self.agent_id = agent_id
        self.report_title = report_title
        self.df = pd.DataFrame()
        self.total_tests = 0
        self.pass_count = 0
        self.fail_count = 0
        self.pass_rate = 0.0
        self.status_counts = {}
        self.chart_config = {
            'margin': dict(l=40, r=40, t=50, b=40),
            'height': 280,
            'font': dict(size=11, color='#2c3e50'),
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'hovermode': 'closest'
        }
        self.chart_config_no_click = {}  # Configuration for Plotly charts (no click for export)
        self.api_url = "http://192.168.1.58:5000/update_data_dashboard?key="
        self.link = None

        os.makedirs(self.VisuleReportpath, exist_ok=True)
        self.device_name = "Unknown Device"
        self.test_cases = []
        self.execution_start_time = None

    def get_latest_Report(self):
        list_of_Reprts_files = glob.glob(os.path.join(self.VisuleReportpath, "*.html"))
        if not list_of_Reprts_files:
            print("❌ No Visule report files found.")
            return None
        return max(list_of_Reprts_files, key=os.path.getctime)

    def get_latest_xml(self):
        print("Directory to search:", self.xml_file)
        # Do not add *.xml in self.xml_file. Add it here in glob.
        search_path = os.path.join(self.xml_file, "*.xml")
        print("Search path:", search_path)

        list_of_files = glob.glob(search_path)
        if not list_of_files:
            print("❌ No xml report files found.")
            return None
        latest_file = max(list_of_files, key=os.path.getctime)
        print("✅ Latest XML file:", latest_file)
        return latest_file

    def encode_image_to_base64(self, image_path):
        """Convert image to base64 string for embedding in HTML"""
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                _, ext = os.path.splitext(image_path)
                ext = ext.lower()
                if ext in ['.jpg', '.jpeg']:
                    mime_type = 'image/jpeg'
                elif ext == '.png':
                    mime_type = 'image/png'
                elif ext == '.gif':
                    mime_type = 'image/gif'
                elif ext == '.svg':
                    mime_type = 'image/svg+xml'
                else:
                    mime_type = 'image/png'  # default
                return f"data:{mime_type};base64,{encoded_string}"
            return None
        except Exception as e:
            print(f"Warning: Could not encode image {image_path}: {e}")
            return None

    def parse_robot_framework_xml(self,xml_file):
        """
        Parses a Robot Framework output.xml file to extract test case data.
        Extracts test name, status, elapsed time, and parent suite name (as Module).
        """
        print(f"Parsing XML file: {xml_file}")

        # self.xml_file = self.get_latest_xml()
        # if not self.xml_file:
        #     print("❌ No XML file found to parse.")
        #     return
        tree = ET.parse(xml_file)
        root = tree.getroot()

        data = []
        # Finding all <suite> elements (top-level and nested)
        for suite in root.iter('suite'):  # Use iter to find all nested suites
            # Getting suite name, which will serve as the module
            module_name = suite.get('name', 'None')  # Default to 'None' if suite name is missing

            # Finding all <test> elements within this suite
            for test in suite.findall('test'):
                test_name = test.get('name', 'Unnamed Test')  # Default to 'Unnamed Test' if name is missing

                # Finding the final <status> tag within the test (usually the last one is the test's overall status)
                status_element = test.find('status')  # This gets the direct child status, for overall test status

                status = "UNKNOWN"
                elapsed_time_seconds = 0.0

                if status_element is not None:
                    raw_status = status_element.get('status')
                    # Map Robot Framework statuses to "PASS" or "FAIL"
                    if raw_status == "PASS":
                        status = "PASS"
                    else:  # Any other status like FAIL, SKIP, NOT RUN will be treated as FAIL for simplicity
                        status = "FAIL"

                    # Elapsed time is directly in seconds (float)
                    try:
                        elapsed_time_seconds = float(status_element.get('elapsed', 0.0))
                    except ValueError:
                        elapsed_time_seconds = 0.0  # Default to 0.0 if conversion fails

                # Format elapsed time to MM:SS string for display
                minutes = int(elapsed_time_seconds // 60)
                seconds = int(elapsed_time_seconds % 60)
                elapsed_time_formatted = f"{minutes:02d}:{seconds:02d}"

                data.append({
                    'Test Case': test_name,
                    'Status': status,
                    'Elapsed Time': elapsed_time_formatted,  # Formatted for display (MM:SS)
                    'Duration (s)': elapsed_time_seconds,  # Numeric seconds for calculations
                    'Module': module_name
                })
        self.df = pd.DataFrame(data)
        self.df = self.df.dropna()  # Remove any rows with NaN values if parsing resulted in incomplete data

        # Add unique IDs for each test case
        self.df['ID'] = self.df.index
        self.df['Test_Short'] = self.df['Test Case'].apply(lambda x: x[:12] + "..." if len(x) > 12 else x)

    def calculate_kpis(self):
        self.total_tests = len(self.df)
        self.pass_count = (self.df["Status"] == "PASS").sum()
        self.fail_count = (self.df["Status"] == "FAIL").sum()
        self.pass_rate = (self.pass_count / self.total_tests) * 100 if self.total_tests > 0 else 0
        self.status_counts = self.df["Status"].value_counts().to_dict()
        self.status_counts.setdefault("PASS", 0)
        self.status_counts.setdefault("FAIL", 0)

    def generate_pie_chart(self):
        fig_pie = px.pie(
            names=["PASS", "FAIL"],
            values=[self.status_counts["PASS"], self.status_counts["FAIL"]],
            title="Pass vs Fail Distribution",
            hole=0,
            color_discrete_map={"PASS": "#28a745", "FAIL": "#dc3545"}
        )
        fig_pie.update_layout(**self.chart_config)
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=10,
            customdata=["PASS", "FAIL"],
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )
        fig_pie.update_layout(legend=dict(itemclick=False, itemdoubleclick=False))
        return fig_pie

    def generate_donut_chart(self):
        fig_donut = px.pie(
            names=["PASS", "FAIL"],
            values=[self.status_counts["PASS"], self.status_counts["FAIL"]],
            title="Test Results Overview",
            hole=0.5,
            color_discrete_map={"PASS": "#28a745", "FAIL": "#dc3545"}
        )
        fig_donut.update_layout(**self.chart_config)
        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=10,
            customdata=["PASS", "FAIL"],
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            marker=dict(line=dict(color='#FFFFFF', width=1))
        )
        fig_donut.update_layout(legend=dict(itemclick=False, itemdoubleclick=False))
        return fig_donut

    def generate_stacked_bar_chart(self):
        stacked = self.df.groupby(['Test Case', 'Status']).size().unstack(fill_value=0)
        fig_stack = go.Figure()

        for status in ['PASS', 'FAIL']:
            if status in stacked.columns:
                fig_stack.add_trace(go.Bar(
                    name=status,
                    x=stacked.index,
                    y=stacked[status],
                    marker_color='#28a745' if status == 'PASS' else '#dc3545',
                    width=0.6,
                    customdata=[{'status': status, 'test_case': tc} for tc in stacked.index],
                    hovertemplate="<b>%{customdata.test_case}</b><br>Status: %{customdata.status}<br>Count: %{y}<extra></extra>"
                ))

        fig_stack.update_layout(
            **self.chart_config,
            title="Test Case Status Distribution",
            barmode='stack',
            xaxis_title="Test Case",
            yaxis_title="Count",
            xaxis={'tickangle': 45, 'tickfont': dict(size=9)},
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, itemclick=False,
                        itemdoubleclick=False)
        )
        return fig_stack

    def generate_module_results_chart(self):
        module_grouped = self.df.groupby(['Module', 'Status']).size().unstack(fill_value=0)
        fig_module = go.Figure()

        for status in ['PASS', 'FAIL']:
            if status in module_grouped.columns:
                fig_module.add_trace(go.Bar(
                    name=status,
                    x=module_grouped.index,
                    y=module_grouped[status],
                    marker_color='#28a745' if status == 'PASS' else '#dc3545',
                    width=0.5,
                    customdata=[{'status': status, 'module': mod} for mod in module_grouped.index],
                    hovertemplate="<b>%{customdata.module}</b><br>Status: %{customdata.status}<br>Count: %{y}<extra></extra>"
                ))

        fig_module.update_layout(
            **self.chart_config,
            title="Results by Module",
            barmode='group',
            xaxis_title="Module",
            yaxis_title="Count",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, itemclick=False,
                        itemdoubleclick=False)
        )
        return fig_module

    def generate_html_report(self):
        xml_file = self.get_latest_xml()
        if not xml_file:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.VisuleReportpath, f"visualreport_{timestamp}.html")
        print(f"Generating report based on: {xml_file}")
        self.parse_robot_framework_xml(xml_file)  # Assuming this takes xml_file as argument
        print("line 253")
        self.calculate_kpis()
        print("line 255")

        df_json = self.df.to_json(orient='records')
        status_counts_json = json.dumps(self.status_counts)
        pass_rate_json = json.dumps(self.pass_rate)

        logo_base64 = self.encode_image_to_base64(self.company_logo)

        fig_pie = self.generate_pie_chart()
        fig_donut = self.generate_donut_chart()
        fig_stack = self.generate_stacked_bar_chart()
        fig_module = self.generate_module_results_chart()

        # timestamp = time.strftime("%Y%m%d_%H%M%S")
        # output_file = f"{self.VisuleReportpath}/visualreport_{timestamp}.html"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"""
            <html>
            <head>
                <title>{self.report_title}</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap' rel='stylesheet'>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <style>
                    /* General Body and Container Styles */
                    body {{
                        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: #2c3e50;
                        padding: 20px;
                        margin: 0;
                        min-height: 100vh;
                        line-height: 1.5;
                        overflow-x: hidden;
                    }}
                    .container {{
                        background: white;
                        border-radius: 20px;
                        padding: 30px;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                        max-width: 1400px;
                        margin: 0 auto;
                        opacity: 0;
                        transform: translateY(20px);
                        animation: fadeInSlideUp 0.8s ease-out forwards;
                        animation-delay: 0.2s;
                    }}

                    /* Header and Logo */
                    .header {{
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin-bottom: 30px;
                        gap: 15px;
                    }}
                    .logo {{
                        height: 50px;
                        width: auto;
                        max-width: 150px;
                        object-fit: contain;
                        border-radius: 10px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }}
                    .logo:hover {{
                        transform: scale(1.05);
                        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
                    }}
                    .logo-fallback {{
                        height: 50px;
                        width: 50px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 18px;
                        font-weight: 600;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    }}
                    h1 {{
                        color: #2c3e50;
                        font-weight: 600;
                        font-size: 2.2em;
                        margin: 0;
                        opacity: 0;
                        transform: translateY(-10px);
                        animation: fadeInDown 0.6s ease-out forwards;
                        animation-delay: 0.4s;
                    }}

                    /* KPIs */
                    .kpis {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 15px;
                        margin-bottom: 30px;
                    }}
                    .kpi {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px;
                        border-radius: 15px;
                        text-align: center;
                        color: white;
                        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
                        transition: all 0.3s ease;
                        opacity: 0;
                        transform: scale(0.9);
                        animation: popIn 0.5s ease-out forwards;
                    }}
                    .kpi:nth-child(1) {{ animation-delay: 0.6s; }}
                    .kpi:nth-child(2) {{ animation-delay: 0.7s; }}
                    .kpi:nth-child(3) {{ animation-delay: 0.8s; }}

                    /* KPI Hover Effect */
                    .kpi:hover {{
                        transform: translateY(-8px) scale(1.03); /* Moves upwards (-Y) and scales slightly */
                        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.5); /* Stronger shadow */
                    }}
                    .kpi h2 {{
                        margin: 5px 0;
                        font-size: 2.2em;
                        font-weight: 600;
                        transition: transform 0.2s ease-out;
                    }}
                    .kpi p {{
                        margin: 0;
                        font-weight: 400;
                        font-size: 0.95em;
                        opacity: 0.9;
                    }}

                    /* Charts */
                    .charts-container {{
                        margin-bottom: 30px;
                    }}
                    .chart-row {{
                        display: grid;
                        grid-template-columns: repeat(3, 1fr);
                        gap: 20px;
                        margin-bottom: 20px;
                    }}
                    .chart-row.two-charts {{
                        grid-template-columns: repeat(2, 1fr);
                    }}
                    .chart {{
                        background: white;
                        border-radius: 18px;
                        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
                        border: 1px solid rgba(0,0,0,0.05);
                        transition: all 0.3s ease;
                        overflow: hidden;
                        position: relative;
                        opacity: 0;
                        transform: translateY(20px);
                        animation: fadeInSlideUp 0.7s ease-out forwards;
                    }}
                    .chart:nth-child(1) {{ animation-delay: 1.0s; }}
                    .chart:nth-child(2) {{ animation-delay: 1.2s; }}
                    .chart:nth-child(3) {{ animation-delay: 1.4s; }}
                    .chart:nth-child(4) {{ animation-delay: 1.6s; }}
                    .chart:nth-child(5) {{ animation-delay: 1.8s; }}

                    /* Chart Hover Effect */
                    .chart:hover {{
                        transform: translateY(-5px);
                        box-shadow: 0 12px 25px rgba(0,0,0,0.1);
                        border: 2px solid #a0b6f1;
                    }}
                    .chart.filtered {{
                        border: 3px solid #667eea;
                        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
                    }}
                    .chart > div {{
                        border-radius: 18px;
                    }}

                    /* Controls */
                    .controls {{
                        background: #f8f9fa;
                        border-radius: 15px;
                        padding: 20px;
                        margin-bottom: 20px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                        opacity: 0;
                        transform: translateY(10px);
                        animation: fadeInSlideUp 0.6s ease-out forwards;
                        animation-delay: 2.0s;
                    }}
                    .filter-controls {{
                        display: flex;
                        gap: 15px;
                        align-items: center;
                        flex-wrap: wrap;
                    }}
                    .filter-btn {{
                        padding: 8px 16px;
                        border: 2px solid #667eea;
                        background: white;
                        color: #667eea;
                        border-radius: 20px;
                        cursor: pointer;
                        transition: all 0.3s ease, transform 0.2s;
                        font-weight: 500;
                        font-size: 0.9em;
                    }}
                    .filter-btn:hover {{
                        background: #667eea;
                        color: white;
                        transform: translateY(-2px);
                    }}
                    .filter-btn.active {{
                        background: #667eea;
                        color: white;
                        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                        transform: scale(1.05);
                    }}
                    .clear-btn {{
                        background: #dc3545;
                        color: white;
                        border: 2px solid #dc3545;
                    }}
                    .clear-btn:hover {{
                        background: #c82333;
                        border-color: #c82333;
                        transform: rotate(5deg) scale(1.05);
                    }}
                    .clear-btn.clicked {{
                        animation: shake 0.3s ease-in-out;
                    }}

                    /* Table Styles */
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        background: white;
                        border-radius: 15px;
                        overflow: hidden;
                        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
                        margin-top: 20px;
                        opacity: 0;
                        transform: translateY(20px);
                        animation: fadeInSlideUp 0.7s ease-out forwards;
                        animation-delay: 2.2s;
                    }}
                    th, td {{
                        padding: 12px 15px;
                        text-align: center;
                        border-bottom: 1px solid #f0f0f0;
                        font-size: 0.9em;
                        transition: background-color 0.3s ease, transform 0.2s;
                    }}
                    th {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        font-weight: 500;
                        font-size: 0.85em;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f8f9fb;
                    }}
                    tr:hover {{
                        background-color: #e8f4fd;
                        transform: scale(1.01);
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    }}
                    tr.filtered {{
                        background-color: #fff3cd !important;
                        border-left: 4px solid #667eea;
                        animation: pulseHighlight 0.5s ease-out;
                    }}
                    tr.hidden {{
                        display: none;
                    }}
                    h2 {{
                        color: #2c3e50;
                        margin: 20px 0 15px 0;
                        font-weight: 500;
                        font-size: 1.4em;
                        opacity: 0;
                        transform: translateX(-10px);
                        animation: fadeInSlideRight 0.6s ease-out forwards;
                        animation-delay: 2.1s;
                    }}
                    .status-indicator {{
                        display: inline-block;
                        width: 10px;
                        height: 10px;
                        border-radius: 50%;
                        margin-right: 8px;
                    }}
                    .status-pass {{
                        background-color: #28a745;
                    }}
                    .status-fail {{
                        background-color: #dc3545;
                    }}

                    /* Keyframe Animations */
                    @keyframes fadeInSlideUp {{
                        from {{ opacity: 0; transform: translateY(20px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                    @keyframes fadeInDown {{
                        from {{ opacity: 0; transform: translateY(-20px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                    @keyframes popIn {{
                        from {{ opacity: 0; transform: scale(0.8); }}
                        to {{ opacity: 1; transform: scale(1); }}
                    }}
                    @keyframes pulseHighlight {{
                        0% {{ box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }}
                        70% {{ box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }}
                        100% {{ box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }}
                    }}
                    @keyframes shake {{
                        0%, 100% {{ transform: translateX(0); }}
                        20%, 60% {{ transform: translateX(-5px); }}
                        40%, 80% {{ transform: translateX(5px); }}
                    }}
                    @keyframes fadeInSlideRight {{
                        from {{ opacity: 0; transform: translateX(-20px); }}
                        to {{ opacity: 1; transform: translateX(0); }}
                    }}

                    /* Responsive Design */
                    @media (max-width: 1200px) {{
                        .chart-row {{
                            grid-template-columns: repeat(2, 1fr);
                        }}
                    }}
                    @media (max-width: 768px) {{
                        .chart-row {{
                            grid-template-columns: 1fr;
                        }}
                        .kpis {{
                            grid-template-columns: repeat(2, 1fr);
                        }}
                        .container {{
                            padding: 20px;
                        }}
                        .header {{
                            flex-direction: column;
                            gap: 10px;
                        }}
                        h1 {{
                            font-size: 1.8em;
                            text-align: center;
                        }}
                        .filter-controls {{
                            justify-content: center;
                        }}
                    }}
                    @media (max-width: 480px) {{
                        .kpis {{
                            grid-template-columns: 1fr;
                        }}
                        .chart-row {{
                            gap: 15px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class='container'>
                    <div class='header'>
                        <div id='logo-container'>
                            {"<img src='" + logo_base64 + "' alt='Company Logo' class='logo'>" if logo_base64 else "<div class='logo-fallback'>QA</div>"}
                        </div>
                        <h1>{self.report_title}</h1>
                    </div>

                    <div class='kpis'>
                        <div class='kpi' id='kpi-total'><h2>{self.total_tests}</h2><p>Total Tests</p></div>
                        <div class='kpi' id='kpi-pass'><h2>{self.pass_count}</h2><p>Passed</p></div>
                        <div class='kpi' id='kpi-fail'><h2>{self.fail_count}</h2><p>Failed</p></div>
                    </div>

                    <div class='charts-container'>
                        <div class='chart-row'>
                            <div class='chart' id='chart-pie'>{fig_pie.to_html(full_html=False, include_plotlyjs='cdn', div_id='pie-chart', config=self.chart_config_no_click)}</div>
                            <div class='chart' id='chart-donut'>{fig_donut.to_html(full_html=False, include_plotlyjs='cdn', div_id='donut-chart', config=self.chart_config_no_click)}</div>
                            <div class='chart' id='chart-stack'>{fig_stack.to_html(full_html=False, include_plotlyjs='cdn', div_id='stack-chart', config=self.chart_config_no_click)}</div>
                        </div>

                        <div class='chart-row two-charts'>
                            <div class='chart' id='chart-gauge'>
                                <div id='gauge-chart'></div>
                            </div>
                            <div class='chart' id='chart-module'>{fig_module.to_html(full_html=False, include_plotlyjs=False, div_id='module-chart', config=self.chart_config_no_click)}</div>
                        </div>
                    </div>

                    <div class='controls'>
                        <div class='filter-controls'>
                            <strong>Interactive Filters:</strong>
                            <button class='filter-btn' onclick='filterByStatus("PASS")'>
                                <span class='status-indicator status-pass'></span>Show PASS Only
                            </button>
                            <button class='filter-btn' onclick='filterByStatus("FAIL")'>
                                <span class='status-indicator status-fail'></span>Show FAIL Only
                            </button>
                            <button class='filter-btn clear-btn' onclick='clearFilters()'>
                                🔄 Clear Filters
                            </button>
                        </div>
                    </div>

                    <h2>📋 Detailed Test Results</h2>
                    <div id='table-container'>
                        <table id='results-table'>
                            <thead>
                                <tr>
                                    <th>S.No</th>
                                    <th>Test Case</th>
                                    <th>Status</th>
                                    <th>Elapsed Time</th>
                                </tr>
                            </thead>
                            <tbody>
            """)

            # Create interactive table
            for i, row in enumerate(self.df.iterrows()):
                status_class = "status-pass" if row[1]['Status'] == 'PASS' else "status-fail"
                f.write(f"""
                                <tr data-status='{row[1]['Status']}' data-module='{row[1].get('Module', 'General')}' data-id='{row[1]['ID']}'>
                                    <td class="sno-column"></td>
                                    <td>{row[1]['Test Case']}</td>
                                    <td><span class='status-indicator {status_class}'></span>{row[1]['Status']}</td>
                                    <td>{row[1]['Elapsed Time']}</td>
                                </tr>
                """)
            f.write(f"""
                            </tbody>
                        </table>
                    </div>
                </div>

                <script>
                    // Global variables
                    let testData = {df_json};
                    let currentFilter = null;
                    let statusCounts = {json.dumps(self.status_counts)};
                    // Store original KPI values - these never change
                    const ORIGINAL_TOTAL = {self.total_tests};
                    const ORIGINAL_PASS = {self.pass_count};
                    const ORIGINAL_FAIL = {self.fail_count};
                    const ORIGINAL_PASS_RATE = {pass_rate_json};
                    // Function to animate a number
                    function animateNumber(elementId, start, end, duration) {{
                        const obj = document.getElementById(elementId);
                        let startTime = null;

                        function step(currentTime) {{
                            if (!startTime) startTime = currentTime;
                            const progress = Math.min((currentTime - startTime) / duration, 1);
                            const currentValue = Math.floor(progress * (end - start) + start);
                            obj.innerHTML = currentValue;
                            if (progress < 1) {{
                                requestAnimationFrame(step);
                            }} else {{
                                obj.innerHTML = end;
                            }}
                        }}
                        requestAnimationFrame(step);
                    }}

                    // KPI Count-up Animation Setup
                    function animateKPIs() {{
                        animateNumber('kpi-total H2', 0, ORIGINAL_TOTAL, 1500);
                        animateNumber('kpi-pass H2', 0, ORIGINAL_PASS, 1500);
                        animateNumber('kpi-fail H2', 0, ORIGINAL_FAIL, 1500);
                    }}

                    // Setup KPI hover effects
                    function setupKpiHoverEffects() {{
                        document.querySelectorAll('.kpi').forEach(kpiDiv => {{
                            kpiDiv.addEventListener('mouseenter', () => {{
                                const h2 = kpiDiv.querySelector('h2');
                                if (h2) {{
                                    h2.style.transform = 'scale(1.08)';
                                }}
                            }});

                            kpiDiv.addEventListener('mouseleave', () => {{
                                const h2 = kpiDiv.querySelector('h2');
                                if (h2) {{
                                    h2.style.transform = 'scale(1)';
                                }}
                            }});
                        }});
                    }}


                    // Gauge Chart Animation Setup
                    function createAnimatedGauge() {{
                        const passRate = ORIGINAL_PASS_RATE;
                        const initialGaugeData = [{{
                            type: "indicator",
                            mode: "gauge+number+delta",
                            value: 0,
                            domain: {{x: [0, 1], y: [0, 1]}},
                            title: {{
                                text: "Success Rate (%)",
                                font: {{size: 14, color: '#2c3e50'}}
                            }},
                            delta: {{
                                reference: 80,
                                increasing: {{color: "#28a745"}},
                                decreasing: {{color: "#dc3545"}},
                                font: {{size: 12}}
                            }},
                            number: {{
                                font: {{size: 28, color: '#2c3e50'}},
                                suffix: "%",
                                valueformat: ".1f"
                            }},
                            gauge: {{
                                axis: {{
                                    range: [null, 100],
                                    tickwidth: 1,
                                    tickcolor: "#2c3e50",
                                    tickfont: {{size: 10}}
                                }},
                                bar: {{
                                    color: passRate >= 80 ? "#28a745" : (passRate >= 60 ? "#ffc107" : "#dc3545"),
                                    thickness: 0.8
                                }},
                                bgcolor: "white",
                                borderwidth: 2,
                                bordercolor: "#e0e0e0",
                                steps: [
                                    {{range: [0, 60], color: "#ffebee"}},
                                    {{range: [60, 80], color: "#fff3e0"}},
                                    {{range: [80, 100], color: "#e8f5e8"}}
                                ],
                                threshold: {{
                                    line: {{color: "#dc3545", width: 4}},
                                    thickness: 0.8,
                                    value: 90
                                }}
                            }}
                        }}];
                        const layout = {{
                            margin: {{l: 20, r: 20, t: 50, b: 20}},
                            height: 280,
                            font: {{size: 11, color: '#2c3e50'}},
                            plot_bgcolor: 'rgba(0,0,0,0)',
                            paper_bgcolor: 'rgba(0,0,0,0)',
                            showlegend: false
                        }};
                        const config = {json.dumps(self.chart_config_no_click)};

                        Plotly.newPlot('gauge-chart', initialGaugeData, layout, config);
                        setTimeout(() => {{
                            Plotly.animate('gauge-chart', {{
                                data: [{{
                                    value: passRate,
                                    gauge: {{
                                        bar: {{
                                            color: passRate >= 80 ? "#28a745" : (passRate >= 60 ? "#ffc107" : "#dc3545")
                                        }}
                                    }}
                                }}],
                                traces: [0]
                            }}, {{
                                transition: {{
                                    duration: 2500,
                                    easing: 'elastic-out'
                                }},
                                frame: {{
                                    duration: 2500,
                                    redraw: true
                                }}
                            }});
                        }}, 800);
                        // Add hover effects for gauge bar thickness
                        const gaugeChartDiv = document.getElementById('gauge-chart');
                        gaugeChartDiv.addEventListener('mouseenter', () => {{
                            Plotly.animate('gauge-chart', {{
                                data: [{{ gauge: {{ bar: {{ thickness: 0.95 }} }} }}],
                                traces: [0]
                            }}, {{ transition: {{duration: 200}}, frame: {{duration: 200}} }});
                        }});
                        gaugeChartDiv.addEventListener('mouseleave', () => {{
                            Plotly.animate('gauge-chart', {{
                                data: [{{ gauge: {{ bar: {{ thickness: 0.8 }} }} }}],
                                traces: [0]
                            }}, {{ transition: {{duration: 200}}, frame: {{duration: 200}} }});
                        }});
                    }}

                    // Function to update chart highlights based on filter
                    function updateChartHighlights(filteredStatus = null) {{
                        // Update Pie and Donut charts
                        ['pie-chart', 'donut-chart'].forEach(chartDivId => {{
                            const chartDiv = document.getElementById(chartDivId);
                            if (!chartDiv || !chartDiv.data || !chartDiv.data[0]) return;

                            let data = JSON.parse(JSON.stringify(chartDiv.data));
                            let layout = JSON.parse(JSON.stringify(chartDiv.layout));

                            // Reset all slices to default appearance
                            data[0].marker.line.width = 1;
                            data[0].marker.line.color = '#FFFFFF';
                            data[0].opacity = 1.0;

                            if (filteredStatus) {{
                                const statusLabels = data[0].labels;
                                const passIndex = statusLabels.indexOf("PASS");
                                const failIndex = statusLabels.indexOf("FAIL");
                                if (filteredStatus === "PASS" && passIndex !== -1) {{
                                    data[0].marker.line.width[passIndex] = 3;
                                    data[0].marker.line.color[passIndex] = '#667eea';
                                    data[0].opacity[passIndex] = 1.0;
                                    data[0].opacity[failIndex] = 0.4;
                                }} else if (filteredStatus === "FAIL" && failIndex !== -1) {{
                                    data[0].marker.line.width[failIndex] = 3;
                                    data[0].marker.line.color[failIndex] = '#667eea';
                                    data[0].opacity[passIndex] = 0.4;
                                    data[0].opacity[failIndex] = 1.0;
                                }}
                            }}

                            Plotly.react(chartDivId, data, layout, {json.dumps(self.chart_config_no_click)});
                        }});

                        // Update Stacked Bar and Module Bar charts
                        ['stack-chart', 'module-chart'].forEach(chartDivId => {{
                            const chartDiv = document.getElementById(chartDivId);
                            if (!chartDiv || !chartDiv.data) return;

                            let data = JSON.parse(JSON.stringify(chartDiv.data));
                            let layout = JSON.parse(JSON.stringify(chartDiv.layout));

                            data.forEach(trace => {{
                                const originalColor = trace.name === 'PASS' ? '#28a745' : '#dc3545';
                                trace.marker.color = originalColor;
                                trace.opacity = 1.0;

                                if (filteredStatus && trace.name !== filteredStatus) {{
                                    trace.opacity = 0.4;
                                }}
                            }});

                            Plotly.react(chartDivId, data, layout, {json.dumps(self.chart_config_no_click)});
                        }});
                    }}

                    // Function to update serial numbers
                    function updateSerialNumbers() {{
                        const visibleRows = document.querySelectorAll('#results-table tbody tr:not(.hidden)');
                        visibleRows.forEach((row, index) => {{
                            const snoCell = row.querySelector('.sno-column');
                            if (snoCell) {{
                                snoCell.textContent = index + 1;
                            }}
                        }});
                    }}

                    // Filter logic
                    function filterByStatus(status) {{
                        currentFilter = status;
                        document.querySelectorAll('.filter-btn').forEach(btn => {{
                            btn.classList.remove('active');
                        }});
                        const activeBtn = document.querySelector(`button[onclick="filterByStatus('${{status}}')"]`);
                        if (activeBtn) {{
                            activeBtn.classList.add('active');
                        }}

                        const tableRows = document.querySelectorAll('#results-table tbody tr');
                        tableRows.forEach(row => {{
                            const rowStatus = row.getAttribute('data-status');
                            if (rowStatus === status) {{
                                row.classList.remove('hidden');
                                row.classList.add('filtered');
                            }}
                            else {{
                                row.classList.add('hidden');
                                row.classList.remove('filtered');
                            }}
                        }});
                        updateChartHighlights(status);
                        updateSerialNumbers(); // Update serial numbers after filtering
                    }}

                    function clearFilters() {{
                        currentFilter = null;
                        document.querySelectorAll('.filter-btn').forEach(btn => {{
                            btn.classList.remove('active');
                        }});
                        const clearBtn = document.querySelector('.clear-btn');
                        clearBtn.classList.add('clicked');
                        setTimeout(() => clearBtn.classList.remove('clicked'), 300);

                        const tableRows = document.querySelectorAll('#results-table tbody tr');
                        tableRows.forEach(row => {{
                            row.classList.remove('hidden', 'filtered');
                        }});
                        updateChartHighlights(null);
                        updateSerialNumbers(); // Update serial numbers after clearing filters
                    }}

                    // Event listeners for Plotly charts
                    function setupPlotlyEventListeners() {{
                        document.getElementById('pie-chart').on('plotly_click', function(data) {{
                            if (data.points.length > 0) {{
                                const status = data.points[0].label;
                                filterByStatus(status);
                            }}
                        }});
                        document.getElementById('donut-chart').on('plotly_click', function(data) {{
                            if (data.points.length > 0) {{
                                const status = data.points[0].label;
                                filterByStatus(status);
                            }}
                        }});
                        document.getElementById('stack-chart').on('plotly_click', function(data) {{
                            if (data.points.length > 0) {{
                                const status = data.points[0].data.name;
                                filterByStatus(status);
                            }}
                        }});
                        document.getElementById('module-chart').on('plotly_click', function(data) {{
                            if (data.points.length > 0) {{
                                const status = data.points[0].data.name;
                                filterByStatus(status);
                            }}
                        }});
                    }}

                    // Resize Observer for responsive charts
                    function setupResizeObserver() {{
                        const charts = document.querySelectorAll('.chart > div[id]');
                        const observer = new ResizeObserver(entries => {{
                            for (let entry of entries) {{
                                const newWidth = entry.contentRect.width;
                                const newHeight = entry.contentRect.height;
                                if (entry.target.layout && (entry.target.layout.width !== newWidth || entry.target.layout.height !== newHeight)) {{
                                    Plotly.relayout(entry.target.id, {{width: newWidth, height: newHeight}});
                                }}
                            }}
                        }});
                        charts.forEach(chartDiv => {{
                            observer.observe(chartDiv);
                        }});
                    }}


                    // Initialize on DOMContentLoaded
                    document.addEventListener('DOMContentLoaded', function() {{
                        setTimeout(animateKPIs, 500);
                        setTimeout(createAnimatedGauge, 1000);
                        setTimeout(setupPlotlyEventListeners, 1200);
                        setTimeout(updateChartHighlights, 1500);
                        setTimeout(setupResizeObserver, 2000);
                        setTimeout(setupKpiHoverEffects, 500);
                        updateSerialNumbers(); // Initial call to set serial numbers
                    }});
                </script>
            </body>
            </html>
            """)

        print(f" Enhanced {self.report_title} generated: {output_file}")
        if logo_base64:
            print("Logo successfully embedded as base64.")
        else:
            print(
                "Logo not found or path is None - using fallback design. You can update 'COMPANY_LOGO' variable in the script if you have a logo file.")
        print(f" - Report is generated, with data read from '{self.xml_file}'!")
        print(f"✅ Enhanced Test Report generated: {output_file}")
        return output_file

    def access_report_file(self, output_file):
        PORT = 8086  # Change port number if needed
        # Handler = http.server.SimpleHTTPRequestHandler
        # Function to access a specific HTML file
        # Change directory to where the HTML file is located
        os.chdir(os.path.dirname(os.path.abspath(output_file)))

        # Extract the file name from the path
        file_report_name = os.path.basename(output_file)
#/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Visual_Reports
        # Print the HTTP link to access the HTML file
        http_report_link = f"http://192.168.1.101:{PORT}/{file_report_name}"
        print(f"Access your HTML file at: {http_report_link}")
        return http_report_link

    # def post_Report(self, output_file):
    #     """Send the generated report file path to the API."""
    #     print(f" Sending report file path to API: {output_file}")
    #     http_report_link = self.access_report_file(output_file)
    #     url = "http://192.168.1.58:5000/update_data_dashboard?key="
    #     data1 = json.dumps({"trigger_id": self.trigger_id, "agent_id": self.agent_id})
    #     data2 = json.dumps({"excel_report": http_report_link})

    #     response = requests.post(url + data1 + "&attribute=" + data2)
    #     print("🔹 API Response:", response.text)
    #     return response


    def post_Report(self, output_file):
        """Send the generated report (HTML + PDF) to the API"""

        import os
        import json
        import requests

        print(f"📤 Sending report file path to API: {output_file}")

        # ✅ HTML link (already working)
        http_report_link = self.access_report_file(output_file)

        # ✅ PDF link (same folder, same server)
        pdf_name = os.path.basename(output_file).replace(".html", ".pdf")
        pdf_link = f"http://192.168.1.101:8086/{pdf_name}"

        print("✅ HTML Link:", http_report_link)
        print("✅ PDF Link :", pdf_link)

        # ✅ API URL
        url = "http://192.168.1.58:5000/update_data_dashboard?key="

        # ✅ Payloads
        data1 = json.dumps({
            "trigger_id": self.trigger_id,
            "agent_id": self.agent_id
        })

        data2 = json.dumps({
            "excel_report": http_report_link,
            "visualreport_pdf": pdf_link
        })

        # ✅ Send request
        response = requests.post(url + data1 + "&attribute=" + data2)

        print("🔹 API Response:", response.text)

        return response



    def convert_visual_pdf(self, html_file_path):
        import asyncio
        import os
        from pyppeteer import launch

        pdf_file = html_file_path.replace(".html", ".pdf")

        async def _convert():
            browser = await launch(headless=True, args=['--no-sandbox'])
            page = await browser.newPage()

            file_name = os.path.basename(html_file_path)
            url = f"http://192.168.1.101:8086/{file_name}"

            print("Opening URL:", url)

            await page.goto(url, {'waitUntil': 'networkidle2'})

            # ✅ WAIT for charts
            await asyncio.sleep(6)

            # 🔥 CONVERT ALL PLOTLY CHARTS TO IMAGES (KEY FIX)
            await page.evaluate("""
                async () => {
                    const charts = document.querySelectorAll('.plotly-graph-div');

                    for (let chart of charts) {
                        try {
                            const imgData = await Plotly.toImage(chart, {format: 'png', width: 800, height: 500});
                            const img = document.createElement('img');
                            img.src = imgData;
                            img.style.width = '100%';

                            chart.parentNode.replaceChild(img, chart);
                        } catch(e) {
                            console.log("Chart conversion failed", e);
                        }
                    }
                }
            """)

            # ✅ wait after conversion
            await asyncio.sleep(3)

            # ✅ generate PDF
            await page.pdf({
                "path": pdf_file,
                "format": "A4",
                "printBackground": True
            })

            await browser.close()

        asyncio.get_event_loop().run_until_complete(_convert())

        if not os.path.exists(pdf_file):
            print("❌ PDF NOT CREATED")
            return None

        print("✅ PDF generated:", pdf_file)
        return pdf_file
    
    # def run(self):
    #     self.generate_html_report()
    #     output_file = self.generate_html_report()
    #     # if output_file:
    #     self.post_Report(output_file)
    #     # else:
    #     #     print("Report generation skipped due to missing XML.")


    def run(self):
        output_file = self.generate_html_report()

        if not output_file:
            print("❌ Report generation failed")
            return

        # ✅ Convert HTML → PDF
        pdf_file = self.convert_visual_pdf(output_file)

        # ✅ Post both links
        self.post_Report(output_file)




# if __name__ == "__main__":
#     parser = TestReportGenerator(trigger_id=12345, agent_id="agent15dut1", report_title= "Test Report")
#     # parser.get_latest_xml()
#     # parser.generate_html_report()
#     parser.run()
