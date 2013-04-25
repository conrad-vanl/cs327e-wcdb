
/* -----------------------------------------------------------------------
1. Which people are associated with more than one crisis? 
*/

Select last_name, first_name, middle_name 
	From
		Person inner join PersonCrisis
		on Person.id = PersonCrisis.person_id
		Group by last_name
		having count(*) > 1;

/* -----------------------------------------------------------------------
2. For the past 5 decades, which countries had the most world crises per decade? 
*/

Create temporary table T as
	Select country
	From Crisis join Location on
	Location.entity_id = Crisis.id
	Where Location.entity_type = C;

Select country
	From( 
	Select country, max(count(*))	
	From T
	Where start_date > 1999-12-31 and start_date < 2010-01-01)
	Group by country;

Select country
	From( 
	Select country, max(*)	
	From T
	Where start_date > 1989-12-31 and start_date < 2000-01-01)
	Group by country;

Select country
	From( 
	Select country, max(*)	
	From T
	Where start_date > 1979-12-31 and start_date < 1990-01-01)
	Group by country;

Select country
	From( 
	Select country, max(*)	
	From T
	Where start_date > 1969-12-31 and start_date < 1980-01-01)
	Group by country;

Select country
	From( 
	Select country, max(*)	
	From T
	Where start_date > 1959-12-31 and start_date < 1970-01-01)
	Group by country;

/* -----------------------------------------------------------------------
3. What is the average death toll of accident crises?
*/

Select avg(number)
	From
	Crisis inner join HumanImpact
	on (Crisis.id = HumanImpact.crisis_id)
	Where (type = "Death") and (CrisisKind = "ACC");

/* -----------------------------------------------------------------------
4. What is the average death toll of world crises per country?
*/

Select country, avg(number)
	From Location join HumanImpact
	on Location.entity_id = HumanImpact.crisis_id
	Where type = "Death"
	Group by country;

/* -----------------------------------------------------------------------
5. What is the most common resource needed?
*/

SELECT description, COUNT(description) AS descriptioncount
	FROM ResourceNeeded
	GROUP BY description
	HAVING COUNT(description) = (SELECT COUNT(description)
					FROM ResourceNeeded
					GROUP BY description
					ORDER BY COUNT(description) DESC
					LIMIT 1);

/* -----------------------------------------------------------------------
6. How many people are related to crises located in countries other than their own?
*/

Select count(*)
	From
		((Crisis join Location on Crisis.id = Location.entity_id as C)
		join PersonCrisis on C.id = PersonCrisis.crisis_id as D)
		natural join
		((Person join Location on Person.id = Location.entity_id as E)
		join (PersonCrisis on E.id = PersonCrisis.crisis_id as F)) As M
	Where ***Incomplete***



/* -----------------------------------------------------------------------
7. How many crises occurred during the 1960's?
*/

Select count(name)
	From Crisis
	Where (start_date > 1959-12-31) and (start_date < 1970-01-01);

/* -----------------------------------------------------------------------
8. Which orgs are located outside the US and were involved in more than 1 crisis?
*/

SELECT name
	FROM Organization
	WHERE (country != "US") and (country != "United States") and id in

		SELECT Organization_id
		FROM CrisisOrganization
		GROUP BY Organization_id
		Having count(*) >  1

/* -----------------------------------------------------------------------
9. Organizations, Crises and People with the same location
*/

Select A.name, B.name, C.name
	From (Crisis join Location on Crisis.id = Location.entity_id where Location.entity_type = "C" as A)
	Join (Organization join Location on Organization.id = Location.entity_id where Location.entity_type = "O" as B)
	Join (Person join Location on Person.id = Location.entity_id where Location.entity_type = "P" as C)
	Where A.location = B.location = C.location

/* -----------------------------------------------------------------------
10. Crisis with minimum human impact
*/

Select name
	From Crisis join HumanImpact on Crisis.id = HumanImpact.crisis_id
	Having min(number);

/* -----------------------------------------------------------------------
11. Number of Crisis each Organization helped
*/

Select name, count(*)
	From Organization join CrisisOrganization
	on Organization.id = CrisisOrganization.organization_id
	Group by name;

/* -----------------------------------------------------------------------
12. Name and postal address of all organizations in California
*/

Select name, street_address, locality, region, postal_code, country
	From Organization
	Where region = "California";

/* -----------------------------------------------------------------------
13. List all crises that happened in the same state/region
*/

SELECT Name
	FROM Crisis INNER JOIN Location
		ON Location.entity_id = Crisis.id
			GROUP BY region;

/* -----------------------------------------------------------------------
14. Find the total number of human casualties caused by crises in the 1990s
*/

SELECT SUM("number") AS TotalCasualties 
	FROM HumanImpact INNER JOIN Crisis
		ON HumanImpact.crisis_id = Crisis.id
		WHERE (start_date >= 1989-12-31)
		AND (start_date <= 2000-1-1)
		AND (HumanImpact.type = "Death");

