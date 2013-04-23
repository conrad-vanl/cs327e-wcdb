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
		FROM Person as R INNER JOIN PersonKind as S
			ON R.kind = S.id
			INNER JOIN Location
			ON R.id = S.entity_id
				WHERE (R.Country = "US" OR country = "USA" OR country = "United States");

/* -----------------------------------------------------------------------
26. Person with the longest name
*/

SELECT first_name, middle_name, last_name
		FROM
			(SELECT first_name, middle_name, last_name, SUM(A, B, C) AS length
				FROM
					(SELECT first_name, middle_name, last_name, CHAR_LENGTH(first_name) AS A, CHAR_LENGTH(middle_name) AS B, CHAR_LENGTH(last_name) AS C))
		WHERE (length = MAX(length));

/* -----------------------------------------------------------------------
27. Crisis type with only one example
*/

SELECT kind
		FROM
			(SELECT kind, COUNT(name)
				FROM Crisis INNER JOIN CrisisKind
					ON Crisis.kind = CrisisKind.id
						GROUP BY kind)
			WHERE (COUNT(name) = 1);

/* -----------------------------------------------------------------------
28. People that don't have a middle name
*/

SELECT name
		FROM Person
			WHERE (middle_name IS NULL);

/* -----------------------------------------------------------------------
29. Names that start with "B"
*/

SELECT name
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
			(SELECT name, COUNT(country)
				FROM Crisis INNER JOIN Location
					ON Crisis.id = Location.entity_id
						GROUP BY name);
		WHERE (COUNT(country) = MAX(COUNT(country)));

/* -----------------------------------------------------------------------
32. Earliest crisis
*/

SELECT name
		FROM Crisis
			ORDER BY start_date DESC, start_time DESC
				WHERE (start_date > start_date AND start_time > start_time);

/* -----------------------------------------------------------------------
33. Number of organizations in the US
*/

SELECT COUNT(DISTINCT id)
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