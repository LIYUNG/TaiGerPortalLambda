import { AWS_ACCOUNT } from "../configuration";
import { Region } from "./regions";

export enum Stage {
    Beta_FE = "Beta-FE",
    Prod_NA = "Prod-NA"
}

export enum DomainStage {
    Beta = "beta",
    Prod = "prod"
}

export const STAGES = [
    {
        stageName: Stage.Beta_FE,
        env: { region: Region.IAD, account: AWS_ACCOUNT },
        isProd: false,
        domainStage: DomainStage.Beta,
        mongodbUriSecretName: "beta/taigerportal/mongodb",
        mongoDBName: "TaiGer",
        fileS3BucketName: "taiger-file-storage"
    },
    {
        stageName: Stage.Prod_NA,
        env: { region: Region.NRT, account: AWS_ACCOUNT },
        isProd: true,
        domainStage: DomainStage.Prod,
        mongodbUriSecretName: "prod/taigerportal/mongodb",
        mongoDBName: "TaiGer_Prod",
        fileS3BucketName: "taiger-file-storage-production-storage"
    }
];
