# coding:utf-8
 
import os
import pyinotify

class EventHandler(pyinotify.ProcessEvent):
	"""事件处理"""
	def process_IN_CREATE(self, event):
		print   "Create file: %s "  %   os.path.join(event.path,event.name)
		
	def process_IN_DELETE(self, event):
		print   "Delete file: %s "  %   os.path.join(event.path,event.name)
		
	def process_IN_MODIFY(self, event):
		print   "Modify file: %s "  %   os.path.join(event.path,event.name)
 
def FSMonitor(path = '.'):
	wm = pyinotify.WatchManager()
	mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
	notifier = pyinotify.Notifier(wm, EventHandler())
	wm.add_watch(path, mask, rec = True, auto_add = True)
	print 'now starting monitor %s'%(path)
	while True:
		try:
			notifier.process_events()
			if notifier.check_events():
				notifier.read_events()
		except KeyboardInterrupt:
			notifier.stop()
			break
 
if __name__ == "__main__":
    FSMonitor()