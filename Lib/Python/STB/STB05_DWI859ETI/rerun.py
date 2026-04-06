import os
import subprocess
import xml.etree.ElementTree as ET


def get_latest_xml():
    # Get the current working directory
    #current_dir = os.getcwd()
    current_dir = "/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/STB05_DWI859ETI"

    # Define the file path relative to the current directory
    file_Path = os.path.join(current_dir)
    path = os.path.join(file_Path, "Report")

    # print("This path:", path)

    # List all XML files in the 'Report' directory
    files = [os.path.join(path, i) for i in os.listdir(path) if
             os.path.isfile(os.path.join(path, i)) and i.endswith(".xml")]

    # Get the most recent file based on creation time
    max_file = max(files, key=os.path.getctime)

    print("Latest XML file:", max_file)
    return max_file


from lxml import etree


def check_testcase_failures(xml_file):
    try:
        # Parse the XML file incrementally
        tree = etree.parse(xml_file)
        root = tree.getroot()

        # Find the <stat> element inside <total>
        stat = root.find(".//statistics//total//stat")

        # Extract the 'fail' attribute
        fail_count = int(stat.attrib.get('fail', '0'))

        # Check if any tests failed and print the count
        if fail_count > 0:
            print(f"{fail_count} test(s) failed.")
            return True
        else:
            print("No tests failed.")
            return False

    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML file: {e}")


def run_robot_tests():
    # Get the latest XML file
    latest_xml = get_latest_xml()

    # Check if any test case has failed
    if check_testcase_failures(latest_xml):

        # Get environment variables
        trigger_id = os.getenv('TRIGGER_ID')
        agent_id = os.getenv('AGENT_ID')
        execution_id = os.getenv('EXECUTION_ID')
        testcase = os.getenv('testcase')
        script_path = os.getenv("SCRIPT_PATH")

        # Check if the necessary environment variables are set
        if not trigger_id or not agent_id or not execution_id:
            print("Environment variables TRIGGER_ID, AGENT_ID, or EXECUTION_ID are not set.")
            return

        # Define the command to run
        command = [
            "python3", "-m", "robot",
            "--rerunfailed", latest_xml,
            "--output", "rerun.xml",
            "--variable", f"trigger_id:{trigger_id}",
            "--variable", f"agent_id:{agent_id}",
            "--variable", f"execution_id:{execution_id}",
            "--variable", f"testcase:{testcase}",  # Include this if applicable
            script_path
        ]

        # Execute the command and check if it was successful
        result = subprocess.run(command, capture_output=True, text=True)

        # After rerun is complete, merge the logs using rebot
        rebot_command = [
            "python3", "-m", "robot.rebot",
            "--timestampoutputs", "--outputdir", "./Report", "--merge", "-o", "merged_output.xml", latest_xml,
            "rerun.xml"

        ]

        # Execute the rebot command to merge logs
        subprocess.run(rebot_command)





    else:
        print("No failed test cases. Skipping Robot Framework rerun.")


# Call the function to check and possibly run the robot tests
run_robot_tests()

