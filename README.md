# SimonSays version 1.0

To deploy the SimonSays bot on a custom system please use the following steps:

1. Create an S3 bucket named "simonsaysresourcebucket"

2. Upload the contents of the 'simonsaysresourcebucket' folder to this bucket

3. Create a CloudFormation stack using the provided setup_simonssays.json CloudFormation template.

4. Add your mobile phone number in the 'PhoneNumber' field in the parameters section (format: +31612345678)

5. Launch the stack, the stack name doesn't matter but check the box for: 'I acknowledge that AWS CloudFormation might create IAM resources with custom names.'

6. You will receive an sms on the provided phone number. Open the SimonSays iOS/Android app, go to settings and copy paste the content of the received sms into the 'Identity Pool Id' field.

7. Select the region in which you deployed the Lex bot for the 'region' field and (optionally) put your name into the 'name' field

8. In the AWS console, go to Lex and click on the bot named 'SimonSays'. Select 'Build' (in the top right corner).

9. Once the build is done, you can use the iOS/Android app to talk to the SimonSays bot!
