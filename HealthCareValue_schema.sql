-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "PlanAttributes" (
    "PlanID" string   NOT NULL,
    "StateCode" string   NOT NULL,
    "IssuerID" string   NOT NULL,
    "MarketCoverage" string   NOT NULL,
    "DentalOnlyPlan" boolean   NOT NULL,
    "StandardComponentId" string   NULL,
    "PlanMarketingName" string   NOT NULL,
    "HIOSProductId" string   NOT NULL,
    "NetworkId" string   NOT NULL,
    "ServiceAreaId" string   NOT NULL,
    "PlanType" string   NOT NULL,
    "MetalLevel" string   NOT NULL,
    "QHPNonQHPTypeId" string   NOT NULL,
    "WellnessProgramOffered" string   NOT NULL,
    "DiseaseManagementProgramsOffered" string   NOT NULL,
    "EHBPercentTotalPremium" string   NOT NULL,
    "OutOfServiceAreaCoverage" string   NOT NULL,
    "OutOfServiceAreaCoverageDescription" string   NOT NULL,
    "PlanVariantMarketingName" string   NOT NULL,
    "CSRVariationType" string   NOT NULL,
    "MedicalDrugDeductiblesIntegrated" string   NOT NULL,
    "MedicalDrugMaximumOutofPocketIntegrated" string   NOT NULL,
    "PlanBrochure" string   NOT NULL,
    CONSTRAINT "pk_PlanAttributes" PRIMARY KEY (
        "PlanID"
     )
);

CREATE TABLE "BenefitsCostSharing" (
    "BCS_ID" string   NOT NULL,
    "StateCode" string   NOT NULL,
    "IssuerID" string   NOT NULL,
    "StandardComonentId" string   NOT NULL,
    "PlanID" string   NOT NULL,
    "BenefitsID" string   NOT NULL,
    "Exclusion" string   NOT NULL,
    CONSTRAINT "pk_BenefitsCostSharing" PRIMARY KEY (
        "BCS_ID"
     )
);

CREATE TABLE "Rates" (
    "RateID" int   NOT NULL,
    "StateCode" string   NOT NULL,
    "IssuerID" int   NOT NULL,
    "PlanID" string   NOT NULL,
    "IndividualRate" double   NOT NULL,
    CONSTRAINT "pk_Rates" PRIMARY KEY (
        "RateID"
     )
);

CREATE TABLE "ServiceArea" (
    "ServiceAreaID" string   NOT NULL,
    "ServiceArea" string   NOT NULL,
    "StateCode" string   NOT NULL,
    "IssuerId" string   NOT NULL,
    "CoverEnteireState" boolean   NOT NULL,
    "County" string   NOT NULL,
    "ZipCodes" string   NOT NULL,
    "MarketCoverage" string   NOT NULL,
    "DentalOnly" boolean   NOT NULL,
    CONSTRAINT "pk_ServiceArea" PRIMARY KEY (
        "ServiceAreaID"
     )
);

CREATE TABLE "Issuer" (
    "IssuerID" string   NOT NULL,
    "IssuerMarketPlaceName" string   NOT NULL,
    CONSTRAINT "pk_Issuer" PRIMARY KEY (
        "IssuerID"
     )
);

CREATE TABLE "Benefits" (
    "BenefitsID" string   NOT NULL,
    "BenefitsName" string   NOT NULL,
    CONSTRAINT "pk_Benefits" PRIMARY KEY (
        "BenefitsID"
     )
);

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

