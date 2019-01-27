import errno
import os
import re


class FileSystem:
    @staticmethod
    def build_folder_name(url):
        """
        Removes or replaces characters from the url that cannot be used for folder names
        :param url
        :return:
        """

        if '@' in url:
            auth, base = url.split('@')
        else:
            base = re.sub(
                "^http[s]?://",
                "",
                url
            )

        base = re.sub(
            r"[/]",
            "-",
            base
        )

        return base

    @staticmethod
    def create_folder(name):
        try:
            os.makedirs(name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
