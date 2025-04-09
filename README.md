# AWSからSlackに毎日利用明細を通知するAWS SAMのApp

## AWS SAMの使い方

AWS SAMを使用するために前提条件を満たす
https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/prerequisites.html

こちらのサイトを参考にAWS SAMをインストール
https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/install-sam-cli.html

```bash
which sam
sam --version
```
でしっかりシンボリックリンクが作成されており、バージョンが表示されるとインストール完了です。

```bash
sam build
```
でビルドします。
```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket budget-notify-lambda-bucket
```
を実行しpackage.yamlを作成します。このとき、保存するs3バケットはあらかじめ作っておき、そのバケット名をコマンドラインで指定する。
今回のコマンドならbudget-notify-lambda-bucketに保存される。

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name NotifyBillingToSlack \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides SlackWebhookUrl="slackのWebhookURLを入れる"
```

上記コマンドでデプロイする。コマンドでSlackのWebhookURLを入れているのはgit上にWebhookURLを上げないためである。

上記コマンドを実行後yesと答えると、aws上でCloudFormationが実行され、EventBridgeとそれに紐づいたLambda関数、IAMポリシーが作成される。
`./template.yaml`内の

```
Schedule: cron(0 0 * * ? *)  
```
にてEventBridgeの起動時間、起動頻度を設定している。
