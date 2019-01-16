# SimonSays version 1.0

**Prerequisites:**

- Make sure the role AWSServiceRoleForLexBots exists in IAM
  If the role doesnt exist:
  1. Go to IAM and select Create Role
  2. For the service that will use the role, select Lex
  3. For the use case, select Lex - bots
  4. Keep clicking next until the role has been created




**To deploy the SimonSays bot on a custom system please use the following steps:**

1. Create an S3 bucket named "simonsaysresourcebucket", make sure to select a region that has lex services available including: Oregon, Northern Virginia and Ireland. If the bucket name already exists, add something to the name to make it unique.

2. Upload the **contents** of the "simonsaysresourcebucket" folder in this repository to the "simonsaysresourcebucket".

3. Create a CloudFormation stack using the provided setup_simonssays.json CloudFormation template. Create this stack in the same region as the bucket you created in step 1.

4. Add your mobile phone number in the 'PhoneNumber' field in the parameters section (format: +31612345678)

5. Put the name of the "simonsaysresourcebucket" you created in the Bucket field.

6. Launch the stack, the stack name doesn't matter but check the box for: 'I acknowledge that AWS CloudFormation might create IAM resources with custom names.'

7. You will receive an sms on the provided phone number (if the 1$ sms limit hasn't been reached yet). Open the SimonSays iOS/Android app, go to settings and copy paste the content of the received sms into the 'Identity Pool Id' field. Select the region in which you deployed the Lex bot for the 'region' field and (optionally) put your name into the 'name' field.

8. Upload the **contents** of the "demoresourcebucket" to the bucket referenced in the exports of the created stack.

9. In the AWS console, go to Lex and click on the bot named 'SimonSays'. Select 'Build' (in the top right corner).

10. Once the build is done, you can use the iOS/Android app to talk to the SimonSays bot!