/* -----------------------------------------------------------------------

15. Find the organization(s) that has provided support on the most Crises
*/
SELECT Organization.name
	FROM (SELECT Organization.name, COUNT(CrisisOrganization.crisis_id) as "number"
		FROM Organization INNER JOIN CrisisOrganization
			ON Organization.id = CrisisOrganization.organization_id
				GROUP BY Organization.name)
		WHERE ("number" = MAX("number"));

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
		WHERE (type = "Death");
	
/* -----------------------------------------------------------------------
18. What is the most common type/kind of crisis occuring in the DB?
*/
select top 1 kindName 
FROM (SELECT CK.name as kindName, COUNT(C.kind)
FROM CrisisKind AS CK INNER JOIN Crisis AS C
	ON CK.id = C.kind
group by kindName)
order by count(*) desc ;
/* -----------------------------------------------------------------------
19. Create a list of telephone numbers, emails, and other contact info for all orgs
*/

SELECT telephone, fax, email, street_address, locality, region, postal_code, country
	FROM Organization;

/* -----------------------------------------------------------------------
20. What is the longest-lasting crisis? (if no end date, then ignore)
*/
SELECT MAX(DATEDIFF(day, endDateTime, startDateTime) as diffDate
	FROM Crises;

/* -----------------------------------------------------------------------
21. Which person(s) is involved or associated with the most organizations?
*/
SELECT first_name, middle_name, last_name 
	FROM (SELECT Person.first_name, Person.middle_name, Person.last_name, COUNT(OrganizationPerson.organization_id)
		FROM Person INNER JOIN OrganizationPerson
			ON Person.id = OrganizationPerson.person_id
				GROUP BY last_name);
		WHERE (COUNT(organization_id) = MAX(COUNT(organization_id)));

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
	WHERE (kind = "HO");

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
		ORDER BY start_date ASC, start_time ASC;
	
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

select count(*) from Crisis
	where (start_date >= 2000-06-05)
	  and (end_date   <= 2012-06-05)
	  and kind in
		(select id from CrisisKind
			where id = 'EQ'
			   or id = 'FR'
			   or id = 'HU'
			   or id = 'ME'
			   or id = 'ST'
			   or id = 'TO'
			   or id = 'TS'
			   or id = 'VO'
			   or id = 'FL');

/* -----------------------------------------------------------------------
38. Number of political figures by country
*/

select country, count(id) from Person inner join Location
	on Person.id = Location.entity_id
	where kind in
		(select id from PersonKind
			where id = 'DI'
			   or id = 'FRC'
			   or id = 'GO'
			   or id = 'GOV'
			   or id = 'PO'
			   or id = 'PR'
			   or id = 'PM'
			   or id = 'SA'
			   or id = 'VP'
			   or id = 'AMB')
	group by country;

/* -----------------------------------------------------------------------
39. Location with the highest number of natural disasters
*/

select country, total from
	(select country, count(R.id) as total
		from
			(select country, R.id from CrisisKind as S inner join Crisis as R inner join Location on (S.id = R.kind) and (R.id = Location.entity_id)
				where (S.id = 'EQ')
				or (S.id = 'FR')
				or (S.id = 'HU')
				or (S.id = 'ME')
				or (S.id = 'ST')
				or (S.id = 'TO')
				or (S.id = 'TS')
				or (S.id = 'VO')
				or (S.id = 'FL')
				group by country)
		order by total DESC)
	where total = max(total);

/* -----------------------------------------------------------------------
40. Average number of deaths in hurricanes
*/

select avg("number") from HumanImpact inner join Crisis
	on HumanImpact.crisis_id = Crisis.id
	where (kind = "HU") and (type = "Death");

/* -----------------------------------------------------------------------
41. Total number of deaths caused by terrorist attacks
*/

select sum("number") from HumanImpact inner join Crisis
	on HumanImpact.crisis_id = Crisis.id
	where (type = "Death") and (kind = "TA");

/* -----------------------------------------------------------------------
42. List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with--
*/

select name from Crisis where id in
	(select Crisis.id 
		from inner join CrisisKind on Crisis.kind = CrisisKind.id 
		inner join PersonCrisis on Crisis.id = PersonCrisis.id_crisis
		where kind = "HU" and person_id = "WStickney");

/* -----------------------------------------------------------------------
43. List of hurricanes in the US where FEMA was NOT involved
*/

select name from Crisis
	where id not in
		(select id from Crisis inner join CrisisOrganization on Crisis.id = CrisisOrganization.id_crisis as id inner join Location on Crisis.id = Location.entity_id
			where organization_id = "FEMA" and not (country = "US" or country = "USA" or country = "United States");

/* -----------------------------------------------------------------------
44. Number of crises that intelligence agencies were involved in
*/

select count(*) from CrisisOrganization
	where id_organization in
		(select id as id_organization from OrganizationKind
		where id = "IA");

/* -----------------------------------------------------------------------
45. How many more orgs does America have than Britain
*/

select (count(distinct AMR) - count(distinct BRT))
	from
	(select id as AMR from Organization inner join Location on Organization.id = Location.entity_id where country = "US"),
	(select id as BRT from Organization inner join Location on Organization.id = Location.entity_id where country = "GB");

