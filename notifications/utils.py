def generate_notification_live_message(notification: dict):
    """
    A utility method to generate message string from the notification dict
    """

    return f'[{notification.category}]{notification.title}: {notification.description}'