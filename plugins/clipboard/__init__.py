''' cap n snap plugin to put the captured data on the clipboard '''

from .clipboard import ClipboardDestination

def init(host):
	host.registerDestination(ClipboardDestination())
#enddef

info = {
	'name' : 'Clipboard',
	'version' : 1.0
}