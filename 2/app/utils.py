import pyotp
import qrcode
import os


def generate_totp_secret():
    return pyotp.random_base32()




def generate_qr_code_uri(username, totp_secret):
    totp = pyotp.TOTP(totp_secret)
    totp_uri = totp.provisioning_uri(name=username, issuer_name='YourApp')

    img = qrcode.make(totp_uri)

    img.save("app/static/qrcode.png")

    return "static/qrcode.png"


def verify_totp(secret, totp_code):
    totp = pyotp.TOTP(secret)
    return totp.verify(totp_code)