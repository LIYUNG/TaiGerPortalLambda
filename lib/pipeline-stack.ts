import * as cdk from "aws-cdk-lib";
import { Stack, StackProps, SecretValue, Duration, RemovalPolicy } from "aws-cdk-lib";
import {
    CodeBuildStep,
    CodePipeline,
    CodePipelineSource,
    ManualApprovalStep,
    ShellStep
} from "aws-cdk-lib/pipelines";
import * as codepipeline_actions from "aws-cdk-lib/aws-codepipeline-actions";
import { Construct } from "constructs";
import {
    GITHUB_OWNER,
    GITHUB_PACKAGE_BRANCH,
    GITHUB_REPO,
    GITHUB_TOKEN
} from "../configuration/dependencies";
import { PipelineAppStage } from "./app-stage";
import { Region, STAGES } from "../constants";
import { PolicyStatement } from "aws-cdk-lib/aws-iam";
import { BlockPublicAccess, Bucket, BucketEncryption } from "aws-cdk-lib/aws-s3";

export class PipelineStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        // Define the source for the pipeline
        const source = CodePipelineSource.gitHub(
            `${GITHUB_OWNER}/${GITHUB_REPO}`,
            GITHUB_PACKAGE_BRANCH,
            {
                authentication: SecretValue.secretsManager(GITHUB_TOKEN),
                trigger: codepipeline_actions.GitHubTrigger.WEBHOOK
            }
        );

        // Create the high-level CodePipeline
        const pipeline = new CodePipeline(this, "Pipeline", {
            pipelineName: "TaiGerPortalTranscriptAnalyzerPipeline",
            artifactBucket: new Bucket(this, `${GITHUB_REPO}-ArtifactBucket`, {
                bucketName: `${GITHUB_REPO}-pipeline-artifact-bucket`.toLowerCase(),
                removalPolicy: RemovalPolicy.DESTROY,
                autoDeleteObjects: true,
                versioned: false,
                encryption: BucketEncryption.S3_MANAGED,
                blockPublicAccess: BlockPublicAccess.BLOCK_ALL,
                enforceSSL: true,
                lifecycleRules: [
                    {
                        expiration: Duration.days(30)
                    }
                ]
            }),
            synth: new ShellStep("Synth", {
                input: source,
                commands: ["npm ci", "npm run build", "npx cdk synth"]
            }),
            // role: adminRole,
            codeBuildDefaults: {
                rolePolicy: [
                    new PolicyStatement({
                        actions: [
                            "route53:ListHostedZonesByName",
                            "route53:GetHostedZone",
                            "route53:ListHostedZones"
                        ],
                        resources: ["*"]
                    })
                ]
            }
        });

        STAGES.forEach(
            ({
                stageName,
                env,
                domainStage,
                isProd,
                mongodbUriSecretName,
                mongoDBName,
                fileS3BucketName
            }) => {
                const stage = new PipelineAppStage(
                    this,
                    `${stageName}-TaiGerPortalTranscriptAnalyzerLambda`,
                    {
                        env,
                        stageName,
                        domainStage,
                        isProd,
                        mongodbUriSecretName,
                        mongoDBName,
                        fileS3BucketName
                    }
                );
                if (isProd) {
                    pipeline.addStage(stage, {
                        pre: [new ManualApprovalStep("ApproveIfStable")]
                    });
                } else {
                    pipeline.addStage(stage);
                }
            }
        );
    }
}
