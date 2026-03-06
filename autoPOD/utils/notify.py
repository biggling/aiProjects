"""Email and Slack notification helpers."""
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from config import SLACK_WEBHOOK_URL, SENDER_EMAIL, RECIPIENT_EMAIL, get_logger

logger = get_logger("notify")


def slack(message: str) -> bool:
    if not SLACK_WEBHOOK_URL:
        logger.debug("Slack webhook not configured, skipping.")
        return False
    try:
        r = requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=10)
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Slack notification failed: {e}")
        return False


def email_html(subject: str, html_body: str) -> bool:
    if not (SENDER_EMAIL and RECIPIENT_EMAIL):
        logger.debug("Email not configured, skipping.")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, "")  # Use app password in .env
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        return True
    except Exception as e:
        logger.error(f"Email notification failed: {e}")
        return False


def alert_order(platform: str, listing_title: str, revenue: float):
    slack(f":moneybag: New order on *{platform}*: {listing_title} — ${revenue:.2f}")


def alert_fulfillment_stuck(order_id: int, hours: int):
    slack(f":warning: Order #{order_id} fulfillment stuck for {hours}h — check Printify!")
