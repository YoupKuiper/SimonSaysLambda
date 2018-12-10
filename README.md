# SimonSays version 1.0

To deploy the SimonSays bot on a custom system please use the following steps:

1. Create an S3 bucket named "simonsaysresourcebucket"

2. Upload the contents of the simonsays_release_resources_v1.0.zip to this bucket

3. Create a stack using the provided setup_simonssays.json cloudformation template.

4. In the lex console, select the dropdown Actions and choose import. Select the simonsays_release_bot_v1.0.zip and choose import

5. In the lex console, select the imported bot, and choose build. Wait for the build to finish and select publish.
