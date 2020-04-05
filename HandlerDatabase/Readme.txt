Installazione manuale delle librerie
Installare la libreria pandas per python.
pip install pandas (Se si possiede il gestore pip)
altrimenti installare il gestore pip
sudo apt update
sudo apt install python3-pip

Installare la libreria di influx per Python
pip install influxdb-client
python3 -m pip install influxdb #per la cli


---------------------------------------
per installare le librerie in automatico, bisogna scaricare
pip3 install -U pipenv
pipenv install
pip install influxdb-client
python3 -m pip install influxdb #per la cli


HOW TO RUN
                                                PATH DIR CSV                                    PATH LOG
python3 script.py localhost 8086 /home/broke31/Desktop/PICO/Traceability_code_weld_data /home/broke31/Desktop/PICO/logname.txt

