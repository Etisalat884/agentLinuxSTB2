import os
import http.server
import threading
import json
import requests
import os
from datetime import datetime
import pathlib
import socketserver
import subprocess

import asyncio
from pyppeteer import launch
import os



class SendReport:
    def __init__(self, trigger_id, agent_id):
        self.trigger_id = trigger_id
        self.agent_id = agent_id

    # Fetch latest report file   
    def syncReports(self):
        file_Path = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI'
        path = file_Path + "/Report/"
        print("this path",path)
        files = [path + i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i)) and i.endswith(".html")]

        print("this whole fles path ", files)
        max_file = max(files, key=os.path.getctime)
        latest_file = os.path.basename(max_file)
        print(latest_file)
        self.latest_file = latest_file

    def syncLogs(self):
        file_Path = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI'
        project_dir = file_Path
        folder_name = os.path.basename(project_dir)
        path = file_Path + "/OutputRecordings/"
        files = [path + i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i)) and i.endswith(".mp4")]
        print(files)
        max_file = max(files, key=os.path.getctime)
        filename = "output"
        latest_file = os.path.basename(max_file)

    def get_latest_log_file(self):
        file_Path = '/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI'
        path = file_Path + "/Report/"
        print("log path:", path)

        log_files = [
            path + i for i in os.listdir(path)
            if os.path.isfile(os.path.join(path, i))
            and i.endswith(".html")
            and i.startswith("log-")
        ]
        print("log files:", log_files)
        if not log_files:
            print("No log files found")
            return None
        latest_log = max(log_files, key=os.path.getctime)
        latest_log_file = os.path.basename(latest_log)
        print("latest log file:", latest_log_file)
        return latest_log_file

    def Post_Result(self, addr):
        print("JS,", addr)
        url = "http://192.168.1.58:5000/update_data_dashboard?key="
        data1 = json.dumps({"trigger_id": self.trigger_id, "agent_id": self.agent_id})
        print("this data1", data1)
        data2 = json.dumps(addr)
        print(type(data2))
        print("this data2", data2)
        x = requests.post(url + data1 + "&attribute=" + data2)
        print("this is data", url + data1 + "&attribute=" + data2)
        return x

    def Post_Logs(self, addr):
        print("JS,", addr)
        url = "http://192.168.1.58:5000/update_data_dashboard?key="
        data1 = json.dumps({"trigger_id": self.trigger_id, "agent_id": self.agent_id})
        data2 = json.dumps(addr)
        # print(type(data), "jsondata")
        x = requests.post(url + data1 + "&attribute=" + data2)
        print("this is url", url + data1 + "&attribute=" + data2)
        return x




    def access_html_file(self, html_file_path):
        PORT = 8084

        file_name = os.path.basename(html_file_path)
        print("file name",file_name)

        # Use your known IP
        http_link = f"http://192.168.1.101:8084/{file_name}"

        print(f"Access your HTML file at: {http_link}")
        return http_link

        




    def access_logs_file(self, file_log_url):
        PORT = 8085  # Change port number if needed
        # Handler = http.server.SimpleHTTPRequestHandler
        # Function to access a specific HTML file
        # Change directory to where the HTML file is located
        os.chdir(os.path.dirname(os.path.abspath(file_log_url)))

        # Extract the file name from the path
        file_logs_name = os.path.basename(file_log_url)

        # Print the HTTP link to access the HTML file    /home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Reports

        http_log_link = f"http://192.168.1.101:{PORT}/{file_logs_name}"
        print(f"Access your HTML file at: {http_log_link}")
        return http_log_link
    


    def convert_pdf(self, html_file_path):
        import asyncio
        import os
        from pyppeteer import launch

        pdf_file = html_file_path.replace(".html", "_expanded.pdf")

        async def _convert():
            browser = await launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )

            page = await browser.newPage()

            # ✅ Load HTML file
            html_url = f"file://{os.path.abspath(html_file_path)}"
            print("Opening URL:", html_url)

            await page.goto(html_url, {'waitUntil': 'domcontentloaded'})

            # ✅ Wait until Robot report content appears
            try:
                await page.waitForFunction(
                    "document.body.innerText.includes('Test Statistics')",
                    {'timeout': 15000}
                )
                print("✅ Robot report loaded")
            except Exception:
                print("❌ ERROR: Robot report not loaded properly")
                await browser.close()
                return None

            # ✅ Extra wait for JS
            await asyncio.sleep(5)

            # ✅ Expand all sections
            print("Expanding all sections...")

            await page.evaluate("""
                () => {
                    if (typeof expandAll === 'function') {
                        expandAll();
                    }

                    document.querySelectorAll('.collapsed').forEach(el => {
                        try { el.click(); } catch(e) {}
                    });
                }
            """)

            # ✅ Wait after expansion
            await asyncio.sleep(10)

            # ✅ Validate again before PDF
            content = await page.content()

            if "Test Statistics" not in content:
                print("❌ ERROR: Not a valid Robot report page")
                await browser.close()
                return None

            print("Generating PDF...")

            # ✅ Generate PDF
            await page.pdf({
                "path": pdf_file,
                "format": "A4",
                "printBackground": True,
                "margin": {
                    "top": "10mm",
                    "bottom": "10mm",
                    "left": "10mm",
                    "right": "10mm"
                }
            })

            await browser.close()

        # ✅ Run async
        asyncio.get_event_loop().run_until_complete(_convert())

        # ✅ Check file created
        if not os.path.exists(pdf_file):
            print("❌ PDF not created")
            return None

        print("✅ PDF generated:", pdf_file)

        return pdf_file
    # Example usage:
    def SendRP(self):

        self.syncReports()
        file_name = self.latest_file
        directory_path = r'/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI/Report'
        html_file_path = f"{directory_path}/{file_name}"
        print("report path",html_file_path)
        html_report_file_path = self.access_html_file(html_file_path)
        print("this is whole report",html_report_file_path)


        # log_file = self.get_latest_log_file()
        # log_html_path = f"{directory_path}/{log_file}"
        # print("log file path", log_html_path)


        # pdf_path = self.convert_pdf(html_file_path)
        # html_pdf_path = self.access_html_file(pdf_path)
        # print("this is report pdf", html_pdf_path)



        # ✅ Generate PDF
        pdf_path = self.convert_pdf(html_file_path)

        if not pdf_path:
            print("❌ PDF generation failed")
            return

        # ✅ WAIT (important for server to pick file)
        import time
        time.sleep(2)

        # ✅ Generate correct HTTP link
        pdf_file_name = os.path.basename(pdf_path)
        html_pdf_path = f"http://192.168.1.101:8084/{pdf_file_name}"

        print("✅ PDF URL:", html_pdf_path)
    


        statusres = {"trigger_id": self.trigger_id, "agent_id": self.agent_id, "exec_reports": html_report_file_path, "report_pdf": html_pdf_path}
        self.Post_Result(statusres)
        self.syncLogs()
        directory_log_path = r'/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Record/STB05_DWI859ETI/OutputRecordings'
        files = [os.path.join(directory_log_path, f) for f in os.listdir(directory_log_path) if
                 os.path.isfile(os.path.join(directory_log_path, f))]

        # Find the most re[]cently created file
        max_file = max(files, key=os.path.getctime)
        print("this max_file:", max_file)
        latest_file = os.path.basename(max_file)
        file_log_url = os.path.join(directory_log_path, latest_file)
        print("this log file path", file_log_url)
        print("line 120")
        http_log_link = self.access_logs_file(file_log_url)
        statuslogs = {"trigger_id": self.trigger_id, "agent_id": self.agent_id, "dev_logs": http_log_link}
        print("this is statuslogs:", statuslogs)
        self.Post_Logs(statuslogs)
        return statusres

# O = SendReport('12345', 'agentLinuxSTB2')
# O.SendRP()

