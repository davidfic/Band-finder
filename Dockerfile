FROM ubuntu:16.04

RUN apt update && apt install -y python-pip
COPY . /bandfinder

RUN pip install pip --upgrade &&  pip install -r /bandfinder/requirements.txt


EXPOSE 5555
ENTRYPOINT ["python"]
CMD  ["/bandfinder/run.py"]