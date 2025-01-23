# TaiGer Portal Lambda with AWS CDK TypeScript

This package includes Cron job Lambda

- daily snapshot of back-up TaiGer Portal MongodbDB data in AWS S3 bucket.
- daily email reminder for TaiGer Portal users.
- daily snapshot of subset of TaiGer portal data in the S3 Bucket shared with TaiGer partner Tenfold AI for customized content recommendation.
- AWS CDK Typescript stack that deploy Lambda, and IAM permissions.

## Useful commands

-   `npm run build` compile typescript to js
-   `npm run watch` watch for changes and compile
-   `npm run test` perform the jest unit tests
-   `npx cdk deploy` deploy this stack to your default AWS account/region
-   `npx cdk diff` compare deployed stack with current state
-   `npx cdk synth` emits the synthesized CloudFormation template
