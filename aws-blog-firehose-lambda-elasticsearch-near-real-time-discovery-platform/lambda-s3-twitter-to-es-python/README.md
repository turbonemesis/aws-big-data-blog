https://docs.aws.amazon.com/lambda/latest/dg//lambda-python-how-to-create-deployment-package.html

~/my-function$ cd v-env/lib/python3.8/site-packages

~/my-function/v-env/lib/python3.8/site-packages$ zip -r9 ${OLDPWD}/function.zip 

~/my-function/v-env/lib/python3.8/site-packages$ cd $OLDPWD

~/my-function$ zip -g function.zip lambda_function.py config.py tweet_utils.py twitter_to_es.py 

zip -g function.zip lambda_function.py config.py github_to_es.py