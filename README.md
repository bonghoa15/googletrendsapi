# googletrendsapi
The simple script to crawl google trends api using input keywords then writting results to GQB. Using Google Cloud Functions, Pub/Sub and google scheduler to crawl at specific interval. \
Step 1: Clone this repo/create similar folder in Google cloudshell\
Step 2: Modify infomation inside [] with your proper project/dataset/table\
Step 3: Install packages in requirements.txt. Run command: "pip3 install -r requirements.txt" \
Step 4: deploy cloud function on pub/sub: \
gcloud functions deploy [FUNCTION_NAME] --entry-point main --runtime python37 --trigger-resource [TOPIC_NAME] --trigger-event  google.pubsub.topic.publish --timeout 540s \
Step 5: Deploy cron job in google cloudshell\
gcloud scheduler jobs create pubsub [JOB_NAME] --schedule [SCHEDULE] --topic [TOPIC_NAME] --message-body [MESSAGE_BODY]\
Reference: https://cloud.google.com/blog/products/application-development/how-to-schedule-a-recurring-python-script-on-gcp
