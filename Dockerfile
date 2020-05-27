FROM python:3
WORKDIR /SoftwareDesign
ENV FLASK_APP hello.py
ENV FLASK_RUN_HOST 0.0.0.0
ADD hello.py /
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
