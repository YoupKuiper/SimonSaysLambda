import json

class Template:


    def __init__(self):
        self.__tempBase = {}

    def addResource(self, type, properties, name):
        type.update(properties)
        self.__tempBase.update({name : type})

    def getVPC(self):
        return self.__tempBase.get("VPC")

    def addVPC(self):
        type = {"Type":"AWS::EC2::VPC"}
        properties = {"Properties":{"CidrBlock":"10.0.0.0/16"}}
        properties.update(type)
        vpc = {"VPC" : properties}
        self.__tempBase.update(vpc)

    def addSubnet(self, amount, vpcid):
        type = {"Type":"AWS::EC2::Subnet"}
        for x in range(0, amount):
            properties = {"Properties" : {"CidrBlock" : "10.0." + str(x) + ".0/24", "VpcId" : {"Ref": vpcid}}}
            properties.update(type)
            subnet = {"subnet" + str(x) : properties}
            self.__tempBase.update(subnet)

    def printJSON(self):
        resources = {"Resources" : self.__tempBase}
        return json.dumps(resources)
