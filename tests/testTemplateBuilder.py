from context import dbhandler
from TemplateBuilder import TemplateBuilder
from lambda_function import buildTemplate

class test:

    def testTemplateBuilder():
        resources = ['temp', 'temp2', 'temp3']
        t = TemplateBuilder()
        for resource in resources:
            t.addResource(resource)
        t.printJSON()

    def test_lambda_function(json):
            buildTemplate(json)

#test.testTemplateBuilder()


json = {
	"sessionAttributes": {
		"projectName": "testStack2"
	},
	"currentIntent": {
		"slots": {
			"resourceOne": "temp",
			"resourceTwo": "temp2"
		}
	}
}

test.test_lambda_function(json)
