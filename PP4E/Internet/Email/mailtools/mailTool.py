"""
###############################################################################
common superclasses: used to turn trace massages on/off
###############################################################################
"""

class MailTool:                    # superclass for all mail tools
    def trace(self, message):      # redef me to disable or log to file
        print(message)

class SilentMailTool:              # to mixin instead of subclassing
    def trace(self, message):
        pass
