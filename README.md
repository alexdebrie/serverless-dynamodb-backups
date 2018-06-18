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

3. Update the required [configuration](#configuration) in the `custom` block of `serverless.yml`.

4. Deploy!

   ```bash
   $ sls deploy
   ```

# Configuration

There are three ways you can specify which tables to backup:

1. **Regex on all tables in region.** The function can call the `ListTables` API and include all tables whose name matches a given regular expression. This is the most dynamic configuration, as you won't need to redeploy this function every time you add a new DynamoDB table. This works best if you have a specified naming scheme for your tables, such as prefixing all tables with the stage. Then you can add a pattern of `"^(prod-)."` to match all tables that start with `prod-`. To use this method, put your regular expression in the `tableRegex` property.

2. **Specify multiple table names in an included file.** If you have a list of tables you want to back up, you can place their names in a local file and specify the name of the file in the `tableFile` property. The format must be valid JSON that is a list of strings. A `tables.json` file is included in this repo as an example.

3. **Specify a single table via environment variable.** If you only have one table to backup, you can specify its name via the `tableName` property.

In addition to the table configuration, there is also the following configuration:

- `backupRate` - **required** - The schedule on which you want to backup your table. You can use either `rate` syntax (`rate(1 hour)`) or `cron` syntax (`cron(0 12 * * ? *)`). See [here](https://serverless.com/framework/docs/providers/aws/events/schedule/) for more details on configuration.
- `slackWebhook` - **optional** - An HTTPS endpoint for an [incoming webhook](https://api.slack.com/incoming-webhooks) to Slack. If provided, it will send success + error messages to a Slack channel when it runs.

- `backupRemovalEnabled` - **optional** - Setting this value to **true** will enable cleanup of old backups. See the below option, `backupRetentionDays`, to specify the retention period. By default, backup removal is disabled.

- `backupRetentionDays` - **optional** - Specify the number of days to retain old snapshots. For example, setting the value to **2** will remove all snapshots that are older then 2 days from today.

# Notes

- As of 12/11/2018, DynamoDB backups aren't working for all tables. It appears to be tables created after a certain time, though I don't know what that cutoff is. If your table is ineligible, you'll get a `ContinuousBackupsUnavailableException`.
- The `botocore` package bundled with Lambda doesn't include the new features announced at reInvent. As a result, I added the `dynamodb` data directory from a more recent version of `botocore` and set the `AWS_DATA_PATH` environment variable to recognize it.

# Potential improvements

- **Better control on notifications?** We could implement email or SMS messages, as well as the ability to only notify on failures.

