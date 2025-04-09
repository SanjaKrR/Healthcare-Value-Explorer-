-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "PlanAttributes" (
    "PlanID" VARCHAR  NOT NULL,
    "StateCode" VARCHAR    NOT NULL,
    "IssuerID" VARCHAR    NOT NULL,
    "MarketCoverage" VARCHAR    NOT NULL,
    "DentalOnlyPlan" boolean   NOT NULL,
    "StandardComponentId" VARCHAR    NULL,
    "PlanMarketingName" VARCHAR    NOT NULL,
    "HIOSProductId" VARCHAR    NOT NULL,
    "NetworkId" VARCHAR    NOT NULL,
    "ServiceAreaId" VARCHAR    NOT NULL,
    "PlanType" VARCHAR    NOT NULL,
    "MetalLevel" VARCHAR    NOT NULL,
    "QHPNonQHPTypeId" VARCHAR    NOT NULL,
    "WellnessProgramOffered" VARCHAR    NOT NULL,
    "DiseaseManagementProgramsOffered" VARCHAR    NOT NULL,
    "EHBPercentTotalPremium" VARCHAR   NOT NULL,
    "OutOfServiceAreaCoverage" VARCHAR    NOT NULL,
    "OutOfServiceAreaCoverageDescription" VARCHAR    NOT NULL,
    "PlanVariantMarketingName" VARCHAR    NOT NULL,
    "CSRVariationType" VARCHAR    NOT NULL,
    "MedicalDrugDeductiblesIntegrated" VARCHAR    NOT NULL,
    "MedicalDrugMaximumOutofPocketIntegrated" VARCHAR    NOT NULL,
    "PlanBrochure" VARCHAR    NOT NULL,
    CONSTRAINT "pk_PlanAttributes" PRIMARY KEY (
        "PlanID"
     )
);
SELECT* FROM "PlanAttributes"

CREATE TABLE "BenefitsCostSharing" (
    "BCS_ID" VARCHAR    NOT NULL,
    "StateCode" VARCHAR    NOT NULL,
    "IssuerID" VARCHAR    NOT NULL,
    "StandardComonentId" VARCHAR    NOT NULL,
    "PlanID" VARCHAR    NOT NULL,
    "BenefitsID" VARCHAR    NOT NULL,
    "Exclusion" VARCHAR    NOT NULL,
    CONSTRAINT "pk_BenefitsCostSharing" PRIMARY KEY (
        "BCS_ID"
     )
);
SELECT* FROM "BenefitsCostSharing"

CREATE TABLE "Rates" (
    "RateID" int   NOT NULL,
    "StateCode" VARCHAR    NOT NULL,
    "IssuerID" int   NOT NULL,
    "PlanID" VARCHAR    NOT NULL,
    "IndividualRate" FLOAT   NOT NULL,
    CONSTRAINT "pk_Rates" PRIMARY KEY (
        "RateID"
     )
);
SELECT * FROM "Rates" 

CREATE TABLE "ServiceArea" (
    "ServiceAreaID" VARCHAR    NOT NULL,
    "ServiceArea" VARCHAR    NOT NULL,
    "StateCode" VARCHAR    NOT NULL,
    "IssuerId" VARCHAR    NOT NULL,
    "CoverEnteireState" boolean   NOT NULL,
    "County" VARCHAR    NOT NULL,
    "ZipCodes" VARCHAR    NOT NULL,
    "MarketCoverage" VARCHAR    NOT NULL,
    "DentalOnly" boolean   NOT NULL,
    CONSTRAINT "pk_ServiceArea" PRIMARY KEY (
        "ServiceAreaID"
     )
);

SELECT * FROM "ServiceArea" 

CREATE TABLE "Issuer" (
    "IssuerID" VARCHAR    NOT NULL,
    "IssuerMarketPlaceName" VARCHAR    NOT NULL,
    CONSTRAINT "pk_Issuer" PRIMARY KEY (
        "IssuerID"
     )
);

SELECT * FROM "Issuer" 

CREATE TABLE "Benefits" (
    "BenefitsID" VARCHAR    NOT NULL,
    "BenefitsName" VARCHAR    NOT NULL,
    CONSTRAINT "pk_Benefits" PRIMARY KEY (
        "BenefitsID"
     )
);

SELECT * FROM "Benefits" 

ALTER TABLE "PlanAttributes" ADD CONSTRAINT "fk_PlanAttributes_IssuerID" FOREIGN KEY("IssuerID")
REFERENCES "Issuer" ("IssuerID");

ALTER TABLE "PlanAttributes" ADD CONSTRAINT "fk_PlanAttributes_ServiceAreaId" FOREIGN KEY("ServiceAreaId")
REFERENCES "ServiceArea" ("ServiceAreaID");

ALTER TABLE "BenefitsCostSharing" ADD CONSTRAINT "fk_BenefitsCostSharing_IssuerID" FOREIGN KEY("IssuerID")
REFERENCES "Issuer" ("IssuerID");

ALTER TABLE "BenefitsCostSharing" ADD CONSTRAINT "fk_BenefitsCostSharing_PlanID" FOREIGN KEY("PlanID")
REFERENCES "PlanAttributes" ("PlanID");

ALTER TABLE "BenefitsCostSharing" ADD CONSTRAINT "fk_BenefitsCostSharing_BenefitsID" FOREIGN KEY("BenefitsID")
REFERENCES "Benefits" ("BenefitsID");

ALTER TABLE "Rates" ADD CONSTRAINT "fk_Rates_IssuerID" FOREIGN KEY("IssuerID")
REFERENCES "Issuer" ("IssuerID");

ALTER TABLE "Rates" ADD CONSTRAINT "fk_Rates_PlanID" FOREIGN KEY("PlanID")
REFERENCES "PlanAttributes" ("PlanID");

ALTER TABLE "ServiceArea" ADD CONSTRAINT "fk_ServiceArea_IssuerId" FOREIGN KEY("IssuerId")
REFERENCES "Issuer" ("IssuerID");

