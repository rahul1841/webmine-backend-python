FROM python:3.9-slim

# Install dependencies including wget and unzip
RUN apt-get update -y && \
    apt-get install -y libasound2 libatk-bridge2.0-0 libgtk-4-1 libnss3 xdg-utils wget unzip && \
    # Download and install Chrome
    /bin/bash -c "wget -q -O chrome-linux64.zip https://bit.ly/chrome-linux64-121-0-6167-85 && \
                   unzip chrome-linux64.zip && \
                   rm chrome-linux64.zip && \
                   mv chrome-linux64 /opt/chrome/ && \
                   ln -s /opt/chrome/chrome /usr/local/bin/" && \
    # Download and install Chromedriver
    /bin/bash -c "wget -q -O chromedriver-linux64.zip https://bit.ly/chromedriver-linux64-121-0-6167-85 && \
                   unzip -j chromedriver-linux64.zip chromedriver-linux64/chromedriver && \
                   rm chromedriver-linux64.zip && \
                   mv chromedriver /usr/local/bin/"

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
