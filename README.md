# SimonSays version 1.0

To deploy the SimonSays bot on a custom system please use the following steps:

1. Create two S3 buckets, name one "simonsaysresourcebucket" and the other one "demoresourcebucket", make sure to select a region that has lex services available including: Oregon, Northern Virginia and Ireland.

2. Upload the contents of the "simonsaysresourcebucket" folder in this repository to the "simonsaysresourcebucket" and do the same for the "demoresourcebucket".

3. Create a CloudFormation stack using the provided setup_simonssays.json CloudFormation template. Create this stack in the same region as the bucket you created in step 1.

4. Add your mobile phone number in the 'PhoneNumber' field in the parameters section (format: +31612345678)

5. Launch the stack, the stack name doesn't matter but check the box for: 'I acknowledge that AWS CloudFormation might create IAM resources with custom names.'

6. You will receive an sms on the provided phone number. Open the SimonSays iOS/Android app, go to settings and copy paste the content of the received sms into the 'Identity Pool Id' field.

7. Select the region in which you deployed the Lex bot for the 'region' field and (optionally) put your name into the 'name' field

8. In the AWS console, go to Lex and click on the bot named 'SimonSays'. Select 'Build' (in the top right corner).

9. Once the build is done, you can use the iOS/Android app to talk to the SimonSays bot!
