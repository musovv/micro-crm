
class Utils:
    """
    This class is used to provide utility functions to the application.
    """
    @staticmethod
    def fill_model(cls, **kwargs):
        """
        This method is used to create and fill a instance with data from a dictionary.
        :param cls: class
        :param kwargs: dictionary
        :return: None
        """
        instance = cls()
        for key, value in kwargs.items():
            setattr(instance, key, value)

        return instance

    @staticmethod
    def remove_none_values(d: dict):
        """
        This method is used to remove None values from a dictionary.
        :param d: dictionary
        :return: dictionary
        """
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def generate_short_guid():
        import base64
        import time
        # Get the current time in milliseconds
        timestamp = int(time.time() * 1000)
        timestamp_bytes = timestamp.to_bytes(8, 'big')

        # Encode bytes to Base64 and decode to string, removing trailing '=' characters
        base64_encoded = base64.urlsafe_b64encode(timestamp_bytes).decode('utf-8').rstrip('=')

        return base64_encoded

