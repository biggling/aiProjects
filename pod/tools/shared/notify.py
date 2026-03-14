import apprise
from tools.shared.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from tools.shared.logger import get_logger

logger = get_logger("notify")


def notify(title: str, body: str, level: str = "info") -> bool:
    """Send a notification via Apprise (Telegram if configured).

    Args:
        title: Notification title.
        body: Notification body text.
        level: One of "info", "success", "warning", "failure".

    Returns:
        True if notification sent, False otherwise.
    """
    apobj = apprise.Apprise()

    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        apobj.add(f"tgram://{TELEGRAM_BOT_TOKEN}/{TELEGRAM_CHAT_ID}")

    if len(apobj) == 0:
        logger.warning("No notification services configured, skipping")
        return False

    notify_type = getattr(apprise.NotifyType, level.upper(), apprise.NotifyType.INFO)

    result = apobj.notify(title=title, body=body, notify_type=notify_type)
    if result:
        logger.info(f"Notification sent: {title}")
    else:
        logger.error(f"Notification failed: {title}")

    return result
