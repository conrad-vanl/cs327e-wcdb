| Crises                                              |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | crisis_id       | required, index     |
| str()       | crisisKind_id   |                     |
| str(255)    | name            | required            |
| datetime()  | startDateTime   | required            |
| datetime()  | endDatetime     |                     |
| str         | economicImpact  |                     |

| RelatedPeople                                       |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | person_id       | required            |
| str()       | crisis_id       |                     |
| str()       | organization_id |                     |

| RelatedOrganizations                                |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | organization_id | required            |
| str()       | person_id       |                     |
| str()       | crisis_id       |                     |

| RelatedCrisis                                       |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | organization_id |                     |
| str()       | person_id       |                     |
| str()       | crisis_id       | required            |

| Locations                                           |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | crisis_id       |                     |
| str()       | person_id       |                     |
| str()       | organization_id |                     |
| str()       | locality        |                     |
| str()       | region          |                     |
| str()       | country         |                     |

| ExternalResources                                   |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | crisis_id       |                     |
| str()       | organization_id |                     |
| enum("ImageURL","VideoURL","MapURL","SocialNetworkURL","Citation","ExternalLinkUrl") | type | |
| text()      | content         |                     |

| HumanImpacts                                        |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| string      | crisis_id       |                     |
| str(255)    | type            |                     |
| int         | number          |                     |

| ResourcesNeeded                                     |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| string      | crisis_id       |                     |
| text        | resource        |                     |

| WaysToHelp                                          |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| string      | crisis_id       |                     |
| text        | waysToHelp      |                     |

| Organizations                                       |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | organization_id | required, index     |
| str()       | organizationKind_id |                 |
| str(255)    | name            | required            |
| text()      | history         |                     |
| str()       | contactInfoTelephone |                | 
| str()       | contactInfoFax |                      |
| str()       | contactInfoEmail |                    |
| str()       | contactInfoPostalAddressStreetAddress | |
| str()       | contactInfoPostalAddressLocality      | |
| str()       | contactInfoPostalAddressRegion        | |
| str()       | contactInfoPostalAddressPostalCode    | |
| str()       | contactInfoPostalAddressCountry       | |

| OrganizationKinds                                   |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | organizationKind_id |                 |
| str()       | name            |                     |
| text()      | description     |                     |

| CrisisKinds                                         |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | crisisKind_id   |                     |
| str()       | name            |                     |
| text()      | description     |                     |

| PersonKinds                                         |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | personKind_id   |                     |
| str()       | name            |                     |
| text()      | description     |                     |

| People                                              |
| --------------------------------------------------- |
| Type        | Name            | Attributes          |
| ------------|-----------------|---------------------|
| str()       | person_id       |                     |
| str()       | firstName       |                     |
| str()       | lastName        |                     |
| str()       | middleName      |                     |
| str()       | suffix          |                     |
| str()       | personKind_id   |                     |