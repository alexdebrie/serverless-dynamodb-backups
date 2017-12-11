# Automated DynamoDB Backups ⚡️

# Usage

1. Install the [Serverless Framework](https://serverless.com/framework/):

    ```bash
    $ npm install -g serverless
    ```

2. Install this repository as a Serverless project:

   ```bash
   $ sls install --url https://github.com/alexdebrie/serverless-dynamodb-backups && cd serverless-dynamodb-backups
   ```
   
3. Update the `tableName`, `slackWebhook`, and `backupRate` in the `custom` block of `serverless.yml`. See [Configuration](#configuration) for more details.

4. Deploy!

   ```bash
   $ sls deploy
   ```

# Configuration

There are three things to configure in the `custom` block of `serverless.yml`:

- `tableName` - **required** - The name of the DynamoDB table you want to backup
- `backupRate` - **required** - The schedule on which you want to backup your table. You can use either `rate` syntax (`rate(1 hour)`) or `cron` syntax (`cron(0 12 * * ? *)`). See [here](https://serverless.com/framework/docs/providers/aws/events/schedule/) for more details on configuration.
- `slackWebhook` - **optional** - An HTTPS endpoint for an [incoming webhook](https://api.slack.com/incoming-webhooks) to Slack. If provided, it will send success + error messages to a Slack channel when it runs.

# Notes

- As of 12/11/2018, DynamoDB backups aren't working for all tables. It appears to be tables created after a certain time, though I don't know what that cutoff is. If your table is ineligible, you'll get a `ContinuousBackupsUnavailableException`.
- The `botocore` package bundled with Lambda doesn't include the new features announced at reInvent. As a result, I added the `dynamodb` data directory from a more recent version of `botocore` and set the `AWS_DATA_PATH` environment variable to recognize it.

# Potential improvements

- **Multiple tables?** Currently you would need to deploy a separate service for each table you want to back up. A future solution have a file that lists all tables to be backed up.
- **Better control on notifications?** We could implement email or SMS messages, as well as the ability to only notify on failures.
- **Cleanup of old backups?** It could be nice to delete all backups older than X days to avoid being charged for backup storage.