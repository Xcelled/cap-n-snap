''' Attempts to make some parts of PyQt5 friendlier to use '''
import loggingstyleadapter
log = loggingstyleadapter.getLogger(__name__)

# QKeySeq mods
log.debug("Monkey-patching QKeySequence")
from PyQt5.QtGui import QKeySequence

def QKeySequence_str(seq): return seq.toString()
QKeySequence.__str__ = QKeySequence_str
QKeySequence.__repr__ = QKeySequence_str

def QKeySequence_Hash(seq):	return hash(seq.toString())
QKeySequence.__hash__ = QKeySequence_Hash