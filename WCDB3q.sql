/* -----------------------------------------------------------------------
16. How many orgs are government based?
*/

SELECT COUNT(id)
	FROM (SELECT id
		FROM Organization
		WHERE (kind = "GMB") OR (kind = "GOV") OR (kind = "NG"));

/* -----------------------------------------------------------------------
17. What is the total number of casualties across the DB?
*/

SELECT SUM("number") AS TotalCasualties 
	FROM HumanImpacts
		WHERE (type = 'Death');
	
/* -----------------------------------------------------------------------
19. Create a list of telephone numbers, emails, and other contact info for all orgs
*/

SELECT telephone, fax, email, street_address, locality, region, postal_code, country
	FROM Organization;

/* -----------------------------------------------------------------------
22. How many hurricane crises (CrisisKind=HU)?
*/

SELECT COUNT(id)
	FROM Crisis
	WHERE (kind = "HU");

/* -----------------------------------------------------------------------
23. Name all humanitarian orgs in the DB
*/

SELECT Name 
	FROM Organizations
	WHERE (kind = 'HO');

/* -----------------------------------------------------------------------
24. Crisis listed based on occurence from earlier to latest
*/

SELECT *
	FROM Crisis
		ORDER BY start_date DESC, start_time DESC;

/* -----------------------------------------------------------------------
25. Name and kind of all people in the United States
*/

SELECT R.name, S.name
	FROM Person as R INNER JOIN PersonKind as S INNER JOIN Location
		ON (R.kind = S.id) AND (R.id = S.entity_id)
	WHERE (R.Country = "US" OR country = "USA" OR country = "United States");

/* -----------------------------------------------------------------------
26. Person with the longest name
*/

SELECT first_name, middle_name, last_name
	FROM
		(SELECT first_name, middle_name, last_name, SUM(A + B + C) AS length
			FROM
				(SELECT first_name, middle_name, last_name, CHAR_LENGTH(first_name) AS A, CHAR_LENGTH(middle_name) AS B, CHAR_LENGTH(last_name) AS C))
	WHERE (length = MAX(length));

/* -----------------------------------------------------------------------
27. Crisis type with only one example
*/

SELECT kind
	FROM
		(SELECT kind, COUNT(name) as "number"
			FROM Crisis INNER JOIN CrisisKind
				ON (Crisis.kind = CrisisKind.id)
					GROUP BY kind)
	WHERE ("number" = 1);

/* -----------------------------------------------------------------------
28. People that don't have a middle name
*/

SELECT name
	FROM Person
	WHERE (middle_name IS NULL);

/* -----------------------------------------------------------------------
29. Names that start with "B"
*/

SELECT first_name
	FROM Person
	WHERE (LEFT(name, 1) = "B" or LEFT(name, 1) = "b");

/* -----------------------------------------------------------------------
30. People associated with each country
*/

SELECT first_name, middle_name, last_name
	FROM Person INNER JOIN Location
		ON Person.id = Location.entity_id
			GROUP BY country;

/* -----------------------------------------------------------------------
31. Crisis affecting the most countries
*/

SELECT name
	FROM
		(SELECT name, COUNT(country) AS "number"
			FROM Crisis INNER JOIN Location
				ON Crisis.id = Location.entity_id
					GROUP BY name);
	WHERE ("number" = MAX("number"));

/* -----------------------------------------------------------------------
32. Earliest crisis
*/

SELECT FIRST(name)
	FROM Crisis
		ORDER BY start_date DESC, start_time DESC;
	
/* -----------------------------------------------------------------------
33. Number of organizations in the US
*/

SELECT COUNT(DISTINCT Organization.id)
	FROM Organization INNER JOIN Location
		ON Organization.id = Location.entity_id
			WHERE (country = "US" OR country = "USA" OR country = "United States");

/* -----------------------------------------------------------------------
34. Number of Singers
*/

SELECT COUNT(id)
	FROM Person
		WHERE (kind = "SNG");

/* -----------------------------------------------------------------------
35. Number of current and former leaders
*/

SELECT COUNT(id)
	FROM Person
		WHERE (kind = "LD");

/* -----------------------------------------------------------------------
36. Hurricane Start Dates
*/

select start_date from Crisis
	where (kind = "HU");

/* -----------------------------------------------------------------------
37. Number of natural disasters between June 5th 2000 and June 5th 2012
*/

select count(*) from Crisis inner join CrisisKind on (Crisis.kind = CrisisKind.id)
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

select country, count(id) from Person inner join Location
	on Person.id = Location.entity_id
	where id in
		(select id from PersonKind
			where name = 'DI'
			   or name = 'FRC'
			   or name = 'GO'
			   or name = 'GOV'
			   or name = 'PO'
			   or name = 'PR'
			   or name = 'PM'
			   or name = 'SA'
			   or name = 'VP'
			   or name = 'AMB')
	group by country;

/* -----------------------------------------------------------------------
39. Location with the highest number of natural disasters
*/

select region from
	(select region, count(id) from Location
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
				or name = 'FL')
				group by region)
	where total = max(count(id));

/* -----------------------------------------------------------------------
40. Average number of deaths in hurricanes
*/

select avg(number) from HumanImpact inner join Crisis
	on HumanImpact.crisis_id = Crisis.id
	where (kind = "HU") and (type = "Death");

/* -----------------------------------------------------------------------
41. Total number of deaths caused by terrorist attacks
*/

select sum(number) from HumanImpact inner join Crisis
	on HumanImpact.crisis_id = Crisis.id
	where (type = 'Death') and (kind = "TA");

/* -----------------------------------------------------------------------
42. List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with--
*/

select name from Crisis where id in
	(select Crisis.id 
		from inner join CrisisKind on Crisis.kind = CrisisKind.id 
		inner join PersonCrisis on Crisis.id = PersonCrisis.id_crisis
		where kind = "HU" and id_person = "WStickney");

/* -----------------------------------------------------------------------
43. List of hurricanes in the US where FEMA was NOT involved
*/

select name from Crisis
	where id not in
		(select id from Crisis inner join CrisisOrganization on Crisis.id = CrisisOrganization.id_crisis as id inner join Location on Crisis.id = Location.entity_id
			where id_organization = "FEMA" and not (country = "US" or country = "USA" or country = "United States");

/* -----------------------------------------------------------------------
44. Number of crises that intelligence agencies were involved in
*/

select count(*) from CrisisOrganization
	where id_organization in
		(select id as id_organization from OrganizationKind
		where name = 'IA');

/* -----------------------------------------------------------------------
45. How many more orgs does America have than Britain
*/

select count(distinct AMR) - count(distinct BRT)
	from
	(select id as AMR from Organization inner join Location on Organization.id = Location.entity_id where country = 'US'),
	(select id as BRT from Organization inner join Location on Organization.id = Location.entity_id where country = 'GB');