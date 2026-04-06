from syncReports import SendReport
from Visual_reports import TestReportGenerator
import os, sys
# obj = syncReports()
# obj.syncReports(sys.argv[1])
obj = SendReport(sys.argv[1], sys.argv[2])
obj.SendRP()
obj2 = TestReportGenerator(sys.argv[1], sys.argv[2])
obj2.run()
