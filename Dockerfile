FROM ubuntu:16.04

RUN apt update && apt install -y python-pip

RUN mkdir /bandfinder                                                         
ADD . /bandfinder
RUN pip install pip --upgrade &&  pip install -r /bandfinder/requirements.txt
EXPOSE 5001
ENTRYPOINT ["python"]
CMD  ["/bandfinder/run.py"]