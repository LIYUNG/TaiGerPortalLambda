import { Construct } from "constructs";
import { LambdaStack } from "./lambda-stack";
import { Stage, StageProps } from "aws-cdk-lib";
import { APP_NAME_TRANSCRIPT_ANALYZER } from "../configuration";

interface DeploymentkProps extends StageProps {
    stageName: string;
    domainStage: string;
    isProd: boolean;
    mongodbUriSecretName: string;
    mongoDBName: string;
    fileS3BucketName: string;
}

export class PipelineAppStage extends Stage {
    constructor(scope: Construct, id: string, props: DeploymentkProps) {
        super(scope, id, props);

        const lambdaStack = new LambdaStack(
            this,
            `${APP_NAME_TRANSCRIPT_ANALYZER}LambdaStack-${props.stageName}`,
            {
                env: props.env,
                stageName: props.stageName,
                domainStage: props.domainStage,
                isProd: props.isProd,
                mongodbUriSecretName: props.mongodbUriSecretName,
                mongoDBName: props.mongoDBName,
                fileS3BucketName: props.fileS3BucketName
            }
        );
    }
}
