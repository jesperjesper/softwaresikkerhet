FROM python

WORKDIR /2

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyotp
RUN pip install qrcode


COPY . .

EXPOSE 5001

CMD ["python", "run.py"]
