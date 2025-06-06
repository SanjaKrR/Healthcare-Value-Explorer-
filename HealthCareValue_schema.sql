﻿-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "PlanAttributes" (
    "PlanID" VARCHAR  NOT NULL,
    "StateCode" VARCHAR,
    "IssuerID" VARCHAR    NOT NULL,
    "MarketCoverage" VARCHAR,
    "DentalOnlyPlan" boolean,
    "StandardComponentId" VARCHAR,
    "PlanMarketingName" VARCHAR,
    "HIOSProductId" VARCHAR,
    "NetworkId" VARCHAR,
    "ServiceAreaId" VARCHAR    NOT NULL,
    "PlanType" VARCHAR,
    "MetalLevel" VARCHAR,
    "QHPNonQHPTypeId" VARCHAR,
    "WellnessProgramOffered" VARCHAR,
    "DiseaseManagementProgramsOffered" VARCHAR,
    "EHBPercentTotalPremium" VARCHAR,
    "OutOfServiceAreaCoverage" VARCHAR,
    "OutOfServiceAreaCoverageDescription" VARCHAR,
    "PlanVariantMarketingName" VARCHAR,
    "CSRVariationType" VARCHAR,
    "MedicalDrugDeductiblesIntegrated" VARCHAR,
    "MedicalDrugMaximumOutofPocketIntegrated" VARCHAR,
    "PlanBrochure" VARCHAR,
    CONSTRAINT "pk_PlanAttributes" PRIMARY KEY (
        "PlanID"
     )
);
SELECT* FROM "PlanAttributes"

CREATE TABLE "BenefitsCostSharing" (
    "BCS_ID" VARCHAR    NOT NULL,
    "StateCode" VARCHAR,
    "IssuerID" VARCHAR NOT NULL,
    "StandardComponentId" VARCHAR,
    "PlanID" VARCHAR    NOT NULL,
    "BenefitsID" VARCHAR    NOT NULL,
    "Exclusion" VARCHAR,
    CONSTRAINT "pk_BenefitsCostSharing" PRIMARY KEY (
        "BCS_ID"
     )
);
SELECT* FROM "BenefitsCostSharing"

CREATE TABLE "Rates" (
    "RateID" int   NOT NULL,
    "StateCode" VARCHAR,
    "IssuerID" VARCHAR   NOT NULL,
    "PlanID" VARCHAR    NOT NULL,
    "IndividualRate" FLOAT,
    CONSTRAINT "pk_Rates" PRIMARY KEY (
        "RateID"
     )
);
SELECT * FROM "Rates" 

CREATE TABLE "ServiceArea" (
    "ServiceAreaID" VARCHAR    NOT NULL,
    "ServiceArea" VARCHAR,
    "StateCode" VARCHAR,
    "IssuerId" VARCHAR    NOT NULL,
    "CoverEntireState" boolean,
    "County" VARCHAR,
    "ZipCodes" VARCHAR,
    "MarketCoverage" VARCHAR,
    "DentalOnly" boolean,
    CONSTRAINT "pk_ServiceArea" PRIMARY KEY (
        "ServiceAreaID"
     )
);

SELECT * FROM "ServiceArea" 

CREATE TABLE "Issuer" (
    "IssuerID" VARCHAR  NOT NULL,
    "IssuerMarketPlaceName" VARCHAR,
    CONSTRAINT "pk_Issuer" PRIMARY KEY (
        "IssuerID"
     )
);

SELECT * FROM "Issuer" 

CREATE TABLE "Benefits" (
    "BenefitsID" VARCHAR    NOT NULL,
    "BenefitsName" VARCHAR,
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

