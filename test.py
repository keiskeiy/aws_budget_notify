import pandas as pd

data = {
    "環境変数名": [
        "IMAGE_URL", "CODE_DEPLOY_APPLICATION_NAME", "CODE_DEPLOY_DEPLOY_GROUP_NAME", "CONTAINER_NAME", "APP_ENVIRONMENT",
        "APP_FRONT_URL", "APP_SAML_SETTINGS_SP_CALLBACK_URL", "APP_VAAQS_URL", "APP_VAAQS_PATH_SIMULATION_MESHCODE",
        "APP_VAAQS_RATE_LIMIT", "APP_LAPLACE_URL", "APP_LAPLACE_SECTORS", "APP_LAPLACE_FAILURES", "APP_LAPLACE_ACTIVE_FAILURES",
        "APP_LAPLACE_WORK_PLANS", "APP_LAPLACE_EFFECT_WORK_PLANS", "APP_LAPLACE_RATE_LIMIT", "APP_DATABASE_URL"
    ],
    "dev": [
        "767397924690.dkr.ecr.ap-northeast-1.amazonaws.com/se-portal-dev-ecr-api:{0}",
        "AppECS-se-portal-dev-ecs-cluster-se-portal-dev-ecs-service-api",
        "DgpECS-se-portal-dev-ecs-cluster-se-portal-dev-ecs-service-api",
        "se-portal-dev-api-container", "development", "https://dev.se-iot-portal.kddi.com",
        "https://dev.se-iot-portal.kddi.com/saml/acs", "https://dev-mock.se-iot-portal.kddi.com",
        "/apis/v1/vaaqs3/area-simulation/meshcode25m/{mesh_code}", "100", "https://dev-mock.se-iot-portal.kddi.com",
        "/apis/v1/laplace/base_stations/{bts_id}/sectors", "/apis/v1/laplace/ords/iottest/case1/kisys/service/{bts_name}",
        "/apis/v1/laplace/ords/iottest/case2/kisys", "/apis/v1/laplace/ords/iottest/case1/autkr/building_names/{bts_name}",
        "/apis/v1/laplace/ords/iottest/case2/autkr", "100",
        "postgresql://kddi:${{ secrets.AWS_DB_PASS_KEY }}@se-portal-dev-postgre-database.cdyk2uce0tnd.ap-northeast-1.rds.amazonaws.com:5432/se-portal"
    ],
    "stg": [
        "390403889572.dkr.ecr.ap-northeast-1.amazonaws.com/se-portal-dev-ecr-api:{0}",
        "AppECS-se-portal-stg-ecs-cluster-se-portal-stg-ecs-service-api",
        "DgpECS-se-portal-stg-ecs-cluster-se-portal-stg-ecs-service-api",
        "se-portal-stg-api-container", "staging", "https://stg.se-iot-portal.kddi.com",
        "https://stg.se-iot-portal.kddi.com/saml/acs", "http://10.23.28.163",
        "/vaaqs_test1/api/v1/area-simulation/meshcode25m/{mesh_code}", "5", "http://se-portal-stg-laplace-proxy-nlb-2dd00234114cc5d6.elb.ap-northeast-1.amazonaws.com",
        "/apis/v1/laplace/base_stations/{bts_id}/sectors", "/ords/iottest/case1/kisys/service/{bts_name}",
        "/ords/iottest/case2/kisys", "/ords/iottest/case1/autkr/building_names/{bts_name}",
        "/ords/iottest/case2/autkr", "10",
        "postgresql://kddi:${{ secrets.AWS_DB_PASS_KEY }}@se-portal-stg-postgre-database.cf84cg6kw0q7.ap-northeast-1.rds.amazonaws.com:5432/se-portal"
    ],
    "prd": [
        "982534378582.dkr.ecr.ap-northeast-1.amazonaws.com/se-portal-dev-ecr-api:{0}",
        "AppECS-se-portal-prd-ecs-cluster-se-portal-prd-ecs-service-api",
        "DgpECS-se-portal-prd-ecs-cluster-se-portal-prd-ecs-service-api",
        "se-portal-prd-api-container", "production", "https://se-iot-portal.kddi.com",
        "https://se-iot-portal.kddi.com/saml/acs", "http://10.23.28.162",
        "/vaaqs/api/v1/area-simulation/meshcode25m/{mesh_code}", "5", "http://se-portal-prd-laplace-proxy-nlb-61864e391a81723f.elb.ap-northeast-1.amazonaws.com",
        "/apis/v1/laplace/base_stations/{bts_id}/sectors", "/ords/ords_api01/case1/kisys/service/{bts_name}",
        "/ords/ords_api01/case2/kisys", "/ords/ords_api01/case1/autkr/building_names/{bts_name}",
        "/ords/ords_api01/case2/autkr", "10",
        "postgresql://kddi:${{ secrets.AWS_DB_PASS_KEY }}@se-portal-prd-postgre-database.chks2km4icjh.ap-northeast-1.rds.amazonaws.com:5432/se-portal"
    ]
}

df = pd.DataFrame(data)
df.to_excel("environment_variables.xlsx", index=False)