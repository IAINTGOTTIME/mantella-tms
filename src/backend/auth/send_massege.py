import smtplib
from email.mime.text import MIMEText
from email.header import Header
from settings import EMAIL_PASS


def send_mail(recipient_mail: str, token: str):
    message = MIMEText(f"To recover your password, enter this token:\n{token}",
                       "plain",
                       "utf-8")
    message["Subject"] = Header("Token for password reset in MantellaTMS", "utf-8")
    message["From"] = "mantellatms@yandex.ru"
    message["To"] = recipient_mail

    smtp = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
    try:
        smtp.set_debuglevel(1)
        smtp.login(user='mantellatms', password=EMAIL_PASS)
        smtp.sendmail(message["From"], message["To"], message.as_string())
    except Exception as ex:
        return ex
    finally:
        smtp.close()
