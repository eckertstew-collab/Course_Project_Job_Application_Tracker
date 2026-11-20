# Course_Project_Job_Application_Tracker


1. Open MySQL workbench and execute the sql script (scheme.sql) provided (You may have to modify database.py so the databases host, password, and username are correct)
2.  install virtual studio code
3.  open virtual studio code and make a new terminal
4.  open the folder provided using virual stuio code or other another code editor.
5.  enter the following lines into the terminal one at a time:
    </br>
    python -m venv venv
    </br>
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    </br>
    .\venv\Scripts\Activate.ps1
    </br>
    python -m pip install flask mysql-connector-python
    </br>
    python -m pip list
    </br>
    python test_connection.py
    </br>
    python app.py
    </br>
6.  By now you should be able to access the URL
   </br> 
    This is the local address for the job tracker: http://127.0.0.1:5000
