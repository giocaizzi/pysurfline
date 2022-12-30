"""update readme.md forecast"""

from pysurfline import SurfReport

params = {
    "spotId": "5842041f4e65fad6a7708890",
    "days": 3,
    "intervalHours": 3,
}
report = SurfReport(params)
report.api_log

f = report.plot()
f.savefig("docsrc/source/images/surfreport_pipeline.jpeg")
