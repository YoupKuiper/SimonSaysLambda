import subprocess
import json
import os
os.chdir("/Users/spreng/Desktop")

synonymfile = open("create.txt", "r")
synonymfile2 = open("project.txt", "r")
valid = []
invalid = []
count = 0
for synonym in synonymfile:
    try:
        for synonym2 in synonymfile2:
            count = count + 1
            try:
                synonym2 = synonym2.replace("\n", "")
                synonym = synonym.replace("\n", "")
                p = subprocess.check_output("aws lex-runtime post-text --region eu-west-1 --bot-name SimonSays --bot-alias \"\$LATEST\" --user-id UserOne --input-text " + "\"" + synonym + " a " + synonym2 + "\"", shell=True)
                p_decoded = p.decode('ascii')
                json_p_decoded = p_decoded.replace("'", "\"")
                responseJSON = json.loads(json_p_decoded)
                if (responseJSON["intentName"] == "CreateProject"):
                    valid.append(synonym + " a " + synonym2)
                else:
                    invalid.append(synonym + " a " + synonym2)
            except:
                invalid.append(synonym + " a " + synonym2)
                print("An exception turned up when using " + synonym + " a " + synonym2)
    except:
        continue

print(str(len(valid)) + "Values are valid " + str(len(invalid)) + " Values came out as invalid")
print(valid)
print("_________")
print(invalid)
print(count)
synonymfile.close()
synonymfile2.close()
