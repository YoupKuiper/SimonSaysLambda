from context import TemplateBuilder
from context import buildTemplate


class test:

    def testTemplateBuilder():
        resources = ['temp', 'temp2', 'temp3']
        t = TemplateBuilder()
        for resource in resources:
            t.addResource(resource)
        t.printJSON()

    def test_lambda_function(json):
            buildTemplate(json)

test.testTemplateBuilder()
