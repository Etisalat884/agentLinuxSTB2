# import socket
# import etisalat_keycodes
# import time
# import RedRatHub

# # def etisalat_tv_cmds(button_name):
# #     print("Button pressed--------",button_name)
# #     button_value = etisalat_keycodes.etisalat_buttons[button_name]
# #     send_data(button_value)
# #     time.sleep(1)



# def send_data(data):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(('192.168.1.33', 4998))
#     # client.connect(('192.168.0.44', 4998))

#     client.send(data.encode())
#     from_server = client.recv(4096)
#     client.close()
#     print(from_server.decode())




# def etisalat_tv_cmds(button_name):
#     try:
#         # Create a client and connect to the RedRatHub
#         client = RedRatHub.Client()
#         client.OpenSocket('192.168.1.24', 40000)

#         # Format the command string
#         cmd = f'ip="192.168.1.143" dataset="Jade_Linux" signal="{button_name}" output="6:100"'
        
#         print(f"Sending command: {cmd}")
        
#         # Send the command to the RedRatHub
#         ret = client.SendMessage(cmd)
#         print(f"Response: {ret}")
#         # time.sleep(1)
#         return True
#     except Exception as e:
#         print(f"Error sending command: {e}")
#         return False
    
# def etisalat_tv_cmds_numbers(button_name):
#     try:
#         # Create a client and connect to the RedRatHub
#         client = RedRatHub.Client()
#         client.OpenSocket('192.168.1.24', 40000)

#         # Format the command string
#         cmd = f'ip="192.168.1.143" dataset="Jade_Linux" signal="{button_name}" output="6:100"'
        
#         print(f"Sending command: {cmd}")
        
#         # Send the command to the RedRatHub
#         ret = client.SendMessage(cmd)
#         print(f"Response: {ret}")
#         time.sleep(1)
#         return True
#     except Exception as e:
#         print(f"Error sending command: {e}")
#         return False

# # etisalat_tv_cmds("POWER")

# from Signal import etisalat_keycodes
# from Signal import RedRatHub
import socket
# import etisalat_keycodes
import time
# import RedRatHub
import sys
sys.path.append("/home/ltts/Documents/evqual_automation/agentLinuxSTB2/workspace/Lib/Python/STB/STB05_DWI859ETI")

from Signal import RedRatHub

# def etisalat_tv_cmds(button_name):
#     print("Button pressed--------",button_name)
#     button_value = etisalat_keycodes.etisalat_buttons[button_name]
#     send_data(button_value)
#     time.sleep(1)



def send_data(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.33', 4998))
    # client.connect(('192.168.0.44', 4998))

    client.send(data.encode())
    from_server = client.recv(4096)
    client.close()
    print(from_server.decode())




def etisalat_tv_cmds(button_name):
    try:
        # Create a client and connect to the RedRatHub
        client = RedRatHub.Client()
        client.OpenSocket('192.168.1.24', 40000)

        # Format the command string
        cmd = f'ip="192.168.1.143" dataset="Linux_DWI259ETI" signal="{button_name}" output="6:100"'
        
        print(f"Sending command: {cmd}")
        
        # Send the command to the RedRatHub
        ret = client.SendMessage(cmd)
        print(f"Response: {ret}")
        # time.sleep(1)
        return True
    except Exception as e:
        print(f"Error sending command: {e}")
        return False
    
def etisalat_tv_cmds_numbers(button_name):
    try:
        # Create a client and connect to the RedRatHub
        client = RedRatHub.Client()
        client.OpenSocket('192.168.1.24', 40000)

        # Format the command string
        cmd = f'ip="192.168.1.143" dataset="Linux_DWI259ETI" signal="{button_name}" output="6:100"'
        
        print(f"Sending command: {cmd}")
        
        # Send the command to the RedRatHub
        ret = client.SendMessage(cmd)
        print(f"Response: {ret}")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Error sending command: {e}")
        return False

# etisalat_tv_cmds("POWER")

