"""
Find the Process Using the Port:
On Linux/macOS, you can use:
sudo lsof -i :PORT_NUMBER

On Windows, you can use:
netstat -ano | findstr :PORT_NUMBER
============================================
Terminate the Process:

On Linux/macOS, you can use:
sudo kill -9 PID

On Windows, you can use:
taskkill /PID typeyourPIDhere /F

Replace PID with the actual process ID.
============================================
Verify the Port is Closed:

On Linux/macOS:
sudo lsof -i :PORT_NUMBER

On Windows:
netstat -ano | findstr :PORT_NUMBER
"""


import http.server
import socketserver
import yaml
import os

with open("configs/app_config.yml") as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

PORT = app_config["serve"]["port"]
DIRECTORY1 = app_config["directories"]["data_directory"]
DIRECTORY2 = app_config["directories"]["data_directory_2"]


# class SingleDirectoryHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, directory=DIRECTORY1, **kwargs)


class MultiDirectoryHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Split the path to get the first directory component
        parts = path.split('/', 2)
        if len(parts) > 1:
            first_directory = parts[1]
            # Check if the first directory matches any of your target directories
            if first_directory == os.path.basename(DIRECTORY1):
                path = os.path.join(DIRECTORY1, *parts[2:])

            elif first_directory == os.path.basename(DIRECTORY2):
                path = os.path.join(DIRECTORY2, *parts[2:])
            else:
                # If the first part of the path is not a directory, check both directories for the file
                file_path1 = os.path.join(DIRECTORY1, first_directory)
                file_path2 = os.path.join(DIRECTORY2, first_directory)
                if os.path.isfile(file_path1):
                    return file_path1
                elif os.path.isfile(file_path2):
                    return file_path2
        # If there's no match, use the default directory
        return super().translate_path(path)


with socketserver.TCPServer(("", PORT), MultiDirectoryHTTPRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()