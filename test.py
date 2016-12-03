import sys
from PyQt5.QtWidgets import QApplication
import screenshot

app = QApplication(sys.argv)

screenshot.captureScreen(QApplication.screens()[1]).save("screen.png")
screenshot.captureDesktop().save("desktop.png")
screenshot.captureRegion(0, 0, 500, 500).save("r1.png")
screenshot.captureRegion(0, 0, 1920*2, 1200).save("r2.png")
screenshot.captureRegion(1800, 100, 400, 400).save("r3.png")