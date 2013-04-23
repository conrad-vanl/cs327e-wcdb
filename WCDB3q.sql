

/* -----------------------------------------------------------------------
36. Hurricane Start Dates
*/

select start_date from Crisis
	where id in
		(select id from CrisisKind
			where name = 'HU');

/* -----------------------------------------------------------------------
37. Number of natural disasters between June 5th 2000 and June 5th 2012
*/

select count(*) from Crisis
	where start_date >= 2000-06-05
	  and end_date   <= 2012-06-05
	  and id in
		(select id from CrisisKind
			where name = 'EQ'
			   or name = 'FR'
			   or name = 'HU'
			   or name = 'ME'
			   or name = 'ST'
			   or name = 'TO'
			   or name = 'TS'
			   or name = 'VO'
			   or name = 'FL');

/* -----------------------------------------------------------------------
38. Number of political figures by country
*/

select country, count(id) from Person natural join Location
	where id in
		(select id from PersonKind
			where name = 'DI'
			   or name = 'ERC'
			   or name = 'GO'
			   or name = 'GOV'
			   or name = 'HO'
			   or name = 'LD'
			   or name = 'PO'
			   or name = 'PR'
			   or name = 'PM'
			   or name = 'SA'
			   or name = 'VP'
			   or name = 'AMB')
	order by count(id);

/* -----------------------------------------------------------------------
39. Location with the highest number of natural disasters
*/

select region, count(id) from Location
	where id in 
		(select id from CrisisKind
			where name = 'EQ'
			   or name = 'FR'
			   or name = 'HU'
			   or name = 'ME'
			   or name = 'ST'
			   or name = 'TO'
			   or name = 'TS'
			   or name = 'VO'
			   or name = 'FL');

/* -----------------------------------------------------------------------
40. Average number of deaths in hurricanes
*/
select avg(number) from HumanImpact
	where id in
		(select id from CrisisKind
			where name = 'HU');

/* -----------------------------------------------------------------------
41. Total number of deaths caused by terrorist attacks
*/

select sum(number) from HumanImpact
	where type = 'Death'
	  and id in
		(select id from CrisisKind
			where name = 'TA');

/* -----------------------------------------------------------------------
42. List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with--
*/

select name from Crisis
	where id in
		(select id from CrisisKind
			where name = 'HU') as R
		natural join
		(select id_crisis id from PersonCrisis
			where id_person = 'WStickney') as S; 

/* -----------------------------------------------------------------------
43. List of hurricanes in the US where FEMA was NOT involved--
*/

select name from Crisis
	where id in
		(select id from CrisisKind
			where name = 'HU') as R
		natural join
		(select id_crisis as id from PersonCrisis
			where id_person != 'FEMA') as S
		natural join
		(select id from Location
			where country = 'US') as T;

/* ----------------------------------------------------------------------- 
44. Number of crises that intelligence agencies were involved in--
*/

select count(*) from CrisisOrganization
	where id_organization in
		(select id as id_organizaiton from OrganizationKind
			where name = 'IA');

/* -----------------------------------------------------------------------
45. How many more orgs does America have than Britain
*/