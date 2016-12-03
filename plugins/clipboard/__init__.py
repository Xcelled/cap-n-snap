''' cap n snap plugin to put the captured data on the clipboard '''

from .clipboard import ClipboardPlugin

def getPlugin(*args, **kwargs):
	return ClipboardPlugin(*args, **kwargs)
#enddef

info = {
	'name' : 'Clipboard',
	'version' : 1.0
}