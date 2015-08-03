alter table submission add column submitted timestamp;
alter table submission add column description character varying;
alter table submission add column url character varying;
alter table submission add column feed character varying;

--

alter table submission add column submission_id character varying;
